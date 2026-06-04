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

# Turn VPN off for large files

client = genai.Client(api_key=os.environ.get['PYTHON_GEMINI_KEY'])

prompt = """
[insert prompt]

"""

path = os.path.expanduser("~/Documents/")
file = "Notes.txt"

outputTitle = "Notes.txt"

file = open(path + file, "rb").read()

tries = 10
fail = True 
attempt = 0

while fail == True and attempt < tries:

    try:
        response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[file, prompt]
                )
         
        fail = False
         
    except:
        print("Error, trying: " + attempt)
        attempt += 1
        time.sleep(5)


# print(response.text)

open(path+outputTitle, "w").write(response.text)

