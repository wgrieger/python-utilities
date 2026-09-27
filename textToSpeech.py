import os
import subprocess

# Put txt file in folder and link here 
folderPath = os.path.expanduser("~/Documents")

# Specify file name
textFile = "Insert file name"

textToSpeech = folderPath + "/" + textFile

subprocess.run(["say", "-f", textToSpeech, "-o", os.path.splitext(textToSpeech)[0] + ".aiff"], check=True)
