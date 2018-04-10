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
updir = '/home/verger/Research/Image_analysis/Papier_qua1_mechastress/Coty_MBD_tests'


####Output file for all images of one condition
fdata = open(updir + '/' + 'Comparaison_of_CMT_Resultat_vector_spread_Summary.txt', 'w')

#Wildtype or control condition contains in name:
WT_CTRL = "1%"

#Mutant or tested condition contains in name:
Mut_Cond = "2,5%"

mutant_RVLs=[]
WT_RVLs=[]
Rad_angle_pi_X2_ = {}
###For each image in the directory
for files in sorted(os.listdir(updir)):
  if "_Log.txt" in files:
    print 'file analyzed: ' + files
    imgpath=updir + '/' + files
    print 'image path: ' + imgpath
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
    fdata.write('Sample analysed: '+ imgpath +'\n' + 'Resultant vector length --> ' + str(RVL) + '\n'+ '\n')

    if Mut_Cond in files:
      #print 'mutant'
      mutant_RVLs.append(RVL)

    elif WT_CTRL in files:
      #print "control"
      WT_RVLs.append(RVL)

print 'WT/Ctrl: ' + str(WT_RVLs)
print 'mutant/condition: ' + str(mutant_RVLs)
fdata.write('Global output: '+ '\n' + 'Mean RVL WT/Ctrl (+-Std) --> ' + str(np.mean(WT_RVLs)) + '+-' + str(np.std(WT_RVLs))+ '\n')
fdata.write('Mean RVL mutant/condition (+-Std) --> ' + str(np.mean(mutant_RVLs)) + '+-' + str(np.std(mutant_RVLs))+ '\n')

    
###T-test
pops=[]
pops.append(WT_RVLs)
pops.append(mutant_RVLs)
###Shapiro's test for normality for coty
w, pnormWT_CTRL = stats.shapiro(WT_RVLs)
if pnormWT_CTRL>0.05:
  normWT_CTRL = True
  print 'WT/Ctrl sample IS normally distributed'
  fdata.write('WT/Ctrl sample IS normally distributed'+'\n')
else:
  normWT_CTRL = False
  print 'WT/Ctrl sample is Not normally distributed'
  fdata.write('WT/Ctrl sample is Not normally distributed'+'\n')
###Shapiro's test for normality for petiole
w, pnormMut_Cond = stats.shapiro(mutant_RVLs)
if pnormMut_Cond>0.05:
  normMut_Cond = True
  print 'mutant/condition sample IS normally distributed'
  fdata.write('mutant/condition sample IS normally distributed'+'\n')
else:
  normMut_Cond = False
  print 'mutant/condition sample is NOT normally distributed'
  fdata.write('mutant/condition sample is NOT normally distributed'+'\n')
if normWT_CTRL and normMut_Cond is True:
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
  statrank, prank =stats.ranksums(*pops)
  if prank>0.05:
    print '-->populations are NOT statiscically different --> p-value is ' + str(prank)
    fdata.write('-->populations are NOT statiscically different --> p-value is ' + str(prank)+'\n'+'\n')
  else:
    print '-->populations are statiscically different --> p-value is ' + str(prank)
    fdata.write('-->populations are statiscically different --> p-value is ' + str(prank)+'\n'+'\n')
fdata.close()
