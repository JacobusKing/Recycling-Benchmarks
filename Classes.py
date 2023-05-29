#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:06:00 2023

@author: jacobusking
"""


class Problem_Instance():
    def __init__(self,n,p,fleet,f,pi,g,q,s,locations,d,t,a,b):
        self.n = n
        self.p = p
        self.fleet = fleet
        self.nodes = range(0,n+1)
        self.customers = range(1,n+1)
        self.periods = range(1,p+1)
        self.pairs = [(i,j) for j in self.periods for i in self.fleet.vehicle_types]
        self.f = f
        self.pi = pi
        self.g = g
        self.q = q
        self.s = s
        self.locations = locations
        self.d = d
        self.t = t
        self.a = a
        self.b = b

class Fleet():
    '''
    The collection of all vehicles available to serve customers
    '''
    def __init__(self, nu_vehicle_types, C, Q, cost_coef, time_coef, B, K):        
        vehicle_types = {}
        vehicle_type_counter = 0
        for i in range(nu_vehicle_types):
            vehicle_type_counter += 1
            vehicle_types[vehicle_type_counter] = Vehicle_Type(C[i], Q[i], cost_coef[i], time_coef[i], B[i], K[i])
        self.vehicle_types = vehicle_types
        self.nu_vehicle_types = nu_vehicle_types
        self.K = K
        
class Vehicle_Type():
    '''
    Stores information about each vehicle available to serve customers
    '''
    def __init__(self, C, Q, cost_coef, time_coef, B, K):
        self.C = C #Fixed cost of using the vehicle
        self.Q = Q #Capacity of the vehicle
        self.cost_coef = cost_coef
        self.time_coef = time_coef
        self.B = B
        self.K = K
