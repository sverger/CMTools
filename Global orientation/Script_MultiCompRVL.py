import numpy as np
import pandas as pd
import os
import pycircstat
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.patheffects as patheffects



###Directory containing all the data to analyse and compare
updir = '/home/verger/Research/Image_analysis/Papier_qua1_mechastress/Multicomp_Hypo_qua1MBD/'


####Output file for all images of one condition
fdata = open(updir + '/' + 'Multi_Comparaison_of_CMT_Resultat_vector_length_Summary.txt', 'w')
fdata.write('Global output: '+ '\n')
###Generate RVL data for each condition and mutants compared
drnames = []
RVLdata = []
RVLdata_ = {}
Rad_angle_pi_X2_ = {}
fig=1
###Find subdirectories containing the experiments/conditions to analyse
for dirname in sorted(os.listdir(updir)):
  drpath = updir + dirname
  if os.path.isdir(drpath):
    #print dirname
    RVLdata_[dirname] = []
    drnames.append(dirname)
    for files in sorted(os.listdir(drpath)):
      if "_Log.txt" in files:
        #print 'file analyzed: ' + files
        imgpath=drpath + '/' + files
        #print 'image path: ' + imgpath
        Rad_angle_pi_X2_[files]=[]
        DegAngles = np.genfromtxt(imgpath, delimiter='\t', usecols=5, dtype=None)
        RadAngles = np.deg2rad(DegAngles)
        #print RadAngles
        for a in RadAngles:
          if a<0:
            a = a+(np.pi)
          b = a*2
          Rad_angle_pi_X2_[files].append(b)
        #print Rad_angle_pi_X2_[files]
        RVL = pycircstat.resultant_vector_length(np.array(Rad_angle_pi_X2_[files]))
        #fdata.write('Sample analysed: '+ imgpath +'\n' + 'Resultant vector length --> ' + str(RVL) + '\n'+ '\n')


        RVLdata_[dirname].append(RVL)
        #RVLdata.append(RVL)
        
    print str(dirname)+ ' :' + str(RVLdata_[dirname])
    RVLdata.append(RVLdata_[dirname])
    fdata.write('Mean RVL' + str(dirname) + '(+-Std) --> ' + str(np.mean(RVLdata_[dirname])) + '+-' + str(np.std(RVLdata_[dirname]))+ '\n')


###Comparaisons
sampleA = ['MBD_1%', 'MBD_1%', 'MBD_1%', 'MBD_2,5%', 'MBD_2,5%', 'qua1MBD_1%']
sampleB = ['MBD_2,5%', 'qua1MBD_1%', 'qua1MBD_2,5%', 'qua1MBD_1%', 'qua1MBD_2,5%', 'qua1MBD_2,5%']



for A, B in zip(sampleA, sampleB):
    fdata.write('\n' + A + ' is sample A'+ '\n' + B + ' is sample B'+'\n')
    fdata.write('RVL comparaison'+'\n')
    fdata.write(str(np.mean(RVLdata_[A])) + '+-' + str(np.std(RVLdata_[A]))+'\n')
    fdata.write(str(np.mean(RVLdata_[B])) + '+-' + str(np.std(RVLdata_[B]))+'\n')
    print 'means'
    
    ###T-test
    pops=[]
    pops.append(RVLdata_[A])
    pops.append(RVLdata_[B])
    ###Shapiro's test for normality for sample A
    w, pnormA = stats.shapiro(np.array(RVLdata_[A]))
    if pnormA>0.05:
      normA = True
      print 'A sample IS normally distributed'
      fdata.write('A sample IS normally distributed'+'\n')
    else:
      normA = False
      print 'A sample is NOT normally distributed'
      fdata.write('A sample is NOT normally distributed'+'\n')
    ###Shapiro's test for normality for sample B
    w, pnormB = stats.shapiro(np.array(RVLdata_[B]))
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
ax = plt.boxplot(RVLdata, labels=drnames, widths= 0.7, patch_artist=True)
plt.tight_layout()
plt.show()
figure.savefig(updir+"/"+"RVLs.pdf")