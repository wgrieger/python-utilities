import openpyxl
import subprocess


# Set folder location of main budget document

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
Merchandise = Shopping for non-grocery and non-homegoods e.g. Amazon 
Dining = Resturaunts, fast food, etc. 
Grocery = Grocery stores, grocery delivery, etc. 

Please review the tranaction data and return it in this format:

"[transaction date],[transaction vendor (where the money was spent)],[amount of spend as positive number (how much money was spent)],
[assigned category]"

How long do this this will take you per row of data on a 16gb RAM cpu?

Do you have the data you need for this? Could anything be more descriptive?
'''

result = subprocess.run(['ollama', 'run', 'llama3.1',prompt],capture_output=True, text=True)

print(result.stdout)
