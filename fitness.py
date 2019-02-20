# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 13:02:42 2018

@author: Imaris
"""

import pandas
import math

base = []
excel = pandas.read_excel('data.xls')

for index, row in excel.iterrows():
    if index == 24:
        for x in row:
            if type(x) == float:
                base.append(0.8 * x)
            else:
                base.append(x)

distance = []

for index, row in excel.iterrows():
    dist = 0
    for x in range(1,9):
        dist += pow(row[x] - base[x], 2)
    distance.append(math.sqrt(dist))

print (distance)