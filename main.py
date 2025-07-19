import pythonnet
pythonnet.load("coreclr")
import clr
import os
import sys
import time

dependency_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","API","UtauGenerate","bin","Debug","net9.0","UtauGenerate.dll")
clr.AddReference(dependency_dir)

from UtauGenerate import Player


player = Player()

time.sleep(3)
print("adding notes and playing")

player.addNote(0, 200, 60, "zef")


pitches = [0,100,200,300]
player.setPitchBend(pitches, 50)

print("playing...")
player.play()

time.sleep(4)
outputUstx = "output.ustx"
player.exportUstx(outputUstx)
