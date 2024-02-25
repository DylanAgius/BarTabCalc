# BarTabCalc
An app to calculate the approximate bar tab required for an event.

## Important details.
The drinks per hour for each men and women are determined by sampling normal distributions. These distributions assume men will drink more per hour then women. For both men and women, the minimum drink per hour is 0 but the maximum for men is 5 while the maximum for women is 3. These values are used for weekends.  For weekday events, the values between 3 and 2 for men and women respectively. The  details of distribution are the following:
|  empty | Mean | Standard deviation|
|--------|------|--------------------|
|Men| 2    | (5-0)/4 |
|Women| 1  | (3-0)/4 |

For those who are driving, the drink rate is different.  This is 2 in the first hour for men, and then 1 in each subsequent hour. For females, it is 1 per hour.

Additionally, the drink rate decays with hours. This approach assumes that initially guests will be drinking faster but as the event goes on, the drink rate will slow.

## Details you must provide
You must select some information about the party you are having. This includes:
* Number of guests
* Approximate percentage driving
* Gender split (provided as percentage of females)
* Number of hours the event will be going for
* Number of drinks and the corresponding price per drink for both men and women.


