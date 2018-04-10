//////////////////////////////////////////////////////////////////////////////////
//////////////////Cell segmentation for automated FibrilTool//////////////////////
/////////////////////////Stephane Verger, Post Doc////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////

//This macro allows a semi-automated segmentation and creataion of ROI sets for fibrilToolBatch (Creates input for Fibril_Tool_Batch_Seg.ijm).
//As input you need 2D images of cell contours (..._cells.png) and a matching 2D image of the mircotubule arrays (..._MTs.png). These can be created using MGX, by creating a rough surface, cropping the stack at a specific distance (with the anihilate function) to obtain either the microtubule arrays or the cell contours. 2D images (.png) can then be obtained with the snapshot function.
//Put the _cells.png and _MTs.png images in a unique directory (as many as you want).
//For each sample, the _cells.png and _MTs.png must share the same name: sample1_cells.png, sample1_MTs.png, sample2_cells.png, sample2_MTs.png,...
//Select this directory when you start the macro.
//As an output, it creates _MTs_RoiSet.zip files with the same name as your samples (sample1_MTs_RoiSet.zip, sample2_MTs_RoiSet.zip,...), which contain the ROIs that will be used as an input for Fibril_Tool_Batch_Seg.ijm


dir = getDirectory("Choose a directory")

list = getFileList(dir);

for (j=0; j<list.length; j++){
	//print("entering loop 1");
	if(endsWith (list[j], "_MTs.png")){
	print("file_path",dir+list[j]);
	open(dir+File.separator+list[j]);
	file_name1=substring(list[j],0,indexOf(list[j],".png"));
    //print (file_name);
	setTool("polyline");
	selectWindow(list[j]);
	waitForUser("Draw walls", "Click OK here when done.");
	setMinAndMax(255, 255);
	roiManager("Deselect");
	roiManager("Draw");
	setOption("BlackBackground", false);
    run("Make Binary");
    run("Dilate");
    run("Dilate");
    run("Dilate");
    run("Invert");
    run("Analyze Particles...", "size=1000-100000 clear add");
    selectWindow(list[j]);
    close();
    open(dir+File.separator+list[j]);
    roiManager("Show All");
    waitForUser("Manage ROIs", "If needed, move or remove some ROIs to fit your needs\nSome ROIs may not be well aligned with the cells on the MTs images\nWhen you are satisfied, click OK here.");
	roiManager("Save", dir+File.separator+file_name1+"_RoiSet.zip");
	selectWindow(list[j]);
	close();
	roiManager("Delete");
	}
}
selectWindow("ROI Manager");
run("Close");
print ("End of the Seg_forFTBatch macro"); 
