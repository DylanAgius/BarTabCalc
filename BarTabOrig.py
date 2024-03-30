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
import pandas as pd


"""
This function determines the number of cost for given information.
The drinks per hour for each gender is determine by applying a normal distribution.

Things to improve:
*Also need to have all drinks together then have higher probabiliy for men and women.

"""

def formdist(event_info,XX_data,XY_data):
    """
    Calculate distributions for female and male drinks for the selection of 
    number of drinks per hour
    """
    weekday=event_info['weekday'].dropna().item()
    if weekday=='no':
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
    
    
    XX_data['Drinks_per_hour_dist']=XX; XY_data['Drinks_per_hour_dist']=XY
    return XX_data,XY_data

def randomsample(event_info,XX_data,XY_data):
    """
    Creates arrays using random numbers to samplefrom the 'drink per hour array' in formdist()
    and the drinkprice array
    """
    #extract event info
    drinkprice=np.array(event_info['drinkprice'])
    num_hours=int(event_info['num_hours'].dropna().item())
    
    #extract XX and XY data
    XX_nondrive=int(XX_data['nondrivers'].dropna().item())
    XY_nondrive=int(XY_data['nondrivers'].dropna().item())
    
    #make an random selection array for drink selection and drinks per hour from the drinkprice array
    XX_drink_select=pd.DataFrame({'female_drink_selection':np.random.randint(np.size(drinkprice),size=(XX_nondrive,num_hours)).flatten('F')})
    XX_data=pd.concat([XX_data,XX_drink_select],axis=1)
    
    XY_drink_select=pd.DataFrame({'male_drink_selection':np.random.randint(np.size(drinkprice),size=(XY_nondrive,num_hours)).flatten('F')})
    XY_data=pd.concat([XY_data,XY_drink_select],axis=1)
   
    
    #create an array used to sample from the distributions formed by formdist()
    XX_drink_per_hour=pd.DataFrame({'female_drinks_per_hour_index':np.random.randint(1000,size=(XX_nondrive,num_hours)).flatten('F')})
    XX_data=pd.concat([XX_data,XX_drink_per_hour],axis=1)
                                    
    XY_drink_per_hour=pd.DataFrame({'male_drinks_per_hour_index':np.random.randint(1000,size=(XY_nondrive,num_hours)).flatten('F')})
    XY_data=pd.concat([XY_data,XY_drink_per_hour],axis=1)
    return XX_data,XY_data

def driveorno(event_info,XX_data,XY_data):
    """
    Calculate the number of drivers and non drivers then split into genders
    """
    # extract event info
    num_guests=event_info['num_guests'].dropna().item()
    percent_drive=event_info['percent_drive'].dropna().item()
    percent_female=event_info['percent_female'].dropna().item()
    
    # Calculate the number of guests who do not drive
    num_drivers=int(num_guests*percent_drive)
    num_nondrivers=num_guests-num_drivers
    
    
    #split this into male and female
    XX_nondrive=pd.DataFrame({'nondrivers':[int(num_nondrivers*percent_female)]})
    XY_nondrive=pd.DataFrame({'nondrivers':[int(num_nondrivers-int(num_nondrivers*percent_female))]})
    
    XX_drive=pd.DataFrame({'drivers':[int(num_drivers*percent_drive)]})
    XY_drive=pd.DataFrame({'drivers':[int(num_drivers-num_drivers*percent_drive)]})
    
    XX_data = pd.concat([XX_data, XX_nondrive], axis=1);  XX_data = pd.concat([XX_data, XX_drive], axis=1)
    XY_data = pd.concat([XY_data,XY_nondrive],axis=1);  XY_data = pd.concat([XY_data,XY_drive],axis=1)
    
    return XX_data,XY_data

def timearrays(event_info,XX_data,XY_data):
    """
    Create time arrays to allow for exponential decay
    """
    num_hours=int(event_info['num_hours'].dropna().item())
    XX_drive=int(XX_data['drivers'].dropna())
    XY_drive=int(XY_data['drivers'].dropna())
    
    XX_selections=XX_data['female_drink_selection'].dropna()
    XY_selections=XY_data['male_drink_selection'].dropna()
    
    #creating a time array for drivers. Note: 2 arrays required for different numbers of females and males
    XX_t_drive=pd.DataFrame({'drivers_time':np.array(([np.arange(0,num_hours)]*XX_drive)).flatten('F')})
    XY_t_drive=pd.DataFrame({'drivers_time':np.array(([np.arange(0,num_hours)]*XY_drive)).flatten('F')})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_t_drive], axis=1)
    XY_data = pd.concat([XY_data, XY_t_drive], axis=1)
    
    #creating a time array for drinkers.  Note: 2 arrays required for different numbers of females and males
    XX_t_drink=pd.DataFrame({'drinkers_time':np.array(([np.arange(0,num_hours)]*int(np.size(XX_selections,axis=0)/num_hours))).flatten('F')})
    XY_t_drink=pd.DataFrame({'drinkers_time':np.array(([np.arange(0,num_hours)]*int(np.size(XY_selections,axis=0)/num_hours))).flatten('F')})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_t_drink], axis=1)
    XY_data = pd.concat([XY_data, XY_t_drink], axis=1)
    
    return XX_data,XY_data
    
def hourlydrinks(event_info,XX_data,XY_data):
    """
    Add a decay to the number of drinks per hour.
    This attempts to recognise that people will slow their drinking as the event
    progresses
    """
    # Extract data from arrays
    XX_t_drink=XX_data['drinkers_time'].dropna()
    XY_t_drink=XY_data['drinkers_time'].dropna()
    
    XX=XX_data['Drinks_per_hour_dist'].dropna()
    XY=XY_data['Drinks_per_hour_dist'].dropna()
    
    XX_selections=XX_data['female_drink_selection'].dropna()
    XY_selections=XY_data['male_drink_selection'].dropna()

    #Use randomly selected drinks per hour to extract the hourly drinks for males and females
    XY_hourlydrinks_drink=pd.DataFrame({'drinks_per_hour_drink_decay':np.exp(-0.4*XY_t_drink)*np.array(XY[XY_selections])})
    XX_hourlydrinks_drink=pd.DataFrame({'drinks_per_hour_drink_decay':np.exp(-0.4*XX_t_drink)*np.array(XX[XX_selections])})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_hourlydrinks_drink], axis=1)
    XY_data = pd.concat([XY_data, XY_hourlydrinks_drink], axis=1)
    

    #for the people who are driving, we will assume 1 drink per hour for women and 2 in first hour
    #then 1 per hour for men
    XY_drive=int(XY_data['drivers'].dropna())
    XX_drive=int(XX_data['drivers'].dropna())
    num_hours=int(event_info['num_hours'].dropna().item())
  
    hour1_drive_male=np.array([1]*XY_drive)[:,None]
    hourrest_male=np.array([[1]*(num_hours-1)]*XY_drive)
    XY_hourlydrinks_drive=pd.DataFrame({'drinks_per_hour_drive':np.hstack((hour1_drive_male,hourrest_male)).flatten('F')})
    XX_hourlydrinks_drive=pd.DataFrame({'drinks_per_hour_drive':np.array([[1]*(num_hours)]*XX_drive).flatten('F')})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_hourlydrinks_drive], axis=1)
    XY_data = pd.concat([XY_data, XY_hourlydrinks_drive], axis=1)
    
  
    #add 'F' inside flatten bracket. need to add time which can be used in the decay.
    XX_t_drive=np.array(XX_data['drivers_time'].dropna())
    XY_t_drive=np.array(XY_data['drivers_time'].dropna())
    
    XX_hourlydrinks_drive=pd.DataFrame({'drinks_per_hour_drive_decay':np.exp(-0.4*XX_t_drive)*np.array(XX_data['drinks_per_hour_drive'].dropna())})
    XY_hourlydrinks_drive=pd.DataFrame({'drinks_per_hour_drive_decay':np.exp(-0.4*XY_t_drive)*np.array(XY_data['drinks_per_hour_drive'].dropna())})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_hourlydrinks_drive], axis=1)
    XY_data = pd.concat([XY_data, XY_hourlydrinks_drive], axis=1)
    
  
    
    return   XX_data,XY_data

def drink_price_selection(event_info,XX_data,XY_data):
    """
    Lets randomly select drinks and create an array
    """
    #Extract data from data area
    num_hours=int(event_info['num_hours'].dropna().item())
    drinkprice=np.array(event_info['drinkprice'].dropna()).astype(float)
    
    XX_drive=int(XX_data['drivers'].dropna())
    XY_drive=int(XY_data['drivers'].dropna())
    
    XX_drink_select=np.array(XX_data['female_drink_selection'].dropna()).astype(int)
    XY_drink_select=np.array(XY_data['male_drink_selection'].dropna()).astype(int)

    #drink selection for drivers
    XX_drink_selection_drive=np.random.randint(np.size(drinkprice),size=(XX_drive,num_hours)).flatten('F')
    XY_drink_selection_drive=np.random.randint(np.size(drinkprice),size=(XY_drive,num_hours)).flatten('F')
   
    #random selection of drink prices for male and female
    XY_drinks_prices_drink=pd.DataFrame({'drinks_prices_drinkers':drinkprice[XY_drink_select]})
    XX_drinks_prices_drink=pd.DataFrame({'drinks_prices_drinkers':drinkprice[XX_drink_select]})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_drinks_prices_drink], axis=1)
    XY_data = pd.concat([XY_data, XY_drinks_prices_drink], axis=1)
    
    
    XY_drinks_prices_drive=pd.DataFrame({'drinks_prices_drivers':drinkprice[XY_drink_selection_drive]})
    XX_drinks_prices_drive=pd.DataFrame({'drinks_prices_drivers':drinkprice[XX_drink_selection_drive]})
    
    #add to total array
    XX_data = pd.concat([XX_data, XX_drinks_prices_drive], axis=1)
    XY_data = pd.concat([XY_data, XY_drinks_prices_drive], axis=1)
    
    return XX_data, XY_data

def totalcalc(XX_data,XY_data):
    """
    This function takes the array of decaying time, drink selection, number of drivers to 
    calculate the total cost
    """
    
    #Extract necessary data from data frames
    hourlydrinksmale=np.array(XY_data['drinks_per_hour_drink_decay'].dropna())
    hourlydrinksfemale=np.array(XX_data['drinks_per_hour_drink_decay'].dropna())
    male_drinks_prices=np.array(XY_data['drinks_prices_drinkers'].dropna())
    female_drinks_prices=np.array(XX_data['drinks_prices_drinkers'].dropna())
    
     
    hourlydrinksdrivemen=np.array(XY_data['drinks_per_hour_drive_decay'].dropna())
    hourlydrinksdrivefemale=np.array(XX_data['drinks_per_hour_drive_decay'].dropna())
    male_drinks_pricesd=np.array(XY_data['drinks_prices_drivers'].dropna())
    female_drinks_pricesd=np.array(XX_data['drinks_prices_drivers'].dropna())
    
    #flatten arrays and mulitply by average drink price
    total_drinks_malesnd =sum(hourlydrinksmale*male_drinks_prices)
    total_drinks_femalesnd=sum(hourlydrinksfemale*female_drinks_prices)
    
    total_drinks_malesd =sum(hourlydrinksdrivemen*male_drinks_pricesd)
    total_drinks_femalesd=sum(hourlydrinksdrivefemale*female_drinks_pricesd)
    
    
    # Calculate the total cost of the bar tab
    total_cost =total_drinks_malesnd +total_drinks_malesd + total_drinks_femalesnd + total_drinks_femalesd  
    
    return total_cost

def drinkcalc():
    
    data= {'num_guests': [34], #number of guests attending
       'percent_drive': [0.7], #fraction driving
       'percent_female': [0.7], #fraction female
       'num_hours': [2],#number hours for the event (note: must be in multiples of 1 hour)
       'drinkprice':[6,7,8.50,7,15,12], # drink prices for available drinks
       'weekday': ['yes'] #specify weekend or weekday event. This alters the drinks per hour for each distribution
       }
 
    event_info = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in data.items()]))

    #initialise dataframes for carrying variables across
    XX_data=pd.DataFrame(); XY_data=pd.DataFrame()
    
    XX_data,XY_data=formdist(event_info,XX_data,XY_data) # form distributions for drinks per hour (XY=men, XX=female)
   
    #calulate split of female and male drivers/nondrivers
    XX_data,XY_data=driveorno(event_info,XX_data,XY_data)
    
    #create arrays of random values to be used in array sampling
    XX_data,XY_data=randomsample(event_info,XX_data,XY_data)
  
    #create time array for decay of drinking rate as hours progress
    XX_data,XY_data=timearrays(event_info,XX_data,XY_data)
   
    #calculate hourly drinks for drivers and drinkers including rate decay
    XX_data,XY_data=hourlydrinks(event_info,XX_data,XY_data)

    XX_data, XY_data=drink_price_selection(event_info,XX_data,XY_data)
    
    #calculate teh toal price
    total_cost=totalcalc(XX_data,XY_data)
   
    
    # Print the total cost
    ##print("Total cost: $" + str(total_cost))
    return total_cost


if __name__ == "__main__":
    
    #need to add the ability to read in the information maybe from a file
    
    totaldrinks=[]
    for i in range(1000):
        drinks=drinkcalc()
        totaldrinks.append(drinks)
            
    average=np.mean(totaldrinks)
    
    print("Total cost: $" + str(average))




