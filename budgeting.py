import openpyxl
import subprocess
import os

# Set folder location of main budget document
budgetExcelDoc = os.path.expanduser("~/Documents/Personal Budgeting/Grieger Personal Budget Tracker.xlsm")

rawTransactionFolder = os.path.expanduser("~/Documents/Personal Budgeting/")
                                          
# Set folder location of raw inputs
    # Loop through to combine as one file?

# Configure categorization params 

# parse raw inputs one row at at time to LLM for format and categorization 

# parse string from LLM output for data to put in excel file, after each transaction? probably


prompt = '''
You will be passed credit card or similiar transaction data as a row of comma seperated values.

Your role will be to clean the data and assign a category. There will be a category provided that may or not match perfectly. 
Use your best judgement to assign one of the defined ones.

The categories are:
Dining - e.g. Resturaunts, delivery apps, food courts. 
Gas/Automotive - e.g. Gas stations, car maintenance, dealerships, car stores (e.g. NAPA/Autozone)
Merchandise -- General retail purchases that don't fit in another category e.g. Amazon, online '.com' orders
Grocery -- e.g. Walmart, Target, and common grocers even not coded as such by the card company 
Entertainment -- e.g. Movie theatres, theme parks, events 
Subscription -- Monthly or annual digital charges such as Apple Music, email, VPN, etc.
Travel -- Airlines, hotels, Ubers, etc. 
Professional Services -- Service businesses that don't fit under other categories e.g. accounting, hair cuts
Health Care / Gym -- Healthcare, wellness, and gym services e.g. memberships, saunas, co-pays
Homeownership -- Notably, Home Depot or contractor bills
Education -- Booth School of Business or online educational resources 
Charity -- Donations 

Please review the tranaction data and return it in this format:

"[transaction date],[transaction vendor (where the money was spent)],[amount of spend as positive number (how much money was spent)],
[assigned category]"

'''

result = subprocess.run(['ollama', 'run', 'llama3.1',prompt],capture_output=True, text=True)

print(result.stdout)
