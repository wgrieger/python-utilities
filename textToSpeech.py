import os
import subprocess
import pyttsx3
import time

# MacOS can compress to M4A in file browser for more widespread playback 

# invokes macOS’s say command and produces AIFF. Windows does not have say. 
# The pyttsx3 notification speech should work, 
# but file generation needs a Windows-compatible implementation—typically 
# pyttsx3.save_to_file() producing WAV.

# Voice quality was great

# Put txt file in folder and link here 
folderPath = os.path.expanduser("~/Desktop/")

# Specify file name
textFile = "Opinion.txt"

textToSpeech = folderPath + "/" + textFile

# Spoken alert
engine = pyttsx3.init()

notif = "Script starting with: " + textToSpeech
print(notif)
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)


subprocess.run(["say", "-r", "120","-f", textToSpeech, "-o", os.path.splitext(textToSpeech)[0] + ".aiff"], check=True)

# --------------------
# Completion
# --------------------

notif = "script complete"
engine.say(notif)
engine.runAndWait()
time.sleep(0.2)
print(notif)

