# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:40:55 2018

@author: Imaris
"""

import itertools
import os
import random
import heapq
from collections import Counter
#==============================================================================
#create population
num_population = 100

names_list=['Ip0','gLs','gLd','gNa','gKdr','gCa','gKahp', 'gKC','VNa','VCa',   
            'VK', 'VL',  'gc','pp', 'Cm']

#'Vsyn', 'vtsyn', these equal 0 so don't inculde them?

i = 0
j = 0
while i < num_population:
    all_target_combo = random.sample(names_list, 3)
    with open("oldOriginal_k.py","r") as f:
        zed=f.readlines()
    
    checked = []
    nomen=[]
    file_name = "oldOriginal" + str(i) + ".py"
    for combos in all_target_combo:
        for nn,name in enumerate(names_list):
            for ln,line in enumerate(zed):
                if not('=' in line):
                    continue
                parse=line.split('=')
                after=line.find('*')
                if combos == parse[0] and combos not in checked:
                    parse2 = parse[1].split('*', 1)
                    if random.random() < 0.5:
                        nomen.append(combos + " 1.1")
                        num = float(parse2[0]) * 1.1
                        num = round(num, 1)
                    else:
                        nomen.append(combos + " 0.9")
                        num = float(parse2[0]) * 0.9
                        num = round(num, 1)
                    line=combos+'='+str(num) + line[after:]
                    zed[ln]=line
                    checked.append(combos)
        zed[-1]= '\n'+ '#' +  str(nomen)
    
        with open(file_name,'w') as f:
            f.writelines(zed)
    i += 1
#==============================================================================
#calc initial fitness

def fit_list():
    j = 0
    fit_list = [0] * (num_population)
    while j < num_population:
        fit_list[j] = random.randint(0,99)
        j+= 1
    #print(fit_list)
    return(fit_list)        
#print(fit_list)
        


def fit_list_2():
    j = 0
    fit_list = [0] * (num_population)
    while j < num_population:
        fit_list[j] = random.randint(0,99)
        j+= 1
    #print(fit_list)
    return(fit_list)
#==============================================================================
#get list of top 10 most fit and bottom 55 least fit 

def lists(fit_list):
    a = []
    j = 0
    fittest = heapq.nlargest(10, enumerate(fit_list), key=lambda x:x[1])
    #print(fittest)
    while j < 10:
        a.append(fittest[j][0])
        j += 1
    #print(a)
    b = []
    k = 0
    smallest = heapq.nsmallest(55, enumerate(fit_list), key=lambda x:x[1])
    #print(smallest)
    while k < 55:
        b.append(smallest[k][0])
        k += 1
    #print (b)
    return(a,b)
#============================================================================== 
#turn these things into functions so i can make a while loop like before and call everything there.

def change(file):
    file_name = "oldOriginal" + str(file) + ".py"
    with open(file_name, "r") as f1:
        for i, line in enumerate(f1):
            if i == 597:
                changes1 = line[2:-1]
        changes1 = changes1.replace("'", "")
        changes1 = changes1.split(",")
    return(changes1)

#==============================================================================
    
def fifty_fifty(changes1):
    #print('change1: ', change1)
    changes3 = {}
    for x in changes1:
        if x != '':
            if random.random() < 0.5:
                x = x.split(" ")
                if x[0] == '':
                    changes3[x[1]] = float(x[2])
                else:
                    changes3[x[0]] = float(x[1])
    return(changes3)

#==============================================================================

def fifty_fifty_pt2(changes2, changes3):
    #print('change2: ', change2)
    for x in changes2:
        if x != '':
            if random.random() < 0.5:
                x = x.split(" ")
                if x[0] == '':
                    if x[1] in changes3:
                        z1 = 1 + (float(x[2]) - 1) + (changes3[x[1]] - 1)
                        #print ('x: ', x[2], 'change: ', changes3[x[1]], 'z: ', z1)
                        changes3[x[1]] = z1
                    else:
                        changes3[x[1]] = float(x[2])
                else:
                    if x[0] in changes3:
                        z1 = 1 + (float(x[1]) - 1) + (changes3[x[0]] - 1)
                        #print ('x: ', x[1], 'change: ', changes3[x[0]], 'z: ', z1)
                        changes3[x[0]] = z1
                    else:
                        changes3[x[0]] = float(x[1])
    #print('change3: ', change3)
    return(changes3)


#==============================================================================
#mutation
def mutation(changes3):
    for x in changes3:
        y = random.random()
        if y < .33:
            changes3[x] -= 0.1
        elif y > .66:
            changes3[x] += 0.1
        if len(str(changes3[x])) >= 3:
            z = str(changes3[x])[:3]
            changes3[x] = float(z)
    return(changes3)


#==============================================================================
#open least fit child and replace with new child   

def replace(m, changes3):
    with open("oldOriginal_k.py","r") as f:
            zad=f.readlines()

    nomen = []
    for x in changes3:
        nomen.append(x + ' '+ str(changes3[x]))
        #print(nomen)

    for ln,line in enumerate(zad):
        if not('=' in line):
            continue
        parse=line.split('=')
        after=line.find('*')
        if parse[0] in changes3:
            parse2 = parse[1].split('*', 1)
            #print('   ', parse[0], parse2[0], 'is gonna change')
            #print('   ', changes3[parse[0]])
            num = float(parse2[0]) * changes3[parse[0]] 
            #print('   ', num)
            line=parse[0]+'='+str(num) + line[after:]
        zad[ln]=line
    zad[-1]= '\n'+ '#' +  str(nomen)
    #print(nomen)

    file_nameA = "oldOriginal" + str(m) + ".py"
    with open(file_nameA,'w') as f:
        f.writelines(zad)

#=============================================================================
#Convergence

def convergence():
    conv = .9 * num_population
    count = 0
    converge = []
    while count < num_population:
        file = "oldOriginal" + str(count) + ".py"
        with open(file,"r") as f:
            zud=f.readlines()
            
        for ln, line in enumerate(zud):
            if ln == 597:
                converge.append(line)
        count += 1
    a = dict(Counter(converge))
    for x in a:
        #print(a[x])
        if a[x] >= conv:
            return 1
    return 0

#==============================================================================
#main while loop
generation = 0
max_generation = 100
fittest = 0
fit_list = fit_list()
fittest = max(fit_list)
file = fit_list.index(fittest)
converge = 0
changes = {}
for x in range(0,100):
    changes[x] = 0
    
print('Generation : ', generation, 'file: ', file,'fittest: ', fittest)
while generation < max_generation and fittest != 100 and converge == 0:
    generation += 1
    #get list of fittest and lest fit individuals
    a,b = lists(fit_list)
    
    
    count = 0
    #make children
    for x in range(0, len(a) - 1):
        for y in range(x + 1, len(a)):
            change1 = change(a[x])
            change2 = change(a[y])
            
            change3 = fifty_fifty(change1)
            change3 = fifty_fifty_pt2(change2, change3)
            change3 = mutation(change3)
            #print(change3)
            replace(b[count],change3)
            count += 1
            #print('a[x]: ', a[x], 'a[y]: ', a[y], ' b[count]: ', b[count])
            changes[b[count]] += 1
    #print(changes)
    
    converge = convergence()
    #recalculate fitness      
    fit_list = fit_list_2()
    fittest = max(fit_list)
    file = fit_list.index(fittest)
    print('Generation : ', generation, 'file: ', file,'fittest: ', fittest)
    
#==============================================================================
if fittest == 100:
    print('Solution found in generation ', generation)
    print('Fittest ', fittest)
    print('file: ', file)
elif converge == 1:
    print('population is converging in ', generation, 'generations')
    print('Fittest ', fittest)
    print('file: ', file)
else:
    print('No Solution found in ', generation,' generations')
    print('Fittest ', fittest)
    print('file: ', file)

    
    
    
    
    
    
    
    
    
    
    
    
    




