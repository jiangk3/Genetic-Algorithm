# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:42:29 2018

@author: Imaris
"""
import os
import subprocess

z=subprocess.check_output('pscp -pw ghost lab@imaging-6:\\helloworld.txt "c:\\Users\\Imaris\\Desktop" ')
x=subprocess.check_output('plink -pw ghost lab@imaging-6: ls')
#c=subprocess.check_output('plink -pw ghost lab@imaging-6: cd music')
#plink(aka putty) comman ls to a specific directory.
#check if filder has 100 files
#file = os.system('pscp -pw ghost lab@imaging-6:')
#os.listdir(os.system('pscp -pw ghost lab@imaging-6:'))

#if there is 100 files, copy those files into variable.
#NEXT STEP PARSE X.
y = str(x)
y = y.split('\\n')    



#get list of files in a folder from linux server and put into python variable.
#pscp -pw ghost "C:\Users\Imaris\Desktop\helloworld.txt" lab@imaging-6:
#os echo ls plink
