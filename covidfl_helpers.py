# Functions used in the data pull and calculations for covidfl, which is the core function for application.py

# Function to subtract the items in the list from one another. This is used to calculate the daily changes
def list_subtract(list1, list2):
    list_dfc = []
    list1_len = len(list1)
    list2_len = len(list2)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_dfc.append(list1[i] - list2[i])
    return(list_dfc)

# Function to add the items in the list to one another (adding two lists - used for Jacksonville region)
def list_add2(list1, list2):
    list_add = []
    list1_len = len(list1)
    list2_len = len(list2)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_add.append(list1[i] + list2[i])
    return(list_add)

# Function to add the items in the list to one another (adding two lists - used for Tampa, South Florida, and Orlando regions)
def list_add3(list1, list2, list3):
    list_add = []
    list1_len = len(list1)
    list2_len = len(list2)
    list3_len = len(list3)
    if list1_len != list2_len:
        print("Lists must have the same number of items")
    if list1_len != list3_len:
        print("Lists must have the same number of items")
    for i in range(list1_len):
        list_add.append(list1[i] + list2[i] + list3[i])
    return(list_add)

# Formats numbers with commas: 1000 to 1,000
def commas_place(value):
    return ("{:,}".format(value))

# Formats to %. Started from USD from cs50 helpers.py program for Finance project
def pct(value):
    return f'{value:,.1f}%'
