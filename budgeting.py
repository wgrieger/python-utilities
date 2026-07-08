import os
import pandas
from google import genai
from dotenv import load_dotenv
import time
load_dotenv()

client = genai.Client(api_key=os.environ.get('PYTHON_GEMINI_KEY'))

#------------------
# Set Folder and File Locations 
#------------------

budgetFolder = os.path.expanduser("~/Documents/Personal Finance/Budgeting")

rawTransactionFolder = os.path.expanduser("~/Documents/Personal Finance/Budgeting/Save Transaction Data Here")

#------------------
# Prompt and Function for LLM
#------------------

prompt = '''
 Here is a spreadsheet of credit card transactions. Look at each row and follow these instructions carefully.

If it is not a credit card transaction or you believe it to be a payment, ignore the data.

If it is a credit card spending transaction, match it to one of the categories below:
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

Rules:
- Don't ever add any text or characters that don't fit the the response criteria provided, including in an initial response or if there are no transactions
  on the document at all. If that is the case, cancel and return 'ignore' exactly.
- Use the context provided in the data to aid your categorization
- it is imperative it is structured exactly as ordered and never deviates at all.
i.e. do not respond anything like 'Please provide the row of data you would like me to process.'
- Date format 'MM-DD-YY'
- Include credits and refunds where applicable as a negative number
- accuracy is very important here
- brackets in format are used for example and should not be present in final output


Finally, return as text in the CSV format all of the transactions with this exact structure:

'[transaction date],[cleaned and formatted vendor name],[transaction amount as positive number],[assigned category]' 
'''

def geminiQuery(file): 
    attempt = 0
    fail = True
    while attempt<11 and fail==True:
        try:
            response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=[prompt,file]
                        )      
            fail = False
        except: 
            attempt = attempt+1
            print("something didn't work. Trying again.")
            print("attempt: "+ str(attempt))
            time.sleep(5)
    
    if response.text != "ignore":         
        open(budgetFolder+'/Combined Output.csv','a').write("\n"+response.text)
        print('file processed and saved to csv')
    else: 
        print('no response')

#------------------
# File Loop  
#------------------
for file in os.listdir(rawTransactionFolder):
    print(file)

    locateDot = file.rindex('.')
    fileType = file[locateDot:len(file)]
    
    completeFilePath = rawTransactionFolder + '/' + file

    if fileType == ".csv":
        file = open(completeFilePath, 'rb').read()
        geminiQuery(file)

    elif fileType == ".xlsx" or fileType == ".xlsm" or fileType ==".xtlx" or fileType ==".xtlm":
        file = pandas.read_excel(completeFilePath).to_csv().encode()
        geminiQuery(file)
    