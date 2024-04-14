#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 08:20:45 2023

@author: dylanagius
"""


import marimo

__generated_with = "0.1.0"
app = marimo.App()


@app.cell
def __(mo):
    mo.md("# Bar Tab Calculator 🍺")
    return


@app.cell
def __(mo):
    mo.md("Use this tool to estimate the required dollar amount needed for an event")
    return



@app.cell
def __(mo):
    settings = mo.vstack(
        [
            mo.md("Provide Guest Information"),
            num_guests := mo.ui.number(label="Number of guests", start=1, stop=1000),
            percent_drive := mo.ui.number(label="Percentage expected to drive", start=0, stop=100),
            percent_female := mo.ui.number(label="Percentage of women attending", start=0, stop=100),
            numhours := mo.ui.number(label="Hours you would like to tab to last", start=1, stop=12),
            weekday := mo.ui.number(label="Is this a school night event (yes/no) ", start=1, stop=12),
            #fix weekday
            #add dirnks
            
        ]
    )

   

    mo.ui.tabs(
        {
            "Your Guest Information": settings,
          
        }
    )
    return numguests, percentdrive, percentfemale, numhours,settings



# """
# This function determines the number of cost for given information.
# The drinks per hour for each gender is determine by applying a normal distribution.

# Things to improve: currently if you are driving, no drinks are calculated: this should be changed to 1 standard drink an hour
# *The other improvement is the rate. There saturday drinking rates and sunday drinking rates.
# *Also the the current drinks per hour is linear.  This should be exponential decay
# """
@app.cell
def __(num_guests,percent_drive, perecent_female, numhours, weekday,stats,np,random):
    
    def formdist(weekday):
        """
        Calculate distributions for female and male drinks for the selection of 
        number of drinks per hour
        """
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
        
        X_drinks_per_hour_dist=XX; XY_drinks_per_hour_dist=XY
        return X_drinks_per_hour_dist, XY_drinks_per_hour_dist


    def driveorno(num_guests, percent_drive, percent_female, numhours):
        """
        Calculate the number of drivers and non drivers then split into genders
        """
        
        # Calculate the number of guests who do not drive
        num_drivers=int(num_guests*percent_drive)
        num_nondrivers=num_guests-num_drivers
        
        
        #split this into male and female
        XX_nondrive=int(num_nondrivers*percent_female)
        XY_nondrive=int(num_nondrivers-int(num_nondrivers*percent_female))
        
        XX_drive=int(num_drivers*percent_drive)
        XY_drive=int(num_drivers-num_drivers*percent_drive)
        
        return XX_nondrive,XX_drive,XY_nondrive,XY_drive


    def randomsample(XX_nondrive,XY_nondrive,XX_drive,XY_drive,num_hours,drinkprice):
        """
        Creates arrays using random numbers to samplefrom the 'drink per hour array' in formdist()
        and the drinkprice array
        """
        #make an random selection array for drink selection and drinks per hour from the drinkprice array
        XX_drink_select=np.random.randint(np.size(drinkprice),size=(XX_nondrive,num_hours)).flatten('F')
        XY_drink_select=np.random.randint(np.size(drinkprice),size=(XY_nondrive,num_hours)).flatten('F')
    
        #create an array used to sample from the distributions formed by formdist()
        XX_drink_per_hour=np.random.randint(1000,size=(XX_nondrive,num_hours)).flatten('F')
        XY_drink_per_hour=np.random.randint(1000,size=(XY_nondrive,num_hours)).flatten('F')
    
        #drink selection for drivers
        XX_drink_selection_drive=np.random.randint(np.size(drinkprice),size=(XX_drive,num_hours)).flatten('F')
        XY_drink_selection_drive=np.random.randint(np.size(drinkprice),size=(XY_drive,num_hours)).flatten('F')
       
    
        return XX_drink_per_hour, XY_drink_per_hour, XX_drink_selection_drive, XY_drink_selection_drive


    def timearrays(XX_drink_per_hour,XY_drink_per_hour,XX_drive,XY_drive,num_hours):
        """
        Create time arrays to allow for exponential decay
        """
        
        #creating a time array for drivers. Note: 2 arrays required for different numbers of females and males
        XX_t_drive=np.array(([np.arange(0,num_hours)]*XX_drive)).flatten('F')
        XY_t_drive=np.array(([np.arange(0,num_hours)]*XY_drive)).flatten('F')
        
        
        #creating a time array for drinkers.  Note: 2 arrays required for different numbers of females and males
        XX_t_drink=np.array(([np.arange(0,num_hours)]*int(np.size(XX_drink_per_hour,axis=0)/num_hours))).flatten('F')
        XY_t_drink=np.array(([np.arange(0,num_hours)]*int(np.size(XY_drink_per_hour,axis=0)/num_hours))).flatten('F')
            
        return XX_t_drive,XY_t_drive,XX_t_drink,XY_t_drink


    def hourlydrinks(XX_drive,XY_drive,XY_t_drink,XX_t_drink,XX_t_drive,XY_t_drive,XY_drinks_per_hour_dist,XX_drinks_per_hour_dist,XY_drink_select,XX_drink_select,num_hours,np):
        """
        Add a decay to the number of drinks per hour.
        This attempts to recognise that people will slow their drinking as the event
        progresses
        """
    
        #Use randomly selected drinks per hour to extract the hourly drinks for males and females
        XY_hourlydrinks_drink_decay=np.exp(-0.4*XY_t_drink)*np.array(XY_drinks_per_hour_dist[XY_drink_select])
        XX_hourlydrinks_drink_decay=np.exp(-0.4*XX_t_drink)*np.array(XX_drinks_per_hour_dist[XX_drink_select])
        
    
        #for the people who are driving, we will assume 1 drink per hour for women and 2 in first hour
        #then 1 per hour for men
      
        hour1_drive_male=np.array([1]*XY_drive)[:,None]
        hourrest_male=np.array([[1]*(num_hours-1)]*XY_drive)
        XY_hourlydrinks_drive=np.hstack((hour1_drive_male,hourrest_male)).flatten('F')
        XX_hourlydrinks_drive=np.array([[1]*(num_hours)]*XX_drive).flatten('F')
    
        #add 'F' inside flatten bracket. need to add time which can be used in the decay.
        XX_hourlydrinks_drive_decay=np.exp(-0.4*XX_t_drive)*XX_hourlydrinks_drive
        XY_hourlydrinks_drive_decay=np.exp(-0.4*XY_t_drive)*XY_hourlydrinks_drive
    
        return XY_hourlydrinks_drive,XX_hourlydrinks_drive,XX_hourlydrinks_drive_decay, XY_hourlydrinks_drive_decay


    def drink_price_selection(XX_drink_selection_drive,XY_drink_selection_drive,XY_drink_select,XX_drink_select,drinkprice):
        """
        Lets randomly select drinks and create an array
        """
    
       
        #random selection of drink prices for male and female
        XY_drinks_prices_drink=drinkprice[XY_drink_select]
        XX_drinks_prices_drink=drinkprice[XX_drink_select]
        
        
        XY_drinks_prices_drive=drinkprice[XY_drink_selection_drive]
        XX_drinks_prices_drive=drinkprice[XX_drink_selection_drive]
        
        return XY_drinks_prices_drink,XX_drinks_prices_drink,XY_drinks_prices_drive,XX_drinks_prices_drive


    def totalcalc(XX_drinks_prices_drive,XX_hourlydrinks_drive_decay,XY_drinks_prices_drive,XY_hourlydrinks_drive_decay,XY_hourlydrinks_drink_decay,XY_drinks_prices_drink,XX_hourlydrinks_drink_decay,XX_drinks_prices_drink):
        """
        This function takes the array of decaying time, drink selection, number of drivers to 
        calculate the total cost
        """
     
        
        #flatten arrays and mulitply by average drink price
        total_drinks_malesnd =sum(XY_hourlydrinks_drink_decay*XY_drinks_prices_drink)
        total_drinks_femalesnd=sum(XX_hourlydrinks_drink_decay*XX_drinks_prices_drink)
        
        total_drinks_malesd =sum(XY_hourlydrinks_drive_decay*XY_drinks_prices_drive)
        total_drinks_femalesd=sum(XX_hourlydrinks_drive_decay*XX_drinks_prices_drive)
        
        
        # Calculate the total cost of the bar tab
        total_cost =total_drinks_malesnd +total_drinks_malesd + total_drinks_femalesnd + total_drinks_femalesd  
       
        return total_cost

@app.cell
def __():
    """Calculate the total across 1000 possibilities  """
    totaldrinks=[]
    for i in range(1000):
        
        drinks=itercalc().totalcalc()
        totaldrinks.append(drinks)
            
    average=np.mean(totaldrinks)
@app.cell
def __(numguests, percentdrive, percentfemale, numhours,np, plt, stats, random):
    
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
    num_guests = numguests.value
    percent_drive = float(percentdrive.value)/100
    percent_female= float(percentfemale.value)/100
    num_hours=numhours.value
    
    #drinks prices for each gender
    maledrinks=np.array([7,8.50,7,6])
    femaledrinks=np.array([9,9,8,15,12])
        
    
    # Calculate the number of guests who do not drive
    num_nondrivers = num_guests - (num_guests * percent_drive)
    
    #create a for loop to do this over 1000 times to find the mean of the results
    totaldrinks=[]
    for i in range(1000):
    
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
        
        totaldrinks.append(total_cost)
        
    #calculate the mean of the sample possibilities
    average_total_cost=np.mean(totaldrinks)
    
    # Print the total cost
    ##print("Total cost: $" + str(total_cost))
    return average_total_cost

# @app.cell
# def __(total_cost,mo):
    
#     totaldrinks=[]
#     for i in range(1000):
#         drinks=drinkcalc()
#         totaldrinks.append(drinks)
        
#     average=np.mean(totaldrinks)

#     print("Total cost: $" + str(average))


@app.cell
def __(average_total_cost,numguests, percentdrive, percentfemale, numhours,mo):
    mo.md(
        f"""
        Your total tab value requred is $ **{average_total_cost}**
      
        """
    )  if all([numguests.value>1, percentdrive.value>0, percentfemale.value>0, numhours.value>1]) else None
    return



@app.cell
def __():
    import marimo as mo
    import numpy as np


    import matplotlib.pyplot as plt
    import scipy.stats as stats

    import random as random

    return mo,np, plt, stats, random


if __name__ == "__main__":
    app.run()

