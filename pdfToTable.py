import pdfplumber
from tabulate import tabulate
from pathlib import Path


filePath = Path(r"C:\Users\will")

pdf  = pdfplumber.open(filePath)

# data = "" 

# for page in pdf.pages:
#     # extractedData= page.extract_tables(table_settings={})
#     extractedData = page.extract_text_simple(x_tolerance=3, y_tolerance=3)
#     # data = data + extractedData
#     print((extractedData))

print(pdf.pages[0].extract_text_simple(x_tolerance=10,y_tolerance=10))

print(pdf.pages[0].extract_tables(table_settings={}))

