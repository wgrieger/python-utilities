import openpyxl
import subprocess
import os
import csv
from google import genai

client = genai.Client(api_key=os.environ.get('PYTHON_GEMINI_KEY'))

#------------------
# Set Folder and File Locations 
#------------------

budgetExcelDoc = os.path.expanduser("~/Documents/Personal Finance/Budgeting/Grieger Personal Budget Tracker.xlsm")

rawTransactionFolder = os.path.expanduser("~/Documents/Personal Finance/Budgeting/Raw Transaction Data")

# which worksheet within budget excel doc? 
# define 2026 somehow 

#------------------
# Prompt for LLM
#------------------

prompt = '''
Take this row of data and determine if it is a credit card transaction. 

If it is not a credit card transaction or you believe it to be a payment, say '0' and add no further commentary to your response.

If it is a credit card transaction, match it to one of the categories below, and respond with the transaction formatted exactly like this,
and with no other commentary in the response:

'[transaction date],[cleaned and formatted vendor name],[transaction amount as positive number],[assigned category]'

Rules:
- Don't include the brackets or quotes in your response
- Don't ever add any text that doesn't fit the the response criteria provided
- Use the context provided in the data to aid your categorization
- The response is being processed by code, so it is imperitive it is structured exactly as ordered and never deviates at all.

Allowed Categories:
- Dining: Restaurants, delivery apps, bars, food courts.
- Gas/Automotive: Gas stations, car maintenance, dealerships, auto parts stores.
- Merchandise: General retail, Amazon, online shopping orders not fitting elsewhere.
- Grocery: Supermarkets, grocery stores, Target, Walmart.
- Entertainment: Movie theaters, concerts, theme parks, events.
- Subscription: Recurring digital charges (e.g., streaming, software, VPN).
- Travel: Airlines, hotels, rideshares (Ubers/Lyft), public transit.
- Professional Services: Personal and business services (e.g., accounting, haircuts).
- Health Care / Gym: Medical co-pays, pharmacies, fitness memberships, wellness.
- Homeownership: Hardware stores (e.g., Home Depot, Lowe's), contractor bills.
- Education: Tuition, school fees, online educational platforms.
- Charity: Donations and non-profit contributions.
- Interest / Fees: Card annual fees, bank fees, interest charges.
'''

def llmQuery(transaction):
    input = prompt + transaction 
    query = subprocess.run(['ollama', 'run', 'llama3.1',input],capture_output=True, text=True)
    output = query.stdout
    return output

def geminiQuery(transaction):
    input = prompt + transaction 
    response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[input]
                )
    return response

# print(result.stdout)

#------------------
# File Loop  
#------------------

for file in os.listdir(rawTransactionFolder):

    locateDot = file.rindex('.')
    fileType = file[locateDot:len(file)]
    
    completeFilePath = rawTransactionFolder + '/' + file

    if fileType == ".csv":
        with open(completeFilePath, newline='') as csvfile:
            for row in csvfile:
                 print(geminiQuery(row))
                 

    elif fileType == ".xlsx" or ".xlsm" or ".xtlx" or ".xtlm":
         ''
    


#------------------
# Logic for Handling Result
#------------------


# if !skip 
# parse by comma and add to excel 

