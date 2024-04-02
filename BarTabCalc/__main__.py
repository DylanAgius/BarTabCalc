#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:55:08 2024

@author: Dylan Agius

"""
import pandas as pd
from runner import runner


if __name__ == "__main__":
    #build data frame by taking inputs
    
    #Add the input data to dataframe for calculations 
    eventdata= {'num_guests': [int(input('Numer of guests: '))], #number of guests attending
       'percent_drive': [float(input('Percent expected to drive: '))/100], #fraction driving
       'percent_female': [float(input('Percent expected to be female: '))/100], #fraction female
       'num_hours': [int(input('Number of hours you would like to tab to last: '))],#number hours for the event (note: must be in multiples of 1 hour)
       'drinkprice':[float(e) for e in input('Drink prices (separated by a comma): ').split(",")], # drink prices for available drinks
       'weekday': [input('Is this a weekday event (not including Friday) (yes/no):' )] #specify weekend or weekday event. This alters the drinks per hour for each distribution
       }
    
    
    data = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in eventdata.items()]))
    
        
    print("Total cost: $" + str(runner(data).loop()))