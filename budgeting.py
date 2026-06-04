import openpyxl
import subprocess


prompt = '''
You will be passed credit card or similiar transaction data as a row of comma seperated values.

Your role will be to clean the data and assign a category. 

The categories are:



Please review the tranaction data and return it in this format:

"[transaction date],[transaction vendor (where the money was spent)],[amount of spend as positive number (how much money was spent)],
[assigned category]"


'''

result = subprocess.run(['ollama', 'run', 'llama3.1',prompt],capture_output=True, text=True)

print(result.stdout)

# Set folder location of main budget document

# Set folder location of raw inputs

# Configure categorization params 

# parse raw inputs one row at at time to LLM for format and categorization 
