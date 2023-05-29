#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:30:52 2023

@author: jacobusking
"""
from Classes import Fleet, Problem_Instance
import numpy as np
rnd = np.random
import math

rnd.normal()

def generate_pattern(comb,p):
    string = format(comb, '0' + str(p) + 'b')
    pattern = set({})
    for period in range(len(string)):
        if string[period] == '1':
            #if period<p:
            pattern.add(period+1)
    return pattern

def read_input(filename,n,z):
    all_lines = []
    with open('Recycling/Benchmarks/'+filename+'.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split()
            int_values = [int(val) if val.isdigit() else float(val) for val in values]
            all_lines.append(int_values)
    
    #n = all_lines[0][2]
    p = all_lines[0][3]
    fleet = Fleet(1, [0], [all_lines[1][1]], [1], [1], [0], [all_lines[0][1]])
    
    x = {i:all_lines[1+p+i][1] for i in range(n+1)}
    y = {i:all_lines[1+p+i][2] for i in range(n+1)}
    s = {i:all_lines[1+p+i][3] for i in range(n+1)}
    q = {i:all_lines[1+p+i][4] for i in range(n+1)}
    if z != 0:
        rnd.seed(z)
        for i in range(1,n+1):
            q[i] = max([0,q[i]+rnd.normal()*q[i]/6]) 
        f = {}
        pi = {}
        for i in range(1,n+1):
            random = rnd.random()
            if random <= 1/3:
                f[i] = 1
                pi[i] = [set({1}), set({2}), set({3}), set({4})]
            elif random <= 2/3:
                f[i] = 2
                pi[i] = [set({1,3}), set({2,4})]
            else:
                f[i] = 4
                pi[i] = [set({1,2,3,4})]
    else:    
        f = {i:all_lines[1+p+i][5] for i in range(n+1)}
        pos = {i:all_lines[1+p+i][6] for i in range(n+1)}
        pi = {i:[] for i in range(n+1)}
        temp_pi = {i:[all_lines[1+p+i][7+j] for j in range(pos[i])] for i in range(n+1)}
        for i in temp_pi:
            for comb in temp_pi[i]:
                pi[i].append(generate_pattern(comb,p))
            
    a = {i:all_lines[1+p+i][-2] for i in range(n+1)}
    b = {i:all_lines[1+p+i][-1] for i in range(n+1)}
    
    g = {i:set({1}) for i in range(1,n+1)}
    locations = {'x':x, 'y':y}
    d = {(i,j):math.hypot(locations['x'][i]-locations['x'][j],locations['y'][i]-locations['y'][j]) for i in range(n+1) for j in range(n+1)}
    t = d
    q = {i:min(q[i]*f[i]*2,all_lines[1][1]*f[i]) for i in range(1,n+1)}
    
    return Problem_Instance(n,p,fleet,f,pi,g,q,s,locations,d,t,a,b)






