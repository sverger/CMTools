import numpy as np
import pandas as pd
import os
import pycircstat
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.patheffects as patheffects



directory = '/home/verger/Research/Image_analysis/Papier_qua1_mechastress/Hypo_qua1-1MBD_2,5%/Analysis_Hypo_qua1-1MBD_2,5%/2,5%'




fall = open(directory + '/' + 'FTangles_and_anisotropy_all.txt', 'w')
fdata = open(directory + '/' + 'CMT_Orientation_Summary.txt', 'w')

fdata.write('Directory used: ' + '\n' + directory + '\n' + 'Files analysed: ' + '\n')

angles_to_x = []
Rad_angles_to_x_pi = []
Rad_angles_to_x_pi_X2 = []
Rad_angle_pi_X2_ = {}
Rad_angle_pi_ = {}

samples = 0
for filename in os.listdir(directory):
  if "_Log.txt" in filename:
    filepath = directory+"/"+filename
    print (directory+"/"+filename)
    Rad_angle_pi_[filename]=[]
    Rad_angle_pi_X2_[filename]=[]
    samples = samples+1
    fdata.write(filepath + '\n')
    ###angle to x = FibriTool angle to the x-axis
    angle_to_x =np.genfromtxt(filepath, delimiter='\t', usecols=5, dtype=None)
    #print angle_to_x
    Rad_angle_to_x = np.deg2rad(angle_to_x)
    for a in Rad_angle_to_x:
      #print 'a'+ str(a)
      if a<0:
        a = a+(np.pi)
      b = a*2
      #print 'b'+ str(a)
      Rad_angles_to_x_pi.append(a)
      Rad_angles_to_x_pi_X2.append(b)
      Rad_angle_pi_[filename].append(a)
      Rad_angle_pi_X2_[filename].append(b)
    print str(len(Rad_angle_pi_X2_[filename]))
    #print Rad_angle_pi_[filename]
    print Rad_angle_pi_X2_[filename]
    #print Rad_angle_pi_X2_filename
    
    ###anisotropy = FibriTool Anisotropy
    anisotropy =np.genfromtxt(filepath, delimiter='\t', usecols=6, dtype=None)
    #print anisotropy
    
    
    #print np.rad2deg(stats.circmean(Rad_angle_pi_[filename], high = np.pi, low = 0))
    #print np.rad2deg(stats.circstd(Rad_angle_pi_[filename], high = np.pi, low = 0))
    #print pycircstat.resultant_vector_length(np.array(Rad_angle_pi_X2_[filename]))
    #mean_angle=np.rad2deg(stats.circmean(Rad_angle_to_x, high = np.pi/2, low = -np.pi/2))
    #print np.mean(angle_to_x)
    #print np.std(angle_to_x)
    #print np.mean(anisotropy)
    #print np.std(anisotropy)
    fdata.write('Number of cells analysed: '+ str(len(angle_to_x)) +'\n'+'Circ_Mean Angle to x (+-Std) --> ' + str(np.rad2deg(stats.circmean(Rad_angle_pi_[filename], high = np.pi, low = 0))) + '+-' + str(np.rad2deg(stats.circstd(Rad_angle_pi_[filename], high = np.pi, low = 0))) + ' degrees'+ '\n'+ 'Resultant_vector_length '+ str(pycircstat.resultant_vector_length(np.array(Rad_angle_pi_X2_[filename])))+ '\n' + 'Mean Anisotropy (+-Std) --> ' + str(np.mean(anisotropy)) + '+-' + str(np.std(anisotropy))+ '\n'+ '\n')
    ###Polar histogram
    figure = plt.figure()
    figure.clf()
    figure.patch.set_facecolor('k')
    ax = figure.add_subplot(111,polar=True)
    colormap = "plasma"
    n_bins = 36
    for offset in [0, np.pi]:
        histo, bins, patches = figure.gca().hist(offset+angle_to_x*np.pi/180,bins=offset+np.linspace(-90,90,n_bins/2 + 1)*np.pi/180.,ec='k',weights=anisotropy)
        norm = colors.Normalize(0,histo.max())
        for h, p in zip(histo, patches):
            p.set_facecolor(cm.get_cmap(colormap)(norm(h)))
    figure.gca().set_yticks([])
    #plt.show()
    figure.savefig(directory+"/"+filename[:-4]+"_FT_polarhist.jpg")

    
    Nb_cell = len(angle_to_x)
    #print 'number of cells is: ' + str(Nb_cell)
    ###for each cell
    for j in range(0, Nb_cell):
      #print '>cell ' + str(i)
      #Mean_angle_to_zero = angle_to_x[i]-mean_angle
      #angle_to_x_90 = angle_to_x[i]+90
      ###Writes output to the file for all images of one condition
      fall.write(str(j) + '\t' + str(angle_to_x[j])+ '\t' + str(anisotropy[j]) + '\n')
fall.close()
all_angles_to_x =np.genfromtxt(directory + '/' + 'FTangles_and_anisotropy_all.txt', delimiter='\t', usecols=1, dtype=None)
#angles_to_x_90 =np.genfromtxt(directory + '/' + 'FTangles_and_anisotropy_all.txt', delimiter='\t', usecols=2, dtype=None)
anisotropies =np.genfromtxt(directory + '/' + 'FTangles_and_anisotropy_all.txt', delimiter='\t', usecols=2, dtype=None)
#Mean_angles_to_zero =np.genfromtxt(directory + '/' + 'FTangles_and_anisotropy_all.txt', delimiter='\t', usecols=4, dtype=None)
#Rad_angles_to_x = np.deg2rad(angles_to_x)
#print angles_to_x
#print angles_to_x_90
#print anisotropies

print angles_to_x
print Rad_angles_to_x_pi
print Rad_angles_to_x_pi_X2

print str(samples)

print np.rad2deg(stats.circmean(Rad_angles_to_x_pi, high = np.pi, low = 0))
print np.rad2deg(stats.circstd(Rad_angles_to_x_pi, high = np.pi, low = 0))
print pycircstat.resultant_vector_length(np.array(Rad_angles_to_x_pi_X2))

pval, U, Uc = pycircstat.raospacing(np.array(Rad_angles_to_x_pi_X2))
print pval
print U
print Uc
if pval>0.05:
  print 'The populations IS uniformly distributed\np-value is ' + str(pval)
  fdata.write('Global results: ' + '\n' + 'Mean Angle to x (+-Std) --> ' + str(np.rad2deg(stats.circmean(Rad_angles_to_x_pi, high = np.pi, low = 0))) + '+-' + str(np.rad2deg(stats.circstd(Rad_angles_to_x_pi, high = np.pi, low = 0))) + ' degrees'+ '\n'+ 'Resultant_vector_length '+ str(pycircstat.resultant_vector_length(np.array(Rad_angles_to_x_pi_X2))) + '\n' + 'Mean Anisotropy (+-Std) --> ' + str(np.mean(anisotropies)) + '+-' + str(np.std(anisotropies))+ '\n'+'The populations IS uniformly distributed\np-value is ' + str(pval))
else:
  print 'The populations is NOT uniformly distributed\np-value is ' + str(pval)
  fdata.write('Global results: ' + '\n' + 'Mean Angle to x (+-Std) --> ' + str(np.rad2deg(stats.circmean(Rad_angles_to_x_pi, high = np.pi, low = 0))) + '+-' + str(np.rad2deg(stats.circstd(Rad_angles_to_x_pi, high = np.pi, low = 0))) + ' degrees'+ '\n'+ 'Resultant_vector_length '+ str(pycircstat.resultant_vector_length(np.array(Rad_angles_to_x_pi_X2))) + '\n' + 'Mean Anisotropy (+-Std) --> ' + str(np.mean(anisotropies)) + '+-' + str(np.std(anisotropies))+ '\n'+'The populations is NOT uniformly distributed\np-value is ' + str(pval))

fdata.close()

figure = plt.figure()
figure.clf()
n, bins, patches = plt.hist(all_angles_to_x,bins=([-90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]), normed=1, weights=anisotropies, facecolor='grey', alpha=0.75)
plt.xlabel('Angles(degree)', fontsize=24)
plt.ylabel('Frequency', fontsize=24)
plt.title('N=' + str(len(all_angles_to_x)) + ' cells in ' + str(samples) +' samples', fontsize=24)
plt.axis([-90, 90, 0, 0.03])
plt.grid(True)
#plt.show()
figure.savefig(directory+"/"+"Batch_FT_hist.jpg")
figure.savefig(directory+"/"+"Batch_FT_hist.pdf")



figure = plt.figure()
figure.clf()
figure.patch.set_facecolor('k')
ax = figure.add_subplot(111,polar=True)

colormap = "plasma"
n_bins = 36

for offset in [0, np.pi]:
    histo, bins, patches = figure.gca().hist(offset+all_angles_to_x*np.pi/180,bins=offset+np.linspace(-90,90,n_bins/2 + 1)*np.pi/180.,ec='k',weights=anisotropies)
    norm = colors.Normalize(0,histo.max())
    for h, p in zip(histo, patches):
        p.set_facecolor(cm.get_cmap(colormap)(norm(h)))
figure.gca().set_yticks([])

#plt.show()

figure.savefig(directory+"/"+"Batch_FT_polarhist.jpg")
figure.savefig(directory+"/"+"Batch_FT_polarhist.pdf")




