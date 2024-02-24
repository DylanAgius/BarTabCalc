#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 08:20:45 2023

@author: dylanagius
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

import random as random



"""
This function determines the number of cost for given information.
The drinks per hour for each gender is determine by applying a normal distribution.

Things to improve: currently if you are driving, no drinks are calculated: this should be changed to 1 standard drink an hour
*The other improvement is the rate. There saturday drinking rates and sunday drinking rates.
*Also the the current drinks per hour is linear.  This should be exponential decay
"""

def drinkcalc():
    
    #distribution for males
    lower, upper = 0, 5
    mu, sigma = 2, (5-0)/4
    X = stats.truncnorm(
        (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs(1000)
    
    #distribution for females
    lowerf, upperf = 0, 3
    muf, sigmaf = 1, (3-0)/4
    Xf= stats.truncnorm(
        (lowerf - muf) / sigmaf, (upperf - muf) / sigmaf, loc=muf, scale=sigmaf).rvs(1000)
    
    # Initialize variables for the number of guests, the percentage of guests who drive,
    # the percentage of females attending, number of hours of the event
    num_guests = 32
    percent_drive = 0.1
    percent_female= 0.5
    num_hours=3
    
    #drinks prices for each gender
    maledrinks=np.array([7,8.50,7,6])
    femaledrinks=np.array([9,9,8,15,12])
        
    
    # Calculate the number of guests who do not drive
    num_nondrivers = num_guests - (num_guests * percent_drive)
    
 

    #make an random selection array fordrink selection and drinks per hour
    female_drink_selection=np.random.randint(np.size(femaledrinks),size=(int(num_nondrivers*percent_female),num_hours))
    male_drink_selection=np.random.randint(np.size(maledrinks),size=(int(num_nondrivers-int(num_nondrivers*percent_female)),num_hours))
    
    
    selectionsfemale=np.random.randint(1000,size=(int(num_nondrivers*percent_female),num_hours))
    selectionsmale=np.random.randint(1000,size=(int(num_nondrivers-int(num_nondrivers*percent_female)),num_hours))
    
    #Use randomly selected drinks per hour to extract the hourly drinks for males and females
    hourlydrinksmale=X[selectionsmale]
    hourlydrinksfemale=Xf[selectionsfemale]
    
    #random selection of drink prices for male and female
    male_drinks_prices=maledrinks[male_drink_selection]
    female_drinks_prices=femaledrinks[female_drink_selection]
    
    #flatten arrays and mulitply by average drink price
    total_drinks_males =sum(hourlydrinksmale.flatten().astype(int)*male_drinks_prices.flatten())
    total_drinks_females=sum(hourlydrinksfemale.flatten().astype(int)*female_drinks_prices.flatten())
    
    
    # Calculate the total cost of the bar tab
    total_cost =total_drinks_males + total_drinks_females
    
    
    # Print the total cost
    ##print("Total cost: $" + str(total_cost))
    return total_cost


    
totaldrinks=[]
for i in range(1000):
    drinks=drinkcalc()
    totaldrinks.append(drinks)
        
average=np.mean(totaldrinks)

print("Total cost: $" + str(average))




