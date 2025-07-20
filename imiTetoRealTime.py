print("Loading RealtimeSTT")
from RealtimeSTT import AudioToTextRecorder

import pythonnet
pythonnet.load("coreclr")
import clr
import os
import sys
import time

from voiceChanger import RealTimeVoiceChanger
from util import spectral_flatness, spectral_flux

def create_callback(voice_changer):
    def _process_text(text):
        print(text)
        voice_changer.transcribe(text)
        voice_changer.play()
    return _process_text

if __name__ == '__main__':
    print("Loading UtauGenerate")
    dependency_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","API","UtauGenerate","bin","Debug","net9.0","UtauGenerate.dll")
    clr.AddReference(dependency_dir)
    from UtauGenerate import Player


    #load Teto player
    print("Loading Teto player...")
    player = Player()

    # devices = player.getDevices()
    player.setDevice("speakers") #cable input, headphones, speakers

    # Initialize VoiceChanger
    voice_changer = RealTimeVoiceChanger(player)

    try:
        print("\n--- Starting real-time transcription, press Ctrl+C to stop ---")
        recorder = AudioToTextRecorder(language="en", model="tiny")
        while True:
            recorder.text(create_callback(voice_changer))
    except KeyboardInterrupt:
        print("\n--- Stopping transcription ---")
        recorder.shutdown()
        