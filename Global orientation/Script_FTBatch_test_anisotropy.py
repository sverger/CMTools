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
fdata = open(updir + '/' + 'Comparaison_of_CMT_Anisotropy_Summary.txt', 'w')

#Wildtype or control condition contains in name:
WT_CTRL = "1%"

#Mutant or tested condition contains in name:
Mut_Cond = "2,5%"

###For each image in the directory
for files in sorted(os.listdir(updir)):
  if "_all.txt" in files:
    print 'file analyzed: ' + files
    imgpath=updir + '/' + files
    print 'image path: ' + imgpath
    Anisotropy = np.genfromtxt(imgpath, delimiter='\t', usecols=2, dtype=None)
    fdata.write('Sample analysed: '+ imgpath +'\n' + 'Mean anisotropy (+-Std)--> ' + str(np.mean(Anisotropy)) + '+-' + str(np.std(Anisotropy)) + '\n'+ '\n')

    if Mut_Cond in files:
      #print 'mutant'
      mutant_ani = np.array(Anisotropy)

    elif WT_CTRL in files:
      #print "control"
      WT_ani = np.array(Anisotropy)
      

print 'WT/Ctrl: ' + str(WT_ani)
print 'mutant/condition: ' + str(mutant_ani)
fdata.write('Global output: '+ '\n' + 'Mean anisotropy WT/Ctrl (+-Std) --> ' + str(np.mean(WT_ani)) + '+-' + str(np.std(WT_ani))+ '\n')
fdata.write('Mean anisotropy mutant/condition (+-Std) --> ' + str(np.mean(mutant_ani)) + '+-' + str(np.std(mutant_ani))+ '\n')



###T-test
pops=[]
pops.append(WT_ani)
pops.append(mutant_ani)
###Shapiro's test for normality for coty
w, pnormWT_CTRL = stats.shapiro(WT_ani)
if pnormWT_CTRL>0.05:
  normWT_CTRL = True
  print 'WT/Ctrl sample IS normally distributed'
  fdata.write('WT/Ctrl sample IS normally distributed'+'\n')
else:
  normWT_CTRL = False
  print 'WT/Ctrl sample is Not normally distributed'
  fdata.write('WT/Ctrl sample is Not normally distributed'+'\n')
###Shapiro's test for normality for petiole
w, pnormMut_Cond = stats.shapiro(mutant_ani)
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
