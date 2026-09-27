import os
import subprocess

# Put txt file in folder and link here 
folderPath = os.path.expanduser("~/Documents/")

# Specify file name
textFile = "Notes Output.txt"

textToSpeech = folderPath + "/" + textFile

subprocess.run(["say", "-f", textToSpeech, "-o", os.path.splitext(textToSpeech)[0] + ".aiff"], check=True)

# MacOS can compress to M4A in file browser for more widespread playback 
# Voice quality was great