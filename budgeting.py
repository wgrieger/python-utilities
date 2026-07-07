import subprocess
import os
import pandas as pd
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.environ.get('PYTHON_GEMINI_KEY'))

#------------------
# Set Folder and File Locations 
#------------------

budgetExcelDoc = os.path.expanduser("~/Documents/Personal Finance/Budgeting/Grieger Personal Budget Tracker.xlsm")

# with open_xlsx(budgetExcelDoc) as wb:
#     workSheet= wb['2026']

rawTransactionFolder = os.path.expanduser("~/Documents/Personal Finance/Budgeting/Raw Transaction Data")

# which worksheet within budget excel doc? 
# define 2026 somehow 

#------------------
# Prompt and Function for LLM
#------------------

prompt = '''
Take this row of data and determine if it is a credit card transaction. 

If it is not a credit card transaction or you believe it to be a payment, say '0' and add no further commentary to your response.

If it is a credit card transaction, match it to one of the categories below, and respond with the transaction formatted exactly like this,
and with no other commentary in the response:

'[transaction date],[cleaned and formatted vendor name],[transaction amount as positive number],[assigned category]'

Rules:
- Don't include the brackets or quotes in your response
- Don't ever add any text that doesn't fit the the response criteria provided, including in an initital response
- Use the context provided in the data to aid your categorization
- The response is being processed by code, so it is imperitive it is structured exactly as ordered and never deviates at all.
    i.e. do not respond anything like 'Please provide the row of data you would like me to process.'
- If data is blank, return 0


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

Here is the data to process:
'''

# def llmQuery(transaction):
#     input = prompt + transaction 
#     query = subprocess.run(['ollama', 'run', 'llama3.1',input],capture_output=True, text=True)
#     output = query.stdout
#     return output

def geminiQuery(transaction):
    input = prompt + transaction
    # print(input) 
    response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=[input]
                )
    return response.text


#------------------
# File Loop  
#------------------

# frozen from looping
# for file in os.listdir(rawTransactionFolder):

file = os.listdir(rawTransactionFolder)[0]

# print(file) 

# reindent below here
locateDot = file.rindex('.')
fileType = file[locateDot:len(file)]
    
completeFilePath = rawTransactionFolder + '/' + file

# print(completeFilePath)

if fileType == ".csv":
    with open(completeFilePath, newline='') as csvfile:
            # for row in csvfile:
            #      print(geminiQuery(row))
            print('skip csv')   

elif fileType == ".xlsx" or ".xlsm" or ".xtlx" or ".xtlm":
    #    here is the total file 
       openFile = pd.read_excel(completeFilePath,0)
    #    row = 0
    #    for row in openFile:
    #     print(openFile[row])
    #     row=row+1

testTransaction = (openFile.loc[10]).to_string()



# print(testTransaction)
# print(type(testTransaction))
# end indent 

print(geminiQuery(testTransaction))

#------------------
# Logic for Handling Result
#------------------


# if !skip 
# parse by comma and add to excel 

