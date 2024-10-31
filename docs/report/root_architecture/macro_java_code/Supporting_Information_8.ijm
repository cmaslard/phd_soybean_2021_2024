// imagej-macro "root_angle" (Maslard C., 24. Jan. 2023)
// A for Mother; C for Daughter ; B for Gama (the angle) or ramification D for pointe generate with gravity for new angle (DBC)
function lenSqr( x_0, y_0, x_1, y_1 ) {
   return ( pow( x_0 - x_1, 2 ) + pow( y_0 - y_1, 2 ) );
}
requires( "1.53i" );
// Select the multi-point selection tool
setTool("multipoint");
// Declare an array to store point coordinates and the angle formed by these points


//label
result_label=newArray();

//coo
result_XA=newArray();
result_YA=newArray();
result_XB=newArray();
result_YB=newArray();
result_XC=newArray();
result_YC=newArray();
result_XD=newArray();
result_YD=newArray();
result_XC2=newArray();
result_YC2=newArray();
result_XD2=newArray();
result_YD2=newArray();

//length
result_AB=newArray();
result_BC=newArray();
result_BD=newArray();
result_CD=newArray();
result_BC2=newArray();
result_BD2=newArray();
result_C2D2=newArray();

//angle
result_angle_ABC=newArray();
result_angle_CBD=newArray();
result_angle_ABD=newArray(); // can be calculate as CBD-ABC

result_angle_ABC2=newArray();
result_angle_C2BD2=newArray();

// branching n 
result_branching_n=newArray();

// circle
result_circle=newArray();

// size pixel
result_pixel=newArray();

// plant_num
result_plant_num=newArray();

// folder
result_folder=newArray();


//left Right angle (only for ABC)
result_LeftRight=newArray();

//small root
result_small_root=newArray();

//dialogues input____
branching_n_x=1;
circle_r=10; //30
size_pixel=0.045;
clean_yesno=newArray("yes","no");
plant_num_input="1A";
folder_input="";
Dialog.create("My Options");
	Dialog.addMessage("Enter your settings here:");
	Dialog.addNumber("branching n: ",branching_n_x);
	Dialog.addString("folder name: ",folder_input);
	Dialog.addString("plant id: ",plant_num_input);
	Dialog.addNumber("Diameter in millimeters of the circle: ",circle_r);
	Dialog.addNumber("Size of each pixel in millimeters: ",size_pixel);
	Dialog.addRadioButtonGroup("Clean Image?", clean_yesno, 1, 2, "no");
Dialog.show();

branching_n_x=Dialog.getNumber();
folder_input=Dialog.getString();
plant_num_input=Dialog.getString();
circle_r=Dialog.getNumber();
size_pixel=Dialog.getNumber();

//end dialog _________

// clean img begin ______
if (Dialog.getRadioButton=="yes") {
		//run("Select None");
		run("Remove Overlay");
}


//create dataframe
Table.create("result_angle"+folder_input+"_plant_id_"+plant_num_input+"_circleS_"+circle_r+"_branching_"+branching_n_x);


waitForUser("Do you click on the first ramification? If so then click ok!");
	requires( "1.53i" );
	getSelectionCoordinates(x, y);
	if (x.length!=1) exit("Incorrect number of point selections!");
	
	// add X and Y for first ramification
	result_label= Array.concat(result_label, getTitle());
	result_XA= Array.concat(result_XA, x[0]);
	result_YA= Array.concat(result_YA, y[0]);
	result_branching_n= Array.concat(result_branching_n, 1);
	
	result_circle= Array.concat(result_circle, circle_r);
	result_pixel= Array.concat(result_pixel, size_pixel);
	result_plant_num= Array.concat(result_plant_num, plant_num_input);
	result_folder= Array.concat(result_folder, folder_input);
	
	// Na for the other add NA
		//coo
	result_XB= Array.concat(result_XB, "NaN");
	result_YB= Array.concat(result_YB, "NaN");
	result_XC= Array.concat(result_XC, "NaN");
	result_YC= Array.concat(result_YC, "NaN");
	result_XD= Array.concat(result_XD, "NaN");
	result_YD= Array.concat(result_YD, "NaN");
	result_XC2= Array.concat(result_XC2, "NaN");
	result_YC2= Array.concat(result_YC2, "NaN");
	result_XD2= Array.concat(result_XD2, "NaN");
	result_YD2= Array.concat(result_YD2, "NaN");
	
		//Length
	result_AB= Array.concat(result_AB, "NaN");
	result_BC= Array.concat(result_BC, "NaN");
	result_BD= Array.concat(result_BD, "NaN");
	result_CD= Array.concat(result_CD, "NaN");
	result_BC2= Array.concat(result_BC2, "NaN");	
	result_BD2= Array.concat(result_BD2, "NaN");
	result_C2D2= Array.concat(result_C2D2, "NaN");	
	
		//angle
	result_angle_ABC= Array.concat(result_angle_ABC, "NaN");
	result_angle_CBD= Array.concat(result_angle_CBD, "NaN");
	result_angle_ABD= Array.concat(result_angle_ABD, "NaN");
	result_angle_ABC2= Array.concat(result_angle_ABC2, "NaN");
	result_angle_C2BD2= Array.concat(result_angle_C2BD2, "NaN");

	result_LeftRight= Array.concat(result_LeftRight,"NaN");
	
	result_small_root=Array.concat(result_small_root,"NaN");
	
	
	// Tab
	Table.setColumn("branching", result_branching_n);
	
	Table.setColumn("side", result_LeftRight);
	Table.setColumn("small_root", result_small_root);
	
	Table.setColumn("Angle_ABC", result_angle_ABC);
	Table.setColumn("Angle_CBD", result_angle_CBD);
	
	Table.setColumn("XA", result_XA);
	Table.setColumn("YA", result_YA);
	Table.setColumn("XB", result_XB);
	Table.setColumn("YB", result_YB);
	Table.setColumn("XC", result_XC);
	Table.setColumn("YC", result_YC);
	Table.setColumn("XD", result_XD);
	Table.setColumn("YD", result_YD);
	Table.setColumn("XC2", result_XC2);
	Table.setColumn("YC2", result_YC2);
	Table.setColumn("XD2", result_XD2);
	Table.setColumn("YD2", result_YD2);

	Table.setColumn("AB", result_AB);
	Table.setColumn("BC", result_BC);
	Table.setColumn("BD", result_BD);
	Table.setColumn("CD", result_CD);
	Table.setColumn("BC2", result_BC2);
	Table.setColumn("BD2", result_BD2);
	Table.setColumn("C2D2", result_C2D2);
	
	Table.setColumn("Angle_ABD", result_angle_ABD);	
	Table.setColumn("Angle_ABC2", result_angle_ABC2);
	Table.setColumn("Angle_C2BD2", result_angle_C2BD2);
		
	Table.setColumn("Label", result_label);
	Table.setColumn("Circle", result_circle);
	Table.setColumn("Size_pixel", result_pixel);
	Table.setColumn("plant_id", result_plant_num);
	Table.setColumn("folder", result_folder);
	
	
	makePoint(x[0], y[0], "large cross yellow add label");
//// end of the night

while (true) {
	//run("Select None");
	//waitForUser("Do you have your first points for make circle (point of rammification)? If so then click ok!");
	
	if ( selectionType() < 1 ){	
	//print("inf to 0");
	continue; // i would like the loop to skip the part and continue the loop.
	}
	if ( selectionType() == 10 ){
		getSelectionCoordinates(x, y);
		if(x.length==1){
			//makeOval(x[0]-250, y[0]-250, 500,500); //befor 0 and 0
			Bx=x[0];
			By=y[0];
			Dx=Bx;
			D2x=Bx;
			//makePoint(Bx, By, "large cyan dot add label"); //make point B begin ____
			if (branching_n_x=="1") {
				makePoint(Bx, By, "large cyan dot add label");
			}
			else if (branching_n_x=="2") {
				makePoint(Bx, By, "large pink dot add label");
			}
			else if (branching_n_x=="3") {
				makePoint(Bx, By, "large green dot add label");
			}
			else if (branching_n_x=="4") {
				makePoint(Bx, By, "large red dot add label");
			}
			else if (branching_n_x=="5") {
				makePoint(Bx, By, "large grey dot add label");
			}
			else {
				print("The current root branching is : "+ branching_n_x);
				makePoint(Bx, By, "large black dot add label");
			}                                                  //make point B end ____
			makeOval(Bx-((circle_r/size_pixel)/2), By-((circle_r/size_pixel/2)), circle_r/size_pixel,circle_r/size_pixel);
		
	
			while (true) {
				if ( selectionType() == 10 ){
					getSelectionCoordinates(x, y);
					Ax=x[0];
					Ay=y[0];
		
					// if root too small
					ABSqr=lenSqr( Ax, Ay, Bx, By);
					AB=sqrt(ABSqr);
					root_small="no";
					if (AB>(circle_r/size_pixel)*1.5) {
						root_small="yes";
						print("root small? "+root_small);
						makeOval(Bx-((circle_r/size_pixel)/10), By-((circle_r/size_pixel/10)), (circle_r/size_pixel)/100,(circle_r/size_pixel)/100);
					}
					if(root_small=="no"){
								////make point A begin ____
					
					//	print("The current root branching is : "+ branching_n_x);
						makePoint(Ax, Ay, "small black dot add label");
					                                                  //make point A end ____
						makeOval(Bx-((circle_r/size_pixel)/2), By-((circle_r/size_pixel/2)), circle_r/size_pixel,circle_r/size_pixel);
					}

					//makePoint(x[0], y[0], "large blue dot add label") ;
					//waitForUser("dowter on circle");
					//print("test");
					while (true) {
						if ( selectionType() == 10 ){
							getSelectionCoordinates(x, y);
							Cx=x[0];
							Cy=y[0];
							Dy=Cy;
							BCSqr=lenSqr( Bx, By, Cx, Cy);
							BC=sqrt(BCSqr);
							ACSqr=lenSqr( Ax, Ay, Cx, Cy);
							AC=sqrt(ACSqr);
							BDSqr=lenSqr( Bx, By, Dx, Dy);
							BD=sqrt(BDSqr);
							CDSqr=lenSqr( Cx, Cy, Dx, Dy);
							CD=sqrt(CDSqr);
							ADSqr=lenSqr( Ax, Ay, Dx, Dy);
							AD=sqrt(ADSqr);
							
							if (BC>(circle_r/size_pixel)*1.5) {
								root_small="yes";
								makeOval(Bx-((circle_r/size_pixel)/10), By-((circle_r/size_pixel/10)), (circle_r/size_pixel)/100,(circle_r/size_pixel)/100);
							}
							
							if(root_small=="no"){
								//makePoint(x[0], y[0], "tiny cyan cross add label") ; // create C point
													//make point B begin ____
								if (branching_n_x=="1") {
									makePoint(Cx, Cy, "small cyan dot add label");
								}
								else if (branching_n_x=="2") {
									makePoint(Cx, Cy, "small pink dot add label");
								}
								else if (branching_n_x=="3") {
									makePoint(Cx, Cy, "small green dot add label");
								}
								else if (branching_n_x=="4") {
									makePoint(Cx, Cy, "small red dot add label");
								}
								else if (branching_n_x=="5") {
									makePoint(Cx, Cy, "small grey dot add label");
								}
								else {
									makePoint(Cx, Cy, "small black dot add label");
								}                                                  //make point C end ____
							}
							makeOval(250, 250, 2,2);
							while (true) {
								if ( selectionType() == 10 ){
									getSelectionCoordinates(x, y);
									C2x=x[0];
									C2y=y[0];
									D2y=C2y;
									//makePoint(x[0], y[0], "cyan cross add label") ;
									// create C2 cross
													//make point B begin ____
								if (branching_n_x=="1") {
									makePoint(C2x, C2y, "cyan cross add label");
								}
								else if (branching_n_x=="2") {
									makePoint(C2x, C2y, "pink cross add label");
								}
								else if (branching_n_x=="3") {
									makePoint(C2x, C2y, "green cross add label");
								}
								else if (branching_n_x=="4") {
									makePoint(C2x, C2y, "red cross add label");
								}
								else if (branching_n_x=="5") {
									makePoint(C2x, C2y, "grey cross add label");
								}
								else {
									makePoint(C2x, C2y, "black cross add label");
								}                                                  //make cross C2 end ____
									
									BC2Sqr=lenSqr( Bx, By, C2x, C2y);
									BC2=sqrt(BC2Sqr);
									BC2Sqr=lenSqr( Bx, By, C2x, C2y);
									BC2=sqrt(BC2Sqr);
									BD2Sqr=lenSqr( Bx, By, D2x, D2y);
									BD2=sqrt(BD2Sqr);
									
									C2D2Sqr=lenSqr( C2x, C2y, D2x, D2y);
									C2D2=sqrt(C2D2Sqr);
									
									AC2Sqr=lenSqr( Ax, Ay, C2x, C2y);
									AC2=sqrt(AC2Sqr);
									
									// Angle calculation
									angle_ABC=180*acos((ABSqr+BCSqr-ACSqr)/(2*AB*BC))/PI;
									angle_CBD=180*acos((BCSqr+BDSqr-CDSqr)/(2*BC*BD))/PI;
									angle_ABD=180*acos((ABSqr+BDSqr-ADSqr)/(2*AB*BD))/PI;
									angle_ABC2=180*acos((ABSqr+BC2Sqr-AC2Sqr)/(2*AB*BC2))/PI;
									angle_C2BD2=180*acos((BC2Sqr+BD2Sqr-C2D2Sqr)/(2*BC2*BD2))/PI;
									
									//print(AB*size_pixel+"_"+BC*size_pixel+"yes the results_angle:::::"+angle_ABC+"_"+angle_CBD+"_"+angle_ABD+"_"+angle_ABC2+"_"+angle_C2BD2);
									
									//Concat result
									result_branching_n = Array.concat(result_branching_n, branching_n_x);
									
									result_circle= Array.concat(result_circle, circle_r);
									result_pixel= Array.concat(result_pixel, size_pixel);
									result_plant_num= Array.concat(result_plant_num, plant_num_input);
									result_folder= Array.concat(result_folder, folder_input);
									
									if (Ax<Cx) {
										result_LeftRight= Array.concat(result_LeftRight,"right");
									}
									else if (Ax>Cx) {
										result_LeftRight= Array.concat(result_LeftRight,"left");
									}
									
									result_small_root= Array.concat(result_small_root,root_small);
									
									//if small root yes inducte imposibility to mesure A, C, D and angle associated. So NA
									if (root_small=="yes") {
										result_angle_ABC= Array.concat(result_angle_ABC,"NaN");
										result_angle_CBD= Array.concat(result_angle_CBD,"NaN");
										result_XA= Array.concat(result_XA, "NaN");
										result_YA= Array.concat(result_YA, "NaN");
										result_XB= Array.concat(result_XB, Bx);
										result_YB= Array.concat(result_YB, By);
										result_XC= Array.concat(result_XC, "NaN");
										result_YC= Array.concat(result_YC, "NaN");
										result_XD= Array.concat(result_XD, "NaN");
										result_YD= Array.concat(result_YD, "NaN");
										
										result_AB= Array.concat(result_AB, "NaN");
										result_BC= Array.concat(result_BC, "NaN");
										result_BD= Array.concat(result_BD, "NaN");
										result_CD= Array.concat(result_CD, "NaN");
										
										result_angle_ABD= Array.concat(result_angle_ABD,"NaN");
										result_angle_ABC2= Array.concat(result_angle_ABC2,"NaN");
									}
									else if (root_small=="no") {
										result_angle_ABC= Array.concat(result_angle_ABC,angle_ABC);
										result_angle_CBD= Array.concat(result_angle_CBD,angle_CBD);
										result_XA= Array.concat(result_XA, Ax);
										result_YA= Array.concat(result_YA, Ay);
										result_XB= Array.concat(result_XB, Bx);
										result_YB= Array.concat(result_YB, By);
										result_XC= Array.concat(result_XC, Cx);
										result_YC= Array.concat(result_YC, Cy);
										result_XD= Array.concat(result_XD, Dx);
										result_YD= Array.concat(result_YD, Dy);
										
										result_AB= Array.concat(result_AB, AB);
										result_BC= Array.concat(result_BC, BC);
										result_BD= Array.concat(result_BD, BD);
										result_CD= Array.concat(result_CD, CD);
										result_angle_ABD= Array.concat(result_angle_ABD,angle_ABD);
										result_angle_ABC2= Array.concat(result_angle_ABC2,angle_ABC2);
									}
									//if small root yes inducte imposibility to mesure A, C, D and angle associated. So NA
									
									
									
									result_XC2= Array.concat(result_XC2, C2x);
									result_YC2= Array.concat(result_YC2, C2y);
									result_XD2= Array.concat(result_XD2, D2x);
									result_YD2= Array.concat(result_YD2, D2y);
									
									result_BC2= Array.concat(result_BC2, BC2);
									result_BD2= Array.concat(result_BD2, BD2);
									result_C2D2= Array.concat(result_C2D2, C2D2);
									
									result_angle_C2BD2= Array.concat(result_angle_C2BD2,angle_C2BD2);

									result_label= Array.concat(result_label, getTitle());
	
									// show RESULT
									Table.setColumn("branching", result_branching_n);//
	
									Table.setColumn("side", result_LeftRight);//
									Table.setColumn("small_root", result_small_root);//
									
									Table.setColumn("Angle_ABC", result_angle_ABC);
									Table.setColumn("Angle_CBD", result_angle_CBD);
									
									Table.setColumn("XA", result_XA);
									Table.setColumn("YA", result_YA);
									Table.setColumn("XB", result_XB);
									Table.setColumn("YB", result_YB);
									Table.setColumn("XC", result_XC);
									Table.setColumn("YC", result_YC);
									Table.setColumn("XD", result_XD);
									Table.setColumn("YD", result_YD);
									Table.setColumn("XC2", result_XC2);
									Table.setColumn("YC2", result_YC2);
									Table.setColumn("XD2", result_XD2);
									Table.setColumn("YD2", result_YD2);
								
									Table.setColumn("AB", result_AB);
									Table.setColumn("BC", result_BC);
									Table.setColumn("BD", result_BD);
									Table.setColumn("CD", result_CD);
									Table.setColumn("BC2", result_BC2);
									Table.setColumn("BD2", result_BD2);
									Table.setColumn("C2D2", result_C2D2);
									
									Table.setColumn("Angle_ABD", result_angle_ABD);	
									Table.setColumn("Angle_ABC2", result_angle_ABC2);
									Table.setColumn("Angle_C2BD2", result_angle_C2BD2);
										
									Table.setColumn("Label", result_label);
									Table.setColumn("Label", result_label);
									Table.setColumn("Circle", result_circle);
									Table.setColumn("Size_pixel", result_pixel);
									Table.setColumn("plant_id", result_plant_num);
									Table.setColumn("folder", result_folder);
									
									makeOval(250, 250, 2,2);
									
									break;
								}
							}
							
							break;
						}
					}
				if ( selectionType() == 1 ){
					//print("end2");
					break;
				}
			
			}
		}
	}
	//Table.show(result_df);
	// imagej-macro "root_angle" (Maslard C., 24. Jan. 2023)
	//waitForUser("lets_continue ?");
	//exit(); // gamma is the angle at point B
	}
}
// imagej-macro "root_angle" (Maslard C., 24. Jan. 2023)