//////////////////////////////////////////////////////////////////////////////////
//////////////////Cell segmentation for automated FibrilTool//////////////////////
/////////////////////////Stephane Verger, Post Doc////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////

//This macro allows a semi-automated segmentation and creation of ROI sets for fibrilToolBatch (Creates input for Fibril_Tool_Batch_Seg.ijm).
//As input you need 2D images of cell contours (..._cells.tif) and a matching 2D image of the mircotubule arrays (..._MTs.tif). These can be created using Surfcut macro (https://github.com/sverger/SurfCut).
//Put the _cells.tif and _MTs.tif images in a unique directory (as many as you want).
//For each sample, the _cells.tif and _MTs.tif must share the same name: sample1_cells.tif, sample1_MTs.tif, sample2_cells.tif, sample2_MTs.tif,...
//Select this directory when you start the macro.
//As an output, it creates _MTs_RoiSet.zip files with the same name as your samples (sample1_MTs_RoiSet.zip, sample2_MTs_RoiSet.zip,...), which contain the ROIs that will be used as an input for Fibril_Tool_Batch_Seg.ijm


dir = getDirectory("Choose a directory")

list = getFileList(dir);

for (j=0; j<list.length; j++){
	//print("entering loop 1");
	if(endsWith (list[j], "_cells.tif")){
	print("file_path",dir+list[j]);
	open( dir+File.separator+list[j] );
	file_name1=substring(list[j],0,indexOf(list[j],".tif"));
	file_name2=substring(list[j],0,indexOf(list[j],"_cells.tif"));
    //print (file_name);
    run("8-bit");
    run("Gaussian Blur...", "sigma=3");
    //waitForUser("If needed...", "Blur more? Close cell?...");
    run("Morphological Segmentation");
    wait(1000);
    call("inra.ijpb.plugins.MorphologicalSegmentation.setInputImageType", "border");
    call("inra.ijpb.plugins.MorphologicalSegmentation.segment", "tolerance=10", "calculateDams=true", "connectivity=6");
    waitForUser("Watershed segmentation", "Rerun the watershed segmentation with appropriate parameters if necessary.\nWhen you are satisfied, click OK here!");
    call("inra.ijpb.plugins.MorphologicalSegmentation.setDisplayFormat", "Watershed lines");
    call("inra.ijpb.plugins.MorphologicalSegmentation.createResultImage");
    selectWindow("Morphological Segmentation");
    close();
    selectWindow(list[j]);
    close();
    selectWindow(file_name1+"-watershed-lines.tif");
    run("Dilate");
    run("Dilate");
    run("Dilate");
    run("Dilate");
    run("Invert");
    run("Analyze Particles...", "size=1000-100000 clear add");

    Dialog.create("Satisfied with ROI sizes");
    Dialog.addCheckbox("Satisfied?", true);
    Dialog.show();
    Satisfied = Dialog.getCheckbox();
    while (Satisfied==false){ 
    	run("Analyze Particles...");
    	Dialog.create("Satisfied with ROI sizes");
        Dialog.addCheckbox("Satisfied?", false);
        Dialog.show();
        Dialog.addCheckbox("Satisfied?", false);
        Satisfied = Dialog.getCheckbox();
    }

    open(dir+File.separator+file_name2+"_MTs.tif" );
    roiManager("Show All");
    waitForUser("Manage ROIs", "If needed, move or remove some ROIs to fit your needs\nSome ROIs may not be well aligned with the cells on the MTs images\nWhen you are satisfied, click OK here.");
	roiManager("Save", dir+File.separator+file_name2+"_MTs_RoiSet.zip");
	selectWindow(file_name2+"_MTs.tif");
	close();
	selectWindow(file_name1+"-watershed-lines.tif");
	close();
	roiManager("Delete");
	}
}
selectWindow("ROI Manager");
run("Close");
print ("End of the Seg_forFTBatch macro"); 
