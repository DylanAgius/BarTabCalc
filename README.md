#  :beer: BarTabCalc :cocktail:
This tool takes the guess work out of arriving at the perfect amount needed to balance your finances while ensuring everyone at your event is satisfied. Given some important information, it will tell you how much you should be aiming to put on the tab at the bar for your event.

## Important details.
The drinks per hour for each men and women are determined by sampling normal distributions. These distributions assume men will drink more per hour than women. For both men and women, the minimum drink per hour is 0 but the maximum for men is 5 while the maximum for women is 3. These values are used for weekends.  For "school night" events, the maximum values are locked in as 3 and 2 for men and women respectively. This alters the standard deviation but I have left the mean the same for both. The  details of distribution are the following:
|   | Mean | Standard deviation| Standard deviation ("school night")|
|--------|------|--------------------|-----------------------------------|
|Men     | 2    |                5/4 |                              3/4  |
|Women   | 1    |                3/4 |                               3/4 |

For those who are driving, the drink rate is different.  This is 1 in the first hour, and then 1 in each subsequent hour.

Additionally, the drink rate decays with hours (using a decay rate of 0.4). This approach assumes that initially guests will be drinking faster but as the event goes on, the drink rate will slow.

The simulation is run 1000 times and the average result is supplied. This is done so that distributions are sampled multiple times in an attempt to consider many possibilities in combinations of drink prices and drink rates.

## :notebook: Details you must provide
You must select some information about the party you are having. This includes:
* Number of guests
* Approximate percentage driving
* Gender split (provided as percentage of females)
* Number of hours the event will be going for
* Number of drinks and the corresponding price for each (separated by a comma).
* Whether the event is on a "school night"

## Usage
There are two ways to use the tool. You can run the code using:
```python
python BarTabCalc
```
You will then be prompted to provide event information for the calculation.

The other usage is with [Marimo](https://github.com/marimo-team/marimo.git).
This code has been developed to be used with Marimo, allowing a seamless deployable app which you can use. 


## :dart: Accuracy
If you do use this tool, please let me know the results of the simulation and the actual amount so that we can see the accuracy and attempt to improve it.

|  Event    | Prediction | Actual   |
|-----------|------------|----------|
|Baby shower| $560       | $575     |




