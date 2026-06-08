import openpyxl
import subprocess
import os

# Set folder location of main budget document
budgetExcelDoc = os.path.expanduser("~/Documents/Personal Budgeting/Grieger Personal Budget Tracker.xlsm")

rawTransactionFolder = os.path.expanduser("~/Documents/Personal Budgeting/Raw Transaction Data")
                                          
# Set folder location of raw inputs
    # Loop through to combine as one file?

# Configure categorization params 

# parse raw inputs one row at at time to LLM for format and categorization 

# parse string from LLM output for data to put in excel file, after each transaction? probably


prompt = '''
You are a data processing script. Your task is to clean credit card transaction rows and assign them to a strict set of categories.

Input format: A single row of comma-separated values (CSV).

Rules:
1. If the row is a header, empty, or does not contain a valid transaction, output exactly: "SKIP"
2. Clean the vendor name to be human-readable (e.g., "AMZN MKTP US*123" -> "Amazon").
3. Convert all transaction amounts to a positive number.
4. Assign exactly one of the allowed categories below. Do not create new categories.

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

Output format: Return only the raw text in this exact format, with no markdown, no quotes, and no conversational filler:
[transaction date],[cleaned transaction vendor],[positive amount],[assigned category]
'''

result = subprocess.run(['ollama', 'run', 'llama3.1',prompt],capture_output=True, text=True)

print(result.stdout)
