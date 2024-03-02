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

Things to improve:
*Also need to have all drinks together then have higher probabiliy for men and women.

"""

def drinkcalc():
    
    #specify weekend or weekday event. This alters the drinks per hour for each distribution
    weekday='yes'
    
    if weekday=='no':
        maxdrinkmale=5; maxdrinkfemale=3;
    else:
        maxdrinkmale=3; maxdrinkfemale=2;
    
    #distribution for males
    lower, upper = 0, maxdrinkmale
    mu, sigma = 2, (maxdrinkmale-0)/4
    X = stats.truncnorm(
        (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs(1000)
    
    #distribution for females
    lowerf, upperf = 0, maxdrinkfemale
    muf, sigmaf = 1, (maxdrinkfemale-0)/4
    Xf= stats.truncnorm(
        (lowerf - muf) / sigmaf, (upperf - muf) / sigmaf, loc=muf, scale=sigmaf).rvs(1000)
    
    # Initialize variables for the number of guests, the percentage of guests who drive,
    # the percentage of females attending, number of hours of the event
    num_guests = 34
    percent_drive = 0.7
    percent_female= 0.6
    num_hours=1
    
    #drinks prices for each gender
    maledrinks=np.array([7,8.50,7])
    femaledrinks=np.array([7,8.50,7,15,12])
        
   
    # Calculate the number of guests who do not drive
    num_nondrivers = num_guests - (num_guests * percent_drive)
    num_drivers=num_guests-int(num_nondrivers)
  
 

    #make an random selection array fordrink selection and drinks per hour
    female_drink_selection=np.random.randint(np.size(femaledrinks),size=(int(num_nondrivers*percent_female),num_hours))
    male_drink_selection=np.random.randint(np.size(maledrinks),size=(int(num_nondrivers-int(num_nondrivers*percent_female)),num_hours))
    
   
    
    selectionsfemale=np.random.randint(1000,size=(int(num_nondrivers*percent_female),num_hours))
    selectionsmale=np.random.randint(1000,size=(int(num_nondrivers-int(num_nondrivers*percent_female)),num_hours))
    
  
    
    #creating a time array for the exponential decay
    timefd=np.array(([np.arange(0,num_hours)]*np.size(selectionsfemale,axis=0)))
    timemd=np.array(([np.arange(0,num_hours)]*np.size(selectionsmale,axis=0)))
    
    #Use randomly selected drinks per hour to extract the hourly drinks for males and females
    hourlydrinksmale=np.exp(-0.4*timemd.flatten('F'))*X[selectionsmale].flatten('F')
    hourlydrinksfemale=np.exp(-0.4*timefd.flatten('F'))*Xf[selectionsfemale].flatten('F')
    
    
    #for the people who are driving, we will assume 1 drink per hour for women and 2 in first hour
    #then 1 per hour for men
    ndrivef=int(num_drivers*percent_female)
    ndrivem=num_drivers-ndrivef
    hour1_drive_male=np.array([1]*ndrivem)[:,None]
    hourrest_male=np.array([[1]*(num_hours-1)]*ndrivem)
    hourlydrinksdrivemen=np.hstack((hour1_drive_male,hourrest_male))
    
    hourlydrinksdrivefemale=np.array([[1]*(num_hours)]*ndrivef)
    
    #now adding an exponential decay
    #creating a time array for the exponential decay
    timef=np.array(([np.arange(0,num_hours)]*ndrivef))
    timem=np.array(([np.arange(0,num_hours)]*ndrivem))
    
    #add 'F' inside flatten bracket. need to add time which can be used in the decay.
    hourlydrinksdrivefemale=np.exp(-0.4*timef.flatten('F'))*hourlydrinksdrivefemale.flatten('F')
    hourlydrinksdrivemen=np.exp(-0.4*timem.flatten('F'))*hourlydrinksdrivemen.flatten('F')
    
    #drink selection for drivers
    female_drink_selectiond=np.random.randint(np.size(femaledrinks),size=(ndrivef,num_hours))
    male_drink_selectiond=np.random.randint(np.size(maledrinks),size=(ndrivem,num_hours))
    
   
    #random selection of drink prices for male and female
    male_drinks_prices=maledrinks[male_drink_selection]
    female_drinks_prices=femaledrinks[female_drink_selection]
    
    male_drinks_pricesd=maledrinks[male_drink_selectiond]
    female_drinks_pricesd=femaledrinks[female_drink_selectiond]
    
    #flatten arrays and mulitply by average drink price
    total_drinks_malesnd =sum(hourlydrinksmale*male_drinks_prices.flatten())
    total_drinks_femalesnd=sum(hourlydrinksfemale*female_drinks_prices.flatten())
    
    total_drinks_malesd =sum(hourlydrinksdrivemen*male_drinks_pricesd.flatten())
    total_drinks_femalesd=sum(hourlydrinksdrivefemale*female_drinks_pricesd.flatten())
    
    
    # Calculate the total cost of the bar tab
    total_cost =total_drinks_malesnd +total_drinks_malesd + total_drinks_femalesnd + total_drinks_femalesd  
    
    
    # Print the total cost
    ##print("Total cost: $" + str(total_cost))
    return total_cost


    
totaldrinks=[]
for i in range(1000):
    drinks=drinkcalc()
    totaldrinks.append(drinks)
        
average=np.mean(totaldrinks)

print("Total cost: $" + str(average))




