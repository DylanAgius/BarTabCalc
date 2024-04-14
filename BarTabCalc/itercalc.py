#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 08:20:45 2023

@author: Dylan Agius


"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

import random as random
import pandas as pd


"""
This  determines the number of cost for given information.
The drinks per hour for each gender is determine by applying a normal distribution.

Things to improve:
*Also need to have all drinks together then have higher probabiliy for men and women.

"""

class itercalc:
      
    def __init__(self,data):
        
       
        #extract event info
        self.num_guests=int(data['num_guests'].dropna())
        self.percent_drive=float(data['percent_drive'].dropna())
        self.num_hours=int(data['num_hours'].dropna())
        self.drinkprice=np.array(data['drinkprice'])
        self.weekday=data['school_night'].dropna().item()
        self.percent_female=float(data['percent_female'].dropna())
        
        self.formdist()
        #calulate split of female and male drivers/nondrivers
        self.driveorno()
        self.randomsample() #create arrays of random values to be used in array sampling
        self.timearrays() #create time array for decay of drinking rate as hours progress
        self.hourlydrinks() #calculate hourly drinks for drivers and drinkers including rate decay
        self.drink_price_selection()
        

        
        
           
        
    def formdist(self):
        """
        Calculate distributions for female and male drinks for the selection of 
        number of drinks per hour
        """
        if self.weekday=='no':
            maxdrinkmale=5; maxdrinkfemale=3;
        else:
            maxdrinkmale=3; maxdrinkfemale=2;
        
        #distribution for males
        lower, upper = 0, maxdrinkmale
        mu, sigma = 2, (maxdrinkmale-0)/4
        XY = stats.truncnorm(
            (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs(1000)
        
        #distribution for females
        lowerf, upperf = 0, maxdrinkfemale
        muf, sigmaf = 1, (maxdrinkfemale-0)/4
        XX= stats.truncnorm(
            (lowerf - muf) / sigmaf, (upperf - muf) / sigmaf, loc=muf, scale=sigmaf).rvs(1000)
        
        
        self.XX_drinks_per_hour_dist=XX; self.XY_drinks_per_hour_dist=XY
    
    
    def randomsample(self):
        """
        Creates arrays using random numbers to samplefrom the 'drink per hour array' in formdist()
        and the drinkprice array
        """
        #make an random selection array for drink selection and drinks per hour from the drinkprice array
        self.XX_drink_select=np.random.randint(np.size(self.drinkprice),size=(self.XX_nondrive,self.num_hours)).flatten('F')
        self.XY_drink_select=np.random.randint(np.size(self.drinkprice),size=(self.XY_nondrive,self.num_hours)).flatten('F')
    
        #create an array used to sample from the distributions formed by formdist()
        self.XX_drink_per_hour=np.random.randint(1000,size=(self.XX_nondrive,self.num_hours)).flatten('F')
        self.XY_drink_per_hour=np.random.randint(1000,size=(self.XY_nondrive,self.num_hours)).flatten('F')
    
        #drink selection for drivers
        self.XX_drink_selection_drive=np.random.randint(np.size(self.drinkprice),size=(self.XX_drive,self.num_hours)).flatten('F')
        self.XY_drink_selection_drive=np.random.randint(np.size(self.drinkprice),size=(self.XY_drive,self.num_hours)).flatten('F')
       
    
    def driveorno(self):
        """
        Calculate the number of drivers and non drivers then split into genders
        """
        
        # Calculate the number of guests who do not drive
        num_drivers=int(self.num_guests*self.percent_drive)
        num_nondrivers=self.num_guests-num_drivers
        
        
        #split this into male and female
        self.XX_nondrive=int(num_nondrivers*self.percent_female)
        self.XY_nondrive=int(num_nondrivers-int(num_nondrivers*self.percent_female))
        
        self.XX_drive=int(num_drivers*self.percent_drive)
        self.XY_drive=int(num_drivers-num_drivers*self.percent_drive)
        
       
    
    def timearrays(self):
        """
        Create time arrays to allow for exponential decay
        """
        
        #creating a time array for drivers. Note: 2 arrays required for different numbers of females and males
        self.XX_t_drive=np.array(([np.arange(0,self.num_hours)]*self.XX_drive)).flatten('F')
        self.XY_t_drive=np.array(([np.arange(0,self.num_hours)]*self.XY_drive)).flatten('F')
        
        
        #creating a time array for drinkers.  Note: 2 arrays required for different numbers of females and males
        self.XX_t_drink=np.array(([np.arange(0,self.num_hours)]*int(np.size(self.XX_drink_per_hour,axis=0)/self.num_hours))).flatten('F')
        self.XY_t_drink=np.array(([np.arange(0,self.num_hours)]*int(np.size(self.XY_drink_per_hour,axis=0)/self.num_hours))).flatten('F')
        
       
        
    def hourlydrinks(self):
        """
        Add a decay to the number of drinks per hour.
        This attempts to recognise that people will slow their drinking as the event
        progresses
        """
 
        #Use randomly selected drinks per hour to extract the hourly drinks for males and females
        self.XY_hourlydrinks_drink_decay=np.exp(-0.4*self.XY_t_drink)*np.array(self.XY_drinks_per_hour_dist[self.XY_drink_select])
        self.XX_hourlydrinks_drink_decay=np.exp(-0.4*self.XX_t_drink)*np.array(self.XX_drinks_per_hour_dist[self.XX_drink_select])
        

        #for the people who are driving, we will assume 1 drink per hour for women and 2 in first hour
        #then 1 per hour for men
      
        hour1_drive_male=np.array([1]*self.XY_drive)[:,None]
        hourrest_male=np.array([[1]*(self.num_hours-1)]*self.XY_drive)
        XY_hourlydrinks_drive=np.hstack((hour1_drive_male,hourrest_male)).flatten('F')
        XX_hourlydrinks_drive=np.array([[1]*(self.num_hours)]*self.XX_drive).flatten('F')

        #add 'F' inside flatten bracket. need to add time which can be used in the decay.
        self.XX_hourlydrinks_drive_decay=np.exp(-0.4*self.XX_t_drive)*XX_hourlydrinks_drive
        self.XY_hourlydrinks_drive_decay=np.exp(-0.4*self.XY_t_drive)*XY_hourlydrinks_drive
  
    
    def drink_price_selection(self):
        """
        Lets randomly select drinks and create an array
        """
    
       
        #random selection of drink prices for male and female
        self.XY_drinks_prices_drink=self.drinkprice[self.XY_drink_select]
        self.XX_drinks_prices_drink=self.drinkprice[self.XX_drink_select]
        
        
        self.XY_drinks_prices_drive=self.drinkprice[self.XY_drink_selection_drive]
        self.XX_drinks_prices_drive=self.drinkprice[self.XX_drink_selection_drive]
        


    def totalcalc(self):
        """
        This function takes the array of decaying time, drink selection, number of drivers to 
        calculate the total cost
        """
     
        
        #flatten arrays and mulitply by average drink price
        total_drinks_malesnd =sum(self.XY_hourlydrinks_drink_decay*self.XY_drinks_prices_drink)
        total_drinks_femalesnd=sum(self.XX_hourlydrinks_drink_decay*self.XX_drinks_prices_drink)
        
        total_drinks_malesd =sum(self.XY_hourlydrinks_drive_decay*self.XY_drinks_prices_drive)
        total_drinks_femalesd=sum(self.XX_hourlydrinks_drive_decay*self.XX_drinks_prices_drive)
        
        
        # Calculate the total cost of the bar tab
        total_cost =total_drinks_malesnd +total_drinks_malesd + total_drinks_femalesnd + total_drinks_femalesd  
       
        return total_cost

if __name__ == "__main__":
    
    #need to add the ability to read in the information maybe from a file
    
    totaldrinks=[]
    for i in range(1000):
        
        drinks=itercalc().totalcalc()
        totaldrinks.append(drinks)
            
    average=np.mean(totaldrinks)
    
    print("Total cost: $" + str(average))




