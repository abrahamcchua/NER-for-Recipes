import json

'''
Aim of this script is to check why the number of parsed websites
in recipes is not equal to the number of links to be parsed
'''
# Read the json files
with open('links.json', 'r') as f:
    truth = json.load(f)
    
with open('recipes.json', 'r') as f:
    test = json.load(f)

# List comprehension to make checking easier
truth_list =[i['link'] for i in truth]
test_list=[i['link'] for i in test]

    
# Check the number of values for each link
print(len(test_list), len(truth_list))
# 1204 1206

# Print the links that were not parsed
[print(l) for l in truth_list if l not in test_list]


# Checking Manually why it did not work
# The instruction on how to prepare the meal is not given
# https://www.budgetbytes.com/mini-garden-turkey-loaf-meal/
# The instruction follows a different format compared to the others
# https://www.budgetbytes.com/picnic-potato-salad/

