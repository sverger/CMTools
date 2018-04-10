###FibrilTool_angle_to_ablation###
########by Stephane Verger########

###Prerequiste: A folder containing subfodlers of the experiments/conditions to analyse
###             Each subfolder contains the "*.png" images to analyse for each conditions
###             For each "*.png" image to analyse --> Make a "*_RoiSet.zip" file for FibrilTool batch (See FibrilTool Batch)
###                                               --> Make a "*_points_log.txt" file made on the image analysed containing 
###                                                   the point to refere to for the angle to ablation calculation
###                                                   (use ImageJ (or Fiji), place points toward the ablation corresponding to 
###                                                   the cells (ROIs used for FibrilTool batch) in the same order. In the ROI manager 
###                                                   go to ->more -> list and save the list with the same name as the image and
###                                                   adding "*_points_log.txt")
###                                               --> Run fibriltool batch on each subfolder

###inputs: "*_MTs.tif" images of the FibrilTool batch output
###        "*_log.txt" files of the FibrilTool batch output
###        "*_points_log.txt" files previously made
###
###The script calculates the principal angle of the Microtubules ("*_log.txt") relative to the ablation (as defined by the user "*_points_log.txt" )
###It outputs for each image a new file "*_FTangles2ablation.txt" containing...
###It draws the line from the user defined point ("*_points_log.txt") to the center of the FibrilTool line, as well as prints the acute angle (0-90 degrees) 
###relative to the ablation on the picture and saves this image as "*_MTs_angles.tif"
###It generates and saves an histogram of angles to the ablaton (0-90 degrees) with the anisotropy weight, for each condition with 10 bins of 10 degrees
### Stats...
###It generates and saves a box plot figure comparing the anisotropies in the different conditions
### Stats...

import numpy as np
import os
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

###Directory containing all the data to analyse and compare
updir = '/home/verger/Research/Image_analysis/Papier_qua1_mechastress/Qua1_abl_MTs/reforfig/'


###Find subdirectories containing the experiments/conditions to analyse
for dirname in sorted(os.listdir(updir)):
  drpath = updir + dirname
  if os.path.isdir(drpath):
    print dirname
    
    ####Output file for all images of one condition
    fall = open(drpath + '/' + 'FTangles2ablation_all.txt', 'w')
    
    ###For each image in the directory
    for img in sorted(os.listdir(drpath)):
      if "_MTs.tif" in img:
        print 'image analyzed: ' + img
        imgpath=drpath + '/' + img
        print 'image path: ' + imgpath
        
        ###Output file for each image
        f = open(imgpath[:-4]+'_FTangles2ablation.txt', 'w')
        #print 'Output_filename: ' + imgpath[:-4]+'_FTangles2ablation.txt'
        
        ###ax = x-coordinate of FT line center
        ax = np.genfromtxt(imgpath[:-8]+'_Log.txt', delimiter='\t', usecols=2, dtype=None)
        #print ax
        ###ay = y-coordinate of FT line center
        ay = np.genfromtxt(imgpath[:-8]+'_Log.txt', delimiter='\t', usecols=3, dtype=None)
        #print ay
        ###bx = x-coordinate of point
        bx = np.genfromtxt(imgpath[:-8]+'_points_Log.txt',skip_header=1, delimiter='\t', usecols=3, dtype=None)
        #print bx
        ###by = y-coordinate of point
        by = np.genfromtxt(imgpath[:-8]+'_points_Log.txt',skip_header=1, delimiter='\t', usecols=4, dtype=None)
        #print by
        ###FTang2x = FibriTool angle to the x-axis
        FTang2x =np.genfromtxt(imgpath[:-8]+'_Log.txt', delimiter='\t', usecols=5, dtype=None)
        #print FTang2x
        ###anisotropy = FibriTool Anisotropy
        anisotropy =np.genfromtxt(imgpath[:-8]+'_Log.txt', delimiter='\t', usecols=6, dtype=None)
        #print anisotropy
        
        ###Open FT output image
        openimg = Image.open(imgpath)
        draw =ImageDraw.Draw(openimg)
        
        ###Find the number of cells to analyse in the image
        Nb_cell = len(ax)
        print 'number of cells is: ' + str(Nb_cell)
        
        ###for each cell
        for i in range(0, Nb_cell):
          ###The cell being analysed and the coordinates of the FT line center and the point with which the angles are calculated
          print '>cell ' + str(i)
          print '  x-FT--> ' +str(ax[i]) +', y-FT--> ' +str(-ay[i]) +', x-pt--> ' +str(bx[i]) +', y-pt--> ' +str(-by[i])
          ###Calculates the ablation angle to the x-axis
          Abl_ang2x = np.rad2deg(np.arctan(((-by[i]) - (-ay[i])) / (bx[i] - ax[i])))
          print '  Ablation angle to x-axis: '+str(Abl_ang2x)
          ###transform to absolute
          Abs_Abl_ang2x = np.abs(Abl_ang2x)
          ###Prints the FibrilTool angle to the x-axis
          print '  Fibriltool angle to x-axis: ' + str(FTang2x[i])
          ###Calculates the absolute angle between the ablation and FT
          FTang2abl = np.abs(FTang2x[i] - Abl_ang2x)
          print '  Absolute Fibriltool angle to ablation: ' + str(FTang2abl)
          ###If the angle is above 90 degrees, it is substracted to 180 to give the acute angle
          if FTang2abl > 90:
              FTang2abl = 180 - FTang2abl
          print '  Acute absolute Fibriltool angle to ablation: ' + str(FTang2abl)
          ###Writes output to the file for each image
          f.write(str(i) + '\t' + str(FTang2abl) + '\t' + str(ax[i]) + '\t' + str(ay[i]) + '\t' + str(bx[i]) + '\t' + str(by[i]) + '\t' + str(Abl_ang2x) + '\t' + str(FTang2x[i]) + '\t' + str(anisotropy[i]) + '\n')
          ###Writes output to the file for all images of one condition
          fall.write(str(i) + '\t' + str(FTang2abl) + '\t' + str(ax[i]) + '\t' + str(ay[i]) + '\t' + str(bx[i]) + '\t' + str(by[i]) + '\t' + str(Abl_ang2x) + '\t' + str(FTang2x[i]) + '\t' + str(anisotropy[i]) + '\n')
          ###Draw lines on image with MTs
          draw.line((ax[i],ay[i], bx[i],by[i]), fill=(255,255,0,255), width=3)
          ###Write acute angle on image with MTs
          font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
          draw.text((ax[i],ay[i]), str(round(FTang2abl,1)), fill=(0,255,0,255), font=font, width=3)
          draw.text((bx[i],by[i]), str(round(Abs_Abl_ang2x,1)), fill=(50,200,255,255), font=font, width=3)
          
        #openimg.show()
        openimg.save(imgpath[:-4]+'_angles.tif')
        f.close()
    fall.close()



###Generate histogram of angles to the ablaton (0-90 degrees) with the anisotropy weight, for each condition with 10 bins of 10 degrees
drnames = []
angledata = []
anidata = []
angledata_ = {}
anidata_ = {}
fig=1
###Find subdirectories containing the experiments/conditions to analyse
for dirname in sorted(os.listdir(updir)):
  drpath = updir + dirname
  if os.path.isdir(drpath):
    print dirname
    angledata_[dirname] = []
    anidata_[dirname] = []
    drnames.append(dirname)
    ###x = Angles of all FT to ablation for one condition
    x = np.genfromtxt(drpath + '/' + 'FTangles2ablation_all.txt', delimiter='\t', usecols=1, dtype=None)
    #print x
    ###y = Anisotropy
    y = np.genfromtxt(drpath + '/' + 'FTangles2ablation_all.txt', delimiter='\t', usecols=8, dtype=None)
    #print y
    angledata_[dirname].append(x)
    anidata_[dirname].append(y)
    angledata.append(x)
    anidata.append(y)
    #print len(x)

    ###Mode and skew
    skew=stats.skew(x)
    statskew, pskew=stats.skewtest(x)
    print "skew " + str(skew) + "pvalue" + str(pskew)
    mode=stats.mode(x)
    print "mode " + str(mode)
    
    ###Histogram of distribution with anisotropy
    figure = plt.figure(str(fig)+ '15')
    figure.clf()
    n, bins, patches = plt.hist(x,bins=([0, 15, 30, 45, 60, 75, 90]), normed=1, facecolor='grey', alpha=0.75)
    plt.xlabel('Angles(degree)', fontsize=24)
    plt.ylabel('Frequency', fontsize=24)
    #plt.title(dirname + ', N=' + str(len(x)) + ' cells', fontsize=24)
    plt.axis([0, 90, 0, 0.025])
    plt.grid(True)
    plt.show()
    figure.savefig(updir+"/"+dirname + "_histogram15.jpg")
    fig=fig+1


###Comparaisons
sampleA = ['GFP-MBD_abl_T0h', 'qua1-1GFP-MBD_abl_T0h', 'GFP-MBD_abl_T0h', 'GFP-MBD_abl_T8h', 'GFP-MBD_abl_T0h', 'GFP-MBD_abl_T8h']
sampleB = ['GFP-MBD_abl_T8h', 'qua1-1GFP-MBD_abl_T8h', 'qua1-1GFP-MBD_abl_T0h', 'qua1-1GFP-MBD_abl_T8h', 'qua1-1GFP-MBD_abl_T8h', 'qua1-1GFP-MBD_abl_T0h']
datatype = ['Angles', 'Anisotropy']
dictnames = [angledata_, anidata_]
####Output file
fdata = open(updir + '/' + 'Comparaison_of_CMT_Reorientation_and_Anisotropy_Summary.txt', 'w')

for A, B in zip(sampleA, sampleB):
  fdata.write('\n' + A + ' is sample A'+ '\n' + B + ' is sample B'+'\n')
  for data, dictn in zip(datatype, dictnames):
    fdata.write(str(data) +'comparaison'+'\n')
    fdata.write(str(np.mean(dictn[A])) + '+-' + str(np.std(dictn[A]))+'\n')
    fdata.write(str(np.mean(dictn[B])) + '+-' + str(np.std(dictn[B]))+'\n')
    
    ###T-test
    pops=[]
    pops.append(dictn[A][0])
    pops.append(dictn[B][0])
    ###Shapiro's test for normality for sample A
    w, pnormA = stats.shapiro(np.array(dictn[A][0]))
    if pnormA>0.05:
      normA = True
      print 'A sample IS normally distributed'
      fdata.write('A sample IS normally distributed'+'\n')
    else:
      normA = False
      print 'A sample is NOT normally distributed'
      fdata.write('A sample is NOT normally distributed'+'\n')
    ###Shapiro's test for normality for sample B
    w, pnormB = stats.shapiro(np.array(dictn[B][0]))
    if pnormB>0.05:
      normB = True
      print 'B sample IS normally distributed'
      fdata.write('B sample IS normally distributed'+'\n')
    else:
      normB = False
      print 'B sample is NOT normally distributed'
      fdata.write('B sample is NOT normally distributed'+'\n')
    if normA and normB is True:
      print 'Both sample have normal distibution --> t-test or Welchs test'
      fdata.write('Both sample have normal distibution --> t-test or Welchs test'+'\n')
      ###Bartlett's test for equal variance
      t, pvar = stats.bartlett(*pops)
      if pvar>0.05:
        equalvar=True
        print 'samples have equal variance--> t-test'
        fdata.write('samples have equal variance--> t-test'+'\n')
      else:
        equalvar=False
        print 'samples do not have equal variance--> Welchs test'
        fdata.write('samples do not have equal variance--> Welchs test'+'\n')
      ###t-test (Welch's if variances are unequal)
      t2, pt =stats.ttest_ind(*pops, equal_var=equalvar)
      if pt>0.05:
        print '-->populations are NOT statiscically different --> p-value is ' + str(pt)
        fdata.write('-->populations are NOT statiscically different --> p-value is ' + str(pt)+'\n'+'\n')
      else:
        print '-->populations are statiscically different --> p-value is ' + str(pt)
        fdata.write('-->populations are statiscically different --> p-value is ' + str(pt)+'\n'+'\n')
    else:
      print 'At least one sample does Not have normal distibution --> wilcoxon rank sum test'
      fdata.write('At least one sample does Not have normal distibution --> wilcoxon rank sum test'+'\n')
      statrank, prank =stats.ttest_ind(*pops)
      if prank>0.05:
        print '-->populations are NOT statiscically different --> p-value is ' + str(prank)
        fdata.write('-->populations are NOT statiscically different --> p-value is ' + str(prank)+'\n'+'\n')
      else:
        print '-->populations are statiscically different --> p-value is ' + str(prank)
        fdata.write('-->populations are statiscically different --> p-value is ' + str(prank)+'\n'+'\n')
fdata.close()


figure = plt.figure(0)
figure.clf()
ax = plt.boxplot(anidata, labels=drnames, widths= 0.7, patch_artist=True)
plt.tight_layout()
plt.show()
figure.savefig(updir+"/"+"Anisotropies.jpg")

