
## Code Challenge 

Analyzing loyalty trends in campaign contributions by identifying areas of repeat donors and calculating how much they're spending.

### Data Structure

I used Python Dictionary to track all distinct contributions (calendar year, recipient, and zipcode) as keys with their contributed amount list. Python dictionaries are based on hash table implementation that provides O(1) time complexity for lookup and insert operations in the average case independent of the size of the dictionary.

I used Python List to keep track of all received amounts for distinct contributions (calendar year, recipient, and zipcode). I do not do any lookup (O(n) time complexity), but I used it to get the value from an ordered amount list that corresponds to the ordinal rank of percentile.

I used Python Set to track all donors with donation years, such that I created a dictionary contains all years set in addition to donors set of each year.
A set is an unordered collection of unique items. Since a set is a sort of dictionary. Therefor searching for an item in a set is O(1).

### Repeat Donors 

A repeat donor is a donor who had previously contributed to any recipient in any prior calendar year, e.g a received donor in year 2017 while also found in donors set of year 2016.

#### An Initial Version
I initially created donation-analytics_v0.py by considering repeat donors if at least two contributions received from the same donor, regardless of the years.

### How to Run

Go to the folder root, then run:
```
donation-analytics~$ ./run.sh
```

#### Example
Results of running a large input file (itcont.txt):
```
Number of Input Rows = 6714651
Number of Valid Rows = 3700053
Number of Output Rows = 1801
Execution Time = 150.677527189 seconds
```

### How to Test

Go to the insight_testsuite folder, then run:
```
insight_testsuite~$ ./run_tests.sh 
```

