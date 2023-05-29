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

def generate_pattern(comb,p):
    string = format(comb, '0' + str(p) + 'b')
    pattern = set({})
    for period in range(len(string)):
        if string[period] == '1':
            pattern.add(period+1)
    return pattern

def read_input(filename,n,z,deviations,patterns):
    # Import the file containing the instance specified by Pirkwieser and Raidl
    all_lines = []
    with open('Benchmarks/'+filename+'.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split()
            int_values = [int(val) if val.isdigit() else float(val) for val in values]
            all_lines.append(int_values)
    
    # Store the numer of periods and information associated with the fleet of available delivery vehicles
    p = all_lines[0][3]
    fleet = Fleet(1, [0], [all_lines[1][1]], [1], [1], [0], [all_lines[0][1]])
    
    # Store the coordinates, service time durations, and demand volumes associated with customers in the original instance specified by Pirkwieser and Raidl
    x = {i:all_lines[1+p+i][1] for i in range(n+1)}
    y = {i:all_lines[1+p+i][2] for i in range(n+1)}
    s = {i:all_lines[1+p+i][3] for i in range(n+1)}
    q = {i:all_lines[1+p+i][4] for i in range(n+1)}
    
    # If z = 0, then the instance corresponds to the original instance specified by Pirkwieser and Raidl, otherwise a new instance with varying demand volumes and possible visitation patterns are specified
    if z != 0:
        # Set the seed according to the data set number z specified (z = 0 corresponds to the original instance specified by Pirkwieser and Raidl)
        rnd.seed(z)
        
        # The demand volumes associated with customers are changed. The deviations are either small or large.
        if deviations == 'Small':
            for i in range(1,n+1):
                q[i] = max([0,q[i]+rnd.normal()*q[i]/6])
        elif deviations == 'Large':
            for i in range(1,n+1):
                q[i] = max([0,q[i]+rnd.normal()*q[i]/3])
        
        # The list of allowable visitation patterns associated with customers are either changed or fixed as those specified in the original instance by Pirkwieser and Raidl
        f = {}
        pi = {}
        if patterns == 'Fixed':
            f = {i:all_lines[1+p+i][5] for i in range(n+1)}
            pos = {i:all_lines[1+p+i][6] for i in range(n+1)}
            pi = {i:[] for i in range(n+1)}
            temp_pi = {i:[all_lines[1+p+i][7+j] for j in range(pos[i])] for i in range(n+1)}
            for i in temp_pi:
                for comb in temp_pi[i]:
                    pi[i].append(generate_pattern(comb,p))
        elif patterns == 'Changed':
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
        # Store the number of visits and list of allowable visitation patterns associated with each customer
        f = {i:all_lines[1+p+i][5] for i in range(n+1)}
        pos = {i:all_lines[1+p+i][6] for i in range(n+1)}
        pi = {i:[] for i in range(n+1)}
        temp_pi = {i:[all_lines[1+p+i][7+j] for j in range(pos[i])] for i in range(n+1)}
        for i in temp_pi:
            for comb in temp_pi[i]:
                pi[i].append(generate_pattern(comb,p))
    
    # Read the time-window start and end times
    a = {i:all_lines[1+p+i][-2] for i in range(n+1)}
    b = {i:all_lines[1+p+i][-1] for i in range(n+1)}
    
    # Each customer is allowed to be visited by each type of delivery vehicle (there are only one type of delivery vehicle)
    g = {i:set({1}) for i in range(1,n+1)}
    
    # Store the locations of customers and calculate travel distance and time as the Euclidean distance
    locations = {'x':x, 'y':y}
    d = {(i,j):math.hypot(locations['x'][i]-locations['x'][j],locations['y'][i]-locations['y'][j]) for i in range(n+1) for j in range(n+1)}
    t = d
    
    # The demand volume to be delivered each customer is multiplied its number of visits and then by a factor of 2 (so that routes may be constrained by their loads as well as their time-windows)
    q = {i:min(q[i]*f[i]*2,all_lines[1][1]*f[i]) for i in range(1,n+1)}
    
    # Save the instance as a Problem_Instance class
    return Problem_Instance(n,p,fleet,f,pi,g,q,s,locations,d,t,a,b)


# Example:
instance = read_input(filename = 'p4c101', n = 25, z = 1, deviations = 'Large', patterns = 'Changed')

