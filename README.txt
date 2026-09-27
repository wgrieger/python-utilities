This folder and environment is what I use to create Python utilites locally. 

Some of the example uses are:

- documentToText.py 
    - can convert a photo album of handwritten notes to a combined and organized .txt
    - converts PDF to .txt for text-to-speech
    - offlineDocumentToText.py uses pdfplumber instead of gemini for on-device processing

-textToSpeech.py lets you go from documentToText.py or offlineDocumentToText.py to a audio file to listen to. 

-pdfToTable.py uses pdfplumber to extract tables for data analysis 

-geminiApi.py is a blank slate to run more intensive tasks through the API, which is much more performant, as opposed to the web interface.

-budgeting.py uses gemini api to sort credit card transactions to update my personal finance tracking excel files

Note to self:
Bash Command to Activate my venv
    'source .venv/bin/activate'
