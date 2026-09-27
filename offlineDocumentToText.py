import pdfplumber
import sys
import time
import os
import pyttsx3

# --------------------
# Functions 
# --------------------
def extractAllPages(document):
#  This is a PDF plumber function, Gemini has tended to be more useful
 
    pageNum = 0
    pageCount = len(document.pages)
    
    printOutput = ""

    while pageNum <= pageCount-1:
        text = document.pages[pageNum].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=True, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None)
        
        printOutput = printOutput+ text
        print(pageNum)
        pageNum = pageNum+ 1
    
    return printOutput


def extractSpecificPages(document, specificPages):
    # Pass specific pages as function
    #  This is a PDF plumber function, Gemini has tended to be more useful 
    printOutput = ""

    for pageNum in specificPages:
        text = document.pages[pageNum].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=True, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None)
        
        printOutput = printOutput+ text
        print(pageNum)
    
    return printOutput

# --------------------
# Script Start 
# --------------------
engine = pyttsx3.init()

notif = "Script starting"
print(notif)
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)

# --------------------
# Folder Method
# --------------------

# For bulk or single file, create a folder with one or many documents. Leave trailing slash off.
folderPath = os.path.expanduser("~/Desktop/")

# Adds a file to the folder location
saveFileTo = folderPath + "/"  


# Future title for cleaned and final text extraction
fileOutputTitle = "Opinion"

# Holds the extraction text during the script
printOutput = ""

# -------------------------------------
# Single File 
# -------------------------------------

singleFile = ""

file = folderPath + "/" + singleFile

with pdfplumber.open(file) as pdf:  
    response = extractAllPages(pdf)
    # OR 
    # response = extractSpecificPages(pdf, [43,44,45,46,47,48,49,50])

    printOutput = response

# -------------------------------------
# Multi File Model = Loop through the folder for each file
# -------------------------------------

# for each in os.listdir(folderPath):
#     file = folderPath + "/" + each

#     notif = "Processing file: " + each
#     print(notif)
#     engine.say(notif)
#     engine.runAndWait()
#     time.sleep(0.2)

#     if each.endswith(".pdf"):
#         # -----------
#         # pdfplumber functions
#         # ------------

#         with pdfplumber.open(file) as pdf:  
#             #response = extractAllPages(pdf)
#             # OR 
#             response = extractSpecificPages(pdf, [43,44,45,46,47,48,49,50])


#         # Adds each file extraction to the bottom of the printOutput variable  
#         printOutput = printOutput + "\n" + response
        
# --------------------
# Completion
# --------------------

# Saves unmodified printoutput to the raw file    
open(saveFileTo+fileOutputTitle + ".txt", "w").write(printOutput)

notif = "script complete"
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)
print(notif)

# Not using at this time

# --------------------
# Double Checking / OCR
# --------------------
# if printOutput == "":
#     print("no text found, likely scanned document. Attempting OCR...")
#     # send to gemini
#     # subprocess.run(["ocrmypdf", filePath, saveFileTo + fileOutputTitle])
#     sys.exit()
