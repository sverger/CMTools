###MTAngleToAblation_vs_CellAngleToX###
########by Stephane Verger########

### !!!!Uses output from "Script_FTBatch_AngleToAblation.py"!!!!

import numpy as np
import os
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

###Directory containing the FTangles2ablation_all.txt file
updir = '/home/verger/Research/Image_analysis/Papier_qua1_mechastress/Qua1_abl_MTs/20170323-qua1-1MBD_abl_8h_quantif/'
directory = 'GFP-MBD_abl_T8h'
Filepath = updir + directory + '/' + 'FTangles2ablation_all.txt'

###Load angle data
###Abl_ang2x = Angle between the ablation and the cell relative to x
Abl_ang2x = np.genfromtxt(Filepath, delimiter='\t', usecols=6, dtype=None)
#print Abl_ang2x
###FT_ang2abl = Angle of CMT relative to x (From FibrilTool)
FT_ang2abl = np.genfromtxt(Filepath, delimiter='\t', usecols=1, dtype=None)
print FT_ang2abl

###transform to absolute
Abs_Abl_ang2x = np.abs(Abl_ang2x)
print Abs_Abl_ang2x


###Scatter plot
figure = plt.figure(directory)
figure.clf()
plt.scatter(Abs_Abl_ang2x, FT_ang2abl)
#plt.xlabel('Acute angle (degree) relative'+'\n'+'to the longitudinal axis of the hypocotyl', fontsize=18)
#plt.ylabel('Acute angle (degree) relative to the ablation', fontsize=18)
#plt.title(directory, fontsize=24)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.axis([0, 90, 0, 90])
plt.tight_layout()
figure.savefig(updir + 'Scatterplot_MTAng2AblvsCellAng2X_'+ directory + '20' + '.png')

###Boxplot of binned data
###Binning data

zipped = zip(FT_ang2abl, Abs_Abl_ang2x)
group1 = []
group2 = []
group3 = []
group4 = []
group5 = []
group6 = []
groups = [group1, group2, group3, group4, group5, group6]
for i in zipped:
    if 0<i[1]<15:
        group1.append(i[0])
    elif 15<i[1]<30:
        group2.append(i[0])
    elif 30<i[1]<45:
        group3.append(i[0])
    elif 45<i[1]<60:
        group4.append(i[0])
    elif 60<i[1]<75:
        group5.append(i[0])
    elif 75<i[1]<90:
        group6.append(i[0])

groupsnames = ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90']
FT_angle_data = []
for g in groups:
    FT_angle_data.append(g)
print FT_angle_data

###Boxplox
figure = plt.figure()
figure.clf()
ax = plt.boxplot(FT_angle_data, labels=groupsnames, widths= 0.7, patch_artist=True)
plt.tight_layout()
figure.savefig(updir + 'Boxplot_MTAng2AblvsCellAng2X_'+ directory + '.jpg')

posi = [7.5, 22.5, 37.5, 52.5, 67.5, 82.5]

###Boxplot-scatterplo overlay
figure = plt.figure()
figure.clf()
plt.boxplot(FT_angle_data, positions = posi, widths= 10, manage_xticks=True)
plt.scatter(Abs_Abl_ang2x, FT_ang2abl)
plt.xlabel('Acute angle (degree) relative'+'\n'+'to the longitudinal axis of the hypocotyl', fontsize=18)
plt.ylabel('Acute angle (degree) relative to the ablation', fontsize=18)
#plt.xticks(0, 15, 30, 45, 60, 75, 90)
plt.title(directory, fontsize=24)
plt.axis([0, 90, 0, 90])
plt.tight_layout()
plt.show()
figure.savefig(updir + 'box-Scatterplot_MTAng2AblvsCellAng2X_'+ directory + '.jpg')


