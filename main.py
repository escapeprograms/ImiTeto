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

devices = player.getDevices()
for device in devices:
    print(f"Device: {device.Item3}, ID: {device.Item2}")
player.setDevice("speakers") #cable input, headphones, speakers

time.sleep(3)
print("adding notes and playing")


for i in range(10):
    player.resetParts()
    player.addNote(0, 400, 60, "hello")
    
    player.addNote(500, 500, 60, "world")


    pitches = [0,100,200,300]
    player.setPitchBend(pitches, 50)

    print("playing...")
    player.play()
    time.sleep(3)


# outputUstx = "output.ustx"
# player.exportUstx(outputUstx)
