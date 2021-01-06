import csv
import requests
from bs4 import BeautifulSoup
import json
import pandas # pip install pandas, pip install openpyxl 


# extract type of "geelong-vic-3220"
def domainAddress(area):

    #call API for postcode
    url = "https://www.domain.com.au/phoenix/api/locations/autocomplete/v2?prefixText={}&stateBoost=vic".format(area)
    r = requests.get(url)
    j = json.loads(r.text)
    # print (j)
    # extract only "geelong-vic-3220" in Json type of file. [{'value': 'geelong-vic-3220'},{}...]
    # suburb = j[0]["value"] # It bring only one {}
    
    # vacant LIST for extracting value.
    prefix=[]
    for k in j:
        # print (k)  # bring dictionary from list [{}.{}] => {},{}
        prefix.append(k["value"]) # put them into prefix List ["","",""]

    # print(prefix) # ["","",""]
    return prefix


# Call selected List 
def domainAddressList(cat,UserSuburb):

    # how many surburbs are incluing postcode entered by user 
    UserSuburbTotal=len((UserSuburb))
    print(UserSuburbTotal) 

    for j in range(0, UserSuburbTotal):
        print (UserSuburb[j])

        results = []
        for i in range(1, 3): # number of pages. start from 1page to 3page

            #call Lists for entered postcode
            #https://www.domain.com.au/sale/wallan-vic-3756/?page=2
            url2 = "https://www.domain.com.au/{}/{}/?page={}".format(cat, UserSuburb[j], i)
            # print (url2)
            r2 = requests.get(url2);
            bs2 = BeautifulSoup(r2.text, "html.parser");

            # CSS Pattern is diffrent. => sale:div.css-1n74r2t  rent:div.css-1gkcyyc
            if (cat == 'sale'):
                saleRent = '1n74r2t'
            elif (cat == 'rent'):
                saleRent = '1gkcyyc'

            lists=bs2.select("div.css-1mf5g4s > ul > li > div > div.css-{} > div".format(saleRent))

                #skip-link-content > div.css-1ned5tb > div.css-1mf5g4s > ul > li:nth-child(4) > div > div.css-1gkcyyc > div
                #skip-link-content > div.css-1ned5tb > div.css-1mf5g4s > ul > li:nth-child(11) > div > div.css-1gkcyyc > div > div.css-9hd67m
            for li in lists:
                price=li.select("div.css-1mf5g4s > ul > li > div > div.css-{} > div > div.css-9hd67m".format(saleRent))[0].text
                address=li.select("div.css-1mf5g4s > ul > li > div > div.css-{} > div > a".format(saleRent))[0].text
                detail=li.select("div.css-1mf5g4s > ul > li > div > div.css-{} > div > div.css-1t41ar7".format(saleRent))[0].text
                 
                results.append([price,address,detail]) # Store a type of List using Pandas DataFrame.
    return results


#Category validation check(Element Must be included in 'categorySave' List )
def categoryValidation(userInput):
    
    # Check whether List elements are included.
    categorySave = ["sale","rent"]
        
    if userInput in categorySave: 
        return(userInput.lower()) #Making the entered character small Letter
    else:
        return False


#Postcode validation check(Only number).
def postcodeValidation(userpostcode):
    if userpostcode.isnumeric() == True:
        print("Your postcode is {}".format(userpostcode))
        return userpostcode

    elif userpostcode.isnumeric() == False:
        print("Please enter number only ")
        answer = input("Please enter PostCode: ")
        return answer



#Result Print
validatedCategory=categoryValidation(input("Please enter rent or sale: "))
print("Your Category is '{}'".format(validatedCategory))

# If validatedCategory is not included in the List, Let user enter the category again.
while validatedCategory == False:
    print("Your Category is not right")
    print("please enter the category again")
    validatedCategory=categoryValidation(input("Please enter rent or sale: "))

# If validatedCategory is  included in the List, Let user enter the postcode.
if validatedCategory != False:
    answer = postcodeValidation(input("Please enter PostCode: "))

    # If returned postcode is not number, Let user enter the postcode again.
    while answer.isnumeric() == False:
        answer = postcodeValidation(input("Please enter PostCode: "))

    # If returned postcode is number, the postcode is returned to domainAddress function as a parameter.
    if answer.isnumeric() == True:
        suburb=domainAddress(answer)

        # Pandas DataFrame
        column = ["Price", "Address", "Detail"]  
        
        # After checking validation for category and postcode, They will pass to the
        # parameter of domainAddressList function. and The result will be returned to resultsList as argument.

        resultsList=domainAddressList(validatedCategory, suburb) 

        # The resultsList will pass to pandas.DataFrame as a parameter to show a form of pandas.
        dataframe = pandas.DataFrame(resultsList, columns = column)
        print(dataframe)

        # Save excel file or csv file.
        dataframe.to_excel("property2.xlsx", sheet_name="kk", header=True, startrow=1)