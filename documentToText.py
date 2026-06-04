import pdfplumber
import os
import subprocess
import sys
from google import genai
from google.genai import types
import mimetypes
import pyttsx3
import time
from dotenv import load_dotenv
load_dotenv()

# --------------------
# Notes 
# --------------------
# Turn VPN off for large files

# I like to have the computer tell me what it is doing while the script is running incase it fails 

engine = pyttsx3.init()

client = genai.Client(api_key=os.environ.get('PYTHON_GEMINI_KEY'))

notif = "Script starting"
print(notif)
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)


# --------------------
# Functions 
# --------------------
def extractAllPages(document):
#  This is a PDF plumber function, Gemini has tended to be more useful
 
    pageNum = 0
    pageCount = len(document.pages)
    
    printOutput = ""

    while pageNum <= pageCount-1:
        text = document.pages[pageNum].extract_text(x_tolerance=2, x_tolerance_ratio=None, y_tolerance=2, layout=False, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None)
        
        printOutput = printOutput+ text
        print(pageNum)
        pageNum = pageNum+ 1
    
    return printOutput


def extractSpecificPages(document, specificPages):
    #  This is a PDF plumber function, Gemini has tended to be more useful 
    printOutput = ""

    for pageNum in specificPages:
        text = document.pages[pageNum].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=True, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None)
        
        printOutput = printOutput+ text
        print(pageNum)
    
    return printOutput



# --------------------
# Single File Method 
# --------------------
# filePath = os.path.expanduser("~/Documents/")

# locationLastSlash = filePath.rfind("/")

# saves to same folder as original file, change if you want to save somewhere else
# saveFileTo = filePath[:locationLastSlash+1]

# fileOutputTitle = "_____ Notes Formatted" 

# pdfplumber
# document = pdfplumber.open(filePath)

#gemini


# --------------------
# Whole folder
# --------------------
folderPath = os.path.expanduser("~/Documents/")

saveFileTo = folderPath + "/"  

roughFormatOutputTitle = "Notes"

fileOutputTitle = "Notes Output"

printOutput = ""

for each in os.listdir(folderPath):
    file = folderPath + "/" + each

    if each == ".DS_Store" or each.startswith("."):
        continue

    notif = "Processing file: " + each
    print(notif)
    engine.say(notif)
    engine.runAndWait()
    time.sleep(0.2)

    mime_type, _ = mimetypes.guess_type(str(each))
    
    if mime_type is None:
        notif = "Could not determine MIME type for file: " + each
        print(notif)
        engine.say(notif)
        engine.runAndWait()
        time.sleep(0.2)

        sys.exit()

    file = open(file, "rb").read()
    
    filePrompt = """
    [insert prompt you want to accompany each file]
    """

    success = False
    max_retries = 10
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=[types.Part.from_bytes(
                                data=file,
                                mime_type=mime_type,
                            ), 
                            filePrompt]
                )
            # Note: Changed your "/n" to "\n" for a proper newline
            printOutput = printOutput + "\n" + response.text
            success = True
            time.sleep(2) # Delay between files to prevent rate limiting
            break

        except Exception as e:
            print(f"Connection error on {each}: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            
    if not success:
        print(f"Failed to process {each} after {max_retries} attempts. Exiting.")
        sys.exit()
   
open(saveFileTo+roughFormatOutputTitle + ".txt", "w").write(printOutput)

classNotes = os.path.expanduser("~/Documents/")

printOutput = printOutput + "\n" + open(classNotes,'r').read()

open(saveFileTo+roughFormatOutputTitle + ".txt", "w").write(printOutput)


# --------------------
# FORMATTING
# --------------------

notif = "All files processed. Sending to Gemini for final formatting check..."
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)
print(notif)

formatPrompt = """
[insert prompt you want to accompany the request of all bundled together]
"""

formatThis = open(saveFileTo+roughFormatOutputTitle + ".txt", "rb").read()

response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[formatThis, formatPrompt]
        )

printOutput = response.text


# --------------------
# Double Checking / OCR
# --------------------
# if printOutput == "":
#     print("no text found, likely scanned document. Attempting OCR...")
#     # send to gemini
#     # subprocess.run(["ocrmypdf", filePath, saveFileTo + fileOutputTitle])
#     sys.exit()


# --------------------
# Save to File
# --------------------
open (saveFileTo+fileOutputTitle + ".txt", "w").write(printOutput)


# --------------------
# Completion
# --------------------

notif = "script complete"
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)
print(notif)


