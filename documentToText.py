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

# Where the raw files are saved
# Leave trailing slash off
folderPath = os.path.expanduser("~/Documents")

# Adds a file to the folder location
saveFileTo = folderPath + "/"  

# Raw text extraction before cleaning 
roughFormatOutputTitle = "Rough Text Output from Flash Lite"

# Cleaned and final text extraction
fileOutputTitle = "Final Output for Use"

# Holds the extraction text during the script
printOutput = ""

# Loop through the folder for each file
for each in os.listdir(folderPath):
    file = folderPath + "/" + each

    if each == ".DS_Store" or each.startswith("."):
        continue

    notif = "Processing file: " + each
    print(notif)
    engine.say(notif)
    engine.runAndWait()
    time.sleep(0.2)

    # Guesses file type for binary 
    mime_type, _ = mimetypes.guess_type(str(each))

    # Fails if unknown
    if mime_type is None:
        notif = "Could not determine MIME type for file: " + each
        print(notif)
        engine.say(notif)
        engine.runAndWait()
        time.sleep(0.2)

        sys.exit()

    # Opens file for API with text prompt
    file = open(file, "rb").read()
    
    filePrompt = """
    Convert this document to plain text as faithfully as possible. 

    Preserve the author's words exactly. Do not rewrite, summarize, correct grammar, or change meaning. 

    If a character, word, or passage is unclear, do not guess or reconstruct it from context. Leave a blank space for the unclear portion and continue with the next legible text. 

    Preserve separate blocks of text and their approximate reading order based on their physical position on the page. Do not infer relationships between blocks merely because of their placement, and do not reorganize the content by topic. 

    Keep text together that clearly belongs together.

    Preserve obvious headings, bullets, numbering, arrows, and simple structural relationships when they can be represented clearly in plain text.

    For drawings or graphics, briefly represent their meaning only when it is unambiguous; otherwise omit them. 

    For tables, preserve the text and relationships as faithfully as possible in a readable plain-text format. Do not invent labels or relationships that are not explicit.

    The priority is faithful transcription, not interpretation. When uncertain, preserve uncertainty rather than inventing text.
    """

# Flash lite does well for these extractions
    success = False
    max_retries = 10

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                    model="gemini-flash-lite-latest",
                    contents=[types.Part.from_bytes(
                                data=file,
                                mime_type=mime_type,
                            ), 
                            filePrompt]
                )

            # Adds each file extraction to the bottom of the printOutput variable holder 
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

# Saves unmodified printoutput to the raw file    
open(saveFileTo+roughFormatOutputTitle + ".txt", "w").write(printOutput)

# --------------------
# FORMATTING
# --------------------

# Sends the raw file to gemini pro for cleaning and checking 

notif = "All files processed. Sending to Gemini for final formatting check..."
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)
print(notif)

formatPrompt = """
    Here is a collection of documents converted to .txt. 

    Please read through this and use your best judgement to understand the intended structure and reading order. 

    Then, without changing any wording, preserve the author's words exactly, do not summarize, correct grammar, or change meaning, 
    organize the text in a way that best presents the intended meaning when read from beginning to end.

    Perhaps no changes are needed. Make changes conservatively. 

"""

formatThis = open(saveFileTo+roughFormatOutputTitle + ".txt", "rb").read()

response = client.models.generate_content(
            model="gemini-flash-latest",
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


