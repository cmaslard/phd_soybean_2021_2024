# Create by Corentin MASLARD maslard.corentin@gmail.com
# 2023.04.29
#Steps:
	# -Take all the file names (from the original files) placed in the taskid folder
	# Then the algorithm cuts them
	# Segments them with the model created by ilastik (make sure to export in 'simple segmentation' and as .png
	# Then another part of the script transforms the black pixels into black, white, or red (for roots, background, or nodules)
	# Then a function cuts the images in half for plant A to plant D
	# After that, a function measures some variable as root surface area, convex hull, width, height, etc.

#package
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse

from skimage import data, filters, color, morphology,io,util, img_as_float, img_as_ubyte, img_as_float32
from skimage.color import rgb2gray, convert_colorspace, label2rgb
from skimage.filters import threshold_otsu
from skimage.io import imread, imsave
from skimage.measure import label, perimeter,regionprops, find_contours
from skimage.morphology import convex_hull_object, closing,square, skeletonize
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.util import invert
from datetime import datetime

import numpy as np
import os
import shutil
import warnings
#import paramiko
from PIL import Image
import pandas as pd
import sys
import subprocess
import concurrent.futures
from skimage import io, img_as_float32, color, img_as_ubyte

#function
print("Tchek if ilastik and tiktorch is install on server")
print("first make the segmentation model and import the images on the server (in .png and Simple Segmentation)")
print("export your image on the server")

warnings.filterwarnings('ignore') #to delet warnings
#list input
#path_to_target=input('Path of the repertory (taskids) where the images are located in the server : ')
#model_input=input('Name of the model in Ilastik folder : ')
#path_result=input('Destination path for csv results : ')

parser = argparse.ArgumentParser(description='de blabla pour dire a quoi il sert')
parser.add_argument('--path_to_target',help='le path de mon dossier ')
parser.add_argument('--model_input',help='path du model')
parser.add_argument('--thread', default=24,type=int ,help='sum the integers (default: find the max)')

args = parser.parse_args()
#print(args.accumulate(args.integers))

path_to_target=args.path_to_target
model_input=args.model_input

def crop_image(file) :
    if file.endswith('.png'):
        filepath = os.path.join(taskid_dir, file)

        rgb_img = io.imread(filepath, as_gray=False)
        rgb_img = img_as_float32(rgb_img) 
        ndims = rgb_img.shape  # original dimensions
        if ndims[2] == 4:  # alpha present
            rgb_img = color.rgba2rgb(rgb_img)
        rgb_img = np.uint8(rgb_img * 255)
        filename, ext = os.path.splitext(file)

        r_img = rgb_img.shape[0] 
        tail = r_img / num_cut
        a = np.arange(num_cut + 1) 
        vec = a[0:(num_cut):1] * tail 
        for i in range(0, num_cut): 
            for j in range(0, num_cut):
                x = int(vec[i])
                y = int(vec[j])
                l = a[i]
                c = a[j]
                crop_img = rgb_img[y:y + int(tail), x:x + int(tail)]

                outputfile = os.path.join(path_to_target, taskid, cropped_dir,
                                          (filename + '_' + str(l + 1) + '_' + str(c + 1) + '.png'))
                if not os.path.isfile(outputfile):
                    print(outputfile)
                    tmp = os.path.dirname(outputfile)
                    if not os.path.isdir(tmp):
                        os.makedirs(tmp)
                    io.imsave(outputfile, img_as_ubyte(crop_img))  # ubyte = int [0:255] precision 8 bits

def process_ilastik_segmentation(infile):
    if infile.endswith('.png'):
        command = './run_ilastik.sh --headless --readonly --project=',ilastik_project,' ', os.path.join(indir,infile), ' --export_source="Simple Segmentation" '
        command = "".join(command)
        print(command)
        subprocess.call(command, shell=True)

def fusion_image(file_name):
    background=[]
    root=[]
    nod=[]
    compile_name=[]
    background_n = 0
    root_n = 0
    nod_n = 0
    if file_name.endswith('.png'):
        print(file_name[:-4])
        file2 = [file_name[:-4], '_Simple_Segmentation_compil_', str(num_cut), '.png']
        file2 = "".join(file2)
        if not os.path.exists(
                os.path.join(output_folder, file2)):  
            new_img = Image.new('RGB', (tail_img, tail_img), (250, 250, 250))
            for file_cut in files_cut:

                if file_cut.startswith(file_name[:-4]) and file_cut.endswith(assembly_type):
                    file_cut_path = os.path.join(taskid_cut_dir, file_cut)
                    n_img = Image.open(file_cut_path)
                    largeur, hauteur = n_img.size
                    imageBrut = Image.new("RGB", (largeur, hauteur))

                    print(file_cut)

                    coo_img_x = int(file_cut[-25])
                    coo_img_y = int(file_cut[-27])

                    for y in range(hauteur):
                        # pour chaque colonne :
                        for x in range(largeur):

                            p = n_img.getpixel((x, y))


                            if p == 1:
                                p = (255, 255, 255)
                                background_n = background_n + 1
                            if p == 3:
                                nod_n = nod_n + 1
                                p = (255, 0, 0)
                            if p == 2:
                                p = (0, 0, 0)
                                root_n = root_n + 1

                            imageBrut.putpixel((x, y), p)
                    
                    new_img.paste(imageBrut, (int((coo_img_y - 1) * img_size), int((coo_img_x - 1) * img_size)))


            file2 = [file_name[:-4], '_Simple_Segmentation_compil_', str(num_cut), '.png']
            file2 = "".join(file2)
            compile_name.append(file_name[:-4])
            background.append(str(background_n))
            root.append(str(root_n))
            nod.append(str(nod_n))

            print(os.path.join(output_folder, file2))
            new_img.save(os.path.join(output_folder, file2), "PNG")
            print("finit")



        df = pd.DataFrame({"Label": compile_name, "root": root, "background": background, "nod": nod})
        print(df)

        chemin = [output_folder, "/result_nb_pixel.csv"]
        chemin = "".join(chemin)
        df.to_csv(chemin, mode='a',decimal=",", index=False,header=not os.path.exists(chemin))

def selection_plant(file) :
    background = []
    root=[]
    nod=[]
    compile_name=[]
    if file.endswith(verif):

        name_img = [file[:-4], "_D.png"]
        name_img = "".join(name_img)
        if not os.path.exists(
                os.path.join(fusion_dir2, "D", name_img)):  # permet de passer a une autre image si il y en a deja une
            print(file)
            file_path = os.path.join(fusion_dir2, file)
            n_img = Image.open(file_path)
            largeur, hauteur = n_img.size

            imageBrutD = Image.new("RGB", (largeur, hauteur), (212, 230, 241))
            imageBrutA = Image.new("RGB", (largeur, hauteur), (212, 230, 241))


            print("for plant D")
            background_n = 0
            root_n = 0
            nod_n = 0

            for x in range(plant_D_position[0], plant_D_position[1]):

                for y in range(hauteur_rhyzo[0], hauteur_rhyzo[1]):
                    p = n_img.getpixel((x, y))

                    if p == (255, 255, 255):
                        p = (255, 255, 255)
                        background_n = background_n + 1
                        # print("coucou")
                    if p == (0, 0, 0):
                        p = (0, 0, 0)
                        root_n = root_n + 1
                    if p == (255, 0, 0):
                        p = (255, 0, 0)
                        nod_n = nod_n + 1

                    imageBrutD.putpixel((x, y), p)

            imageBrutD.save(os.path.join(fusion_dir2, "D", name_img), "PNG")

            compile_name.append(name_img[:-4])
            background.append(str(background_n))
            root.append(str(root_n))
            nod.append(str(nod_n))

            print("for plantA")
            background_n = 0
            root_n = 0
            nod_n = 0

            for x in range(plant_D_position[1], largeur):

                for y in range(hauteur_rhyzo[0], hauteur_rhyzo[1]):
                    p = n_img.getpixel((x, y))

                    if p == (255, 255, 255):
                        p = (255, 255, 255)
                        background_n = background_n + 1

                    if p == (0, 0, 0):
                        p = (0, 0, 0)
                        root_n = root_n + 1
                    if p == (255, 0, 0):
                        p = (255, 0, 0)
                        nod_n = nod_n + 1

                    imageBrutA.putpixel((x - plant_D_position[1], y), p)

            print("for small part of the plant A")
            for x in range(0, plant_D_position[0]):

                for y in range(hauteur_rhyzo[0], hauteur_rhyzo[1]):
                    p = n_img.getpixel((x, y))

                    if p == (255, 255, 255):
                        p = (255, 255, 255)
                        background_n = background_n + 1

                    if p == (0, 0, 0):
                        p = (0, 0, 0)
                        root_n = root_n + 1
                    if p == (255, 0, 0):
                        p = (255, 0, 0)
                        nod_n = nod_n + 1

                    imageBrutA.putpixel((x + largeur - plant_D_position[1], y), p)


            name_img = [file[:-4], "_A.png"]
            name_img = "".join(name_img)
            imageBrutA.save(os.path.join(fusion_dir2, "A", name_img), "PNG")


            compile_name.append(name_img[:-4])
            background.append(str(background_n))
            root.append(str(root_n))
            nod.append(str(nod_n))
            # print(nod, root, background)
            if not len(root) == 0:
                df = pd.DataFrame({"Label": compile_name, "root": root, "background": background, "nod": nod})
                # print(df)

                chemin = [fusion_dir2, "/result_nb_pixel_by_plant.csv"]
                chemin = "".join(chemin)
                df.to_csv(chemin, mode='a', decimal=",", index=False,header=not os.path.exists(chemin))


def analyse_image(file) :
    verif = ["_", assembly_type2, "_compil_", str(num_cut), "_", folder, ".png"]
    verif = "".join(verif)
    print(file)
    print(verif)
    if file.endswith(verif):
        Label = [];
        compile_name = [];
        num_label = [];
        perimeter = [];
        area = [];
        profondeur = [];
        largeur = []
        file_path = os.path.join(folder_path, file)
        # debut de la lecture de l'image
        print("lecture_img")
        read_img = io.imread(file_path)
        # ajouter le 2/2/2021
        read_img = img_as_float32(read_img)  # float32 = [0:1] precision 32 bits
        ndims = read_img.shape  # original dimensions
        if ndims[2] == 4:  # alpha present
            read_img = color.rgba2rgb(read_img)
        read_img = np.uint8(read_img * 255)

        print("transformation_gris")  # Lecture et creation d'un tableau numpy

        img_gray = rgb2gray(read_img)
        image_rescaled = rescale(img_gray, 0.25,
                                 anti_aliasing=False)  # ne pas oublier la conversion a la fin. avec 0,25 je passe de 12000 à 3000 (et c'est vachement plus rapide !!!)
        print("resize")
        thresh = threshold_otsu(image_rescaled)
        bin = image_rescaled > thresh;
        print("treshold")  # image binomial

        bin = invert(bin)  # inversion des couleurs

        print('morphology_closing')

        image_rescaled2 = morphology.binary_closing(bin, morphology.disk(18)).astype(  
            np.int)  

        print("convex_hull")
        chull = convex_hull_object(image_rescaled2)

        name_file1 = [file[:-4], "_convex_hull.png"]
        name_file1 = "".join(name_file1)
        print(output_folder)
        print(os.path.join(output_folder, name_file1))

        imsave(os.path.join(output_folder, name_file1), invert(img_as_ubyte(chull)))

        print("analyser convex_hull")
        label_image = label(chull)
        image_label_overlay = label2rgb(label_image, image=chull, bg_label=0)

        fig, axes = plt.subplots(1, 2, figsize=(8, 4))
        ax = axes.ravel()
        ax[1].imshow(image_label_overlay)

        for region in regionprops(label_image):
            # take regions with large enough areas
            if region.area >= 60000:  
                # draw rectangle around segmented coins
                minr, minc, maxr, maxc = region.bbox
                rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False,
                                          edgecolor='red', linewidth=2)
                circle = mpatches.Circle((region.centroid), 25)
                ax[1].add_patch(circle)
                ax[1].add_patch(rect)
                print(region.label)
                print(region.perimeter)
                print(region.area)
                print(maxr - minr)
                print(maxc - minc)
                print(region.centroid)

                # creation des donnees
                Label.append(file[:-4])
                num_label.append(str(region.label))
                perimeter.append(str(region.perimeter))
                area.append(region.area)
                profondeur.append(maxr - minr)
                largeur.append(maxc - minc)

        ax[1].set_title('Convex_hull')
        ax[1].set_axis_off()

        ax[0].set_title('Original picture')
        ax[0].imshow(bin, cmap=plt.cm.gray)
        ax[0].set_axis_off()

        name_file2 = ["resume_", file[:-4], "_convex_hull2.png"]
        name_file2 = "".join(name_file2)

        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, name_file2), dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None,
                    pad_inches=0.1, frameon=None, metadata=None)

        # exportation des donnees
        df = pd.DataFrame({"Label": Label, "num_label": num_label, "perimeter": perimeter, "area": area,
                           "profondeur": profondeur, "largeur": largeur})

        chemin = [fusion_dir2, "/result_convex_hull.csv"]
        chemin = "".join(chemin)
        df.to_csv(chemin, mode='a', decimal=",", index=False, header=not os.path.exists(chemin))


def skeletonize_root(list_file) :
    compile_name = []
    length_skull = []
    file_path=os.path.join(path_to_target_folder,list_file)
    read_img = io.imread(file_path)
    read_img = img_as_float32(read_img)  # float32 = [0:1] precision 32 bits
    ndims = read_img.shape  # original dimensions
    if ndims[2] == 4:  # alpha present
        read_img = color.rgba2rgb(read_img)
    read_img = np.uint8(read_img * 255)
    img_gray = rgb2gray(read_img)
    #print("invert and thresh")
    thresh = threshold_otsu(img_gray)
    bin = img_gray > thresh
    bin = invert(bin)  # inversion des couleurs
    skeleton = skeletonize(bin)
    name_file1 = [list_file[:-4], "_skeletonize.png"]
    name_file1 = "".join(name_file1)
    imsave(os.path.join(output_folder, name_file1), img_as_ubyte(invert(skeleton)))
    compile_name.append(list_file[:-4])
    print(compile_name)
    length_skull_n=np.sum(skeleton)*0.0042
    length_skull.append(int(length_skull_n))
    print(length_skull)
    df = pd.DataFrame({"Label": compile_name, "length_skull": length_skull})
    print(df)
    chemin = [path_to_target,"/",taskid,"/","fusion_Simple Segmentation.png_4", "/result_skull.csv"]
    chemin = "".join(chemin)
    print("write")
    print(chemin)
    df.to_csv(chemin, mode='a',decimal=",", index=False,header=not os.path.exists(chemin))

##parameter

num_cut=int(4)
cropped_dir = ["cut_img","_",str(num_cut)]
cropped_dir="".join(cropped_dir)
taskids = os.listdir(path_to_target)
taskids.sort()
assembly_type='Simple Segmentation'
assembly_type=[assembly_type,".png"]
assembly_type="".join(assembly_type)
num_cut_folder=["cut_img_",str(num_cut)] ;num_cut_folder="".join(num_cut_folder)
fusion_dir = ['fusion_', assembly_type,'_',str(num_cut)]
fusion_dir="".join(fusion_dir) ; print(fusion_dir) 
tail_img=12000
img_size=tail_img/num_cut
#print(taskids)

#for segmentation
home_path='/home/cmaslard/'
ilastik_location = os.path.join(home_path,'ilastik-1.3.3post3-Linux')
ilastik_project = os.path.join(home_path,'ilastik-1.3.3post3-Linux/',model_input)

#for selection plant
#add in input user (may be)
#plant_D_position=[1750,7500]
plant_D_position=[1400,7400]
hauteur_rhyzo=[0,11500]
#juste pour rajouter l'enderscor
assembly_type2="Simple_Segmentation"
verif=["_",assembly_type2,"_compil_",str(num_cut),".png"]
verif="".join(verif)

#analyse root
letter_folders=["A","D"]

#fichier log dans le repertoire
fichier_log = open("log_verif_nb_image.txt", "a") #pour une ouverture en mode ajout à la fin du fichier (APPEND). Si le fichier n'existe pas python le crée.
fichier_log.write('\n' + '\n' + '\t'+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ "This log file is automatically generated to check the number of images at each step to see if there are any problems, omissions etc.")
fichier_log.close()

############# crop image ###############

for taskid in taskids:
    taskid_dir = os.path.join(path_to_target, taskid)
    if taskid.isnumeric() and os.path.isdir(taskid_dir):
        fusion_dir2 = os.path.join(taskid_dir, fusion_dir) #pour selection plant
        print_taskids = ["crop : ", taskid_dir]
        print_taskids = "".join(print_taskids)
        print(print_taskids)

        # compter le nombre de fichier decouper et segmenter pour log
        initial_count = 0
        for path in os.listdir(taskid_dir):
            if os.path.isfile(os.path.join(taskid_dir, path)):
                initial_count += 1

        fichier_log = open("log_verif_nb_image.txt",
                           "a")  # pour une ouverture en mode ajout à la fin du fichier (APPEND). Si le fichier n'existe pas python le crée.
        fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ 'nb_initial_img_in_task:' + str(initial_count))
        fichier_log.close()

        #files = os.listdir(taskid_dir)
        files = [file for file in os.listdir(taskid_dir) if file.endswith('.png')]
        files.sort()

        output_folder = os.path.join(path_to_target, taskid, cropped_dir)
        # print(output_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with concurrent.futures.ProcessPoolExecutor(args.thread*21) as executor:  # ici 32 le nombre de tache qu'il execute en même temps
            executor.map(crop_image, files)

        ############## segmentation ################

        taskid_cut_dir = os.path.join(path_to_target, taskid, num_cut_folder)
        indir=os.path.join(home_path,taskid_cut_dir)
        print_taskids = ["segmentation : ", taskid_cut_dir]
        print_taskids = "".join(print_taskids)
        print(print_taskids)
        infiles=os.listdir(indir)
        infiles.sort()

	#log
        initial_count = 0
        for path in os.listdir(indir):
            if os.path.isfile(os.path.join(indir, path)):
                initial_count += 1

            #data input
        fichier_log = open("log_verif_nb_image.txt", "a") 
        fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+'nb_crop_img:'+str(initial_count))
        fichier_log.close()

        #warning, change of directory

        os.chdir(ilastik_location)

        with concurrent.futures.ProcessPoolExecutor(14) as executor:  
            executor.map(process_ilastik_segmentation, infiles)

        os.chdir(home_path)

        ######## fusion_img #########################
        files_n = []
        files_cut = os.listdir(taskid_cut_dir)
        files_cut.sort()
        print_taskids = ["fusion : ", taskid_cut_dir] ; print_taskids = "".join(print_taskids) ; print(print_taskids) 
        # compter le nombre de fichier decouper et segmenter pour log
        initial_count = 0
        for path in os.listdir(taskid_cut_dir):
            if os.path.isfile(os.path.join(taskid_cut_dir, path)):
                initial_count += 1

            # data input
        fichier_log = open("log_verif_nb_image.txt","a") 
        fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ 'nb_crop_and_segmentation_img:' + str(initial_count))
        fichier_log.close()

        output_folder = os.path.join(path_to_target, taskid, fusion_dir)
        # print(output_folder)
        compile_name=[]
        background = []
        root = []
        nod = []

        # creation du dossier
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        print(files)
        with concurrent.futures.ProcessPoolExecutor(82) as executor:  
            executor.map(fusion_image, files)

        initial_count = 0
        for path in os.listdir(fusion_dir2):
            if os.path.isfile(os.path.join(fusion_dir2, path)):
                initial_count += 1

            # data input
        fichier_log = open("log_verif_nb_image.txt", "a")  
        fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ 'nb_fustion_img:' + str(initial_count)+' '+str(files))
        fichier_log.close()

        ########### delet folder #########################
        print("delet foldet cut_img_4")
        shutil.rmtree(os.path.join(path_to_target, taskid, cropped_dir))

        ########selection plant ###############
        root = []
        if os.path.isdir(fusion_dir2):
            #cree les dossiers A et D si il n'existe pas
            output_folderA=os.path.join(fusion_dir2,'A')
            output_folderD = os.path.join(fusion_dir2, 'D')
            if not os.path.exists(output_folderA):
                os.makedirs(output_folderA)
            if not os.path.exists(output_folderD):
                os.makedirs(output_folderD)

            files = os.listdir(fusion_dir2)
            files.sort()  

            compile_name = []
            background = []
            root = []
            nod = []

            with concurrent.futures.ProcessPoolExecutor(args.thread*12) as executor:
                executor.map(selection_plant,files)

        ############## analyse root ###################
        print("analyse root")
        output_folder = os.path.join(taskid_dir, fusion_dir, "convex_hull")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if os.path.isdir(fusion_dir2):
            Label = []
            compile_name = []
            num_label = []
            perimeter = []
            area = []
            profondeur = []
            largeur = []
            for folder in letter_folders:  # if A ou D
                folder_path = os.path.join(fusion_dir2, folder)
                print(folder_path)

                initial_count = 0
                for path in os.listdir(folder_path):
                    if os.path.isfile(os.path.join(folder_path, path)):
                        initial_count += 1

                    # data input
                fichier_log = open("log_verif_nb_image.txt",
                                   "a")  
                fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ 'nb_plante_folder_'+folder +'_img:' + str(initial_count))
                fichier_log.close()
                #end log file

                files = os.listdir(folder_path)
                files.sort()  

                with concurrent.futures.ProcessPoolExecutor(args.thread*5) as executor:  
                    executor.map(analyse_image, files)


                initial_count = 0
                for path in os.listdir(output_folder):
                    if os.path.isfile(os.path.join(output_folder, path)):
                        initial_count += 1

                    # data input
                fichier_log = open("log_verif_nb_image.txt", "a")  
                fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ 'nb_img_convex:' + str(initial_count))
                fichier_log.close()

        ############## analyse skull ###################
        print("skull measure")
        output_folder = os.path.join(path_to_target, taskid, 'fusion_Simple Segmentation.png_4', "skeletonize")
        file_to_del_path = os.path.join(path_to_target, taskid, 'fusion_Simple Segmentation.png_4', "result_skull.csv")
        if os.path.exists(file_to_del_path):
            os.remove(file_to_del_path)
        if taskid.isnumeric():
            # making new dir
            list_files = []
            compile_name = []
            length_skull = []


            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for letter_folder in letter_folders:

                path_to_target_folder = os.path.join(path_to_target, taskid, 'fusion_Simple Segmentation.png_4',
                                                     letter_folder)
                print(path_to_target_folder)
                # print(os.listdir(path_to_target_folder))
                list_files_x = os.listdir(path_to_target_folder)
                for list_file_x in list_files_x:
                    list_files.append(list_file_x)
                with concurrent.futures.ProcessPoolExecutor(args.thread*15) as executor:  
                    executor.map(skeletonize_root, list_files)

            initial_count = 0
            for path in os.listdir(output_folder):
                if os.path.isfile(os.path.join(output_folder, path)):
                    initial_count += 1

                # data input
            fichier_log = open("log_verif_nb_image.txt", "a")  
            fichier_log.write('\n'+taskid+"\t"+datetime.now().strftime("%d/%m/%y %H:%M")+'\t'+ 'nb_img_skull:' + str(initial_count))
            fichier_log.close()