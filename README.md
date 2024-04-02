# BarTabCalc
An app to calculate the approximate bar tab required for an event.

## Important details.
The drinks per hour for each men and women are determined by sampling normal distributions. These distributions assume men will drink more per hour than women. For both men and women, the minimum drink per hour is 0 but the maximum for men is 5 while the maximum for women is 3. These values are used for weekends.  For weekday events, the values between 3 and 2 for men and women respectively. The  details of distribution are the following:
|  empty | Mean | Standard deviation|
|--------|------|--------------------|
|Men| 2    | (5-0)/4 |
|Women| 1  | (3-0)/4 |

For those who are driving, the drink rate is different.  This is 1 in the first hour, and then 1 in each subsequent hour.

Additionally, the drink rate decays with hours (using a decay rate of 0.4). This approach assumes that initially guests will be drinking faster but as the event goes on, the drink rate will slow.

The simulation is run 1000 times and the average result is supplied. This is done so that distributions are sampled multiple times in an attempt to consider many possibilities in combinations of drink prices and drink rates.

## Details you must provide
You must select some information about the party you are having. This includes:
* Number of guests
* Approximate percentage driving
* Gender split (provided as percentage of females)
* Number of hours the event will be going for
* Number of drinks and the corresponding price for each (separated by a comma).

## Usage
This code has been developed to be used with Marimo, allowing a seamless deployable app which you can use. 

Additionally, if you'd prefer to not use Marimo, you can run the code using the following which will ask you to provide the required information:

```bash
python BarTabCalc
```

## Accuracy
If you do use this tool, please let me know the results of the simulation and the actual amount so that we can see the accuracy and attempt to improve it.

|  Event    | Prediction | Actual   |
|-----------|------------|----------|
|Baby shower| $560       | $575     |




