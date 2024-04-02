#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:08:57 2024

@author: Dylan Agius

This class runs the calculation multiple times, allowing for the random selection
from the distributions to occur many times. Then the average of these values are calculated
"""
import numpy as np
from itercalc import itercalc

class runner:
    def __init__(self,data):
        self.totaldrinks=[] #store
        self.itrange=1000 #number of iterations to occur from which the average is calculated
        self.data=data
    def loop(self):
        for i in range(self.itrange):
            drinks=itercalc(self.data).totalcalc()
            self.totaldrinks.append(drinks)
        
        return np.mean(self.totaldrinks)


