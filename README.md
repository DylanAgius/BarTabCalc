# BarTabCalc
An app to calculate the approximate bar tab required for an event.

## Important details.
The drinks per hour for each men and women are determined by sampling normal distributions. These distributions assume men will drink more per hour then women. The both minimum drink per hour is 0 but the maximum for men is 5 while the maximum for women is 3.  The current details of each distribution are the following:
|   | Mean | Standard deviation|
|Men| 2    | (5-0)/4 |
|Women| 1  | (3-0)/4 |

## Details you must provide
You must select some information about the party you are having. This includes:
* Number of guests
* Approximate percentage driving
* Gender split (provided as percentage of females)
* Number of hours the event will be going for
* Number of drinks and the correponding price per drink for both men and women.


