import pythonnet
pythonnet.load("coreclr")
import clr
import os
import sys
import time

print("Loading UtauGenerate")
dependency_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","API","UtauGenerate","bin","Debug","net9.0","UtauGenerate.dll")
clr.AddReference(dependency_dir)
from UtauGenerate import Player

from voiceChanger import NemoVoiceChanger
from util import spectral_flatness, spectral_flux

print("Loading NeMo")
import nemo.collections.asr as nemo_asr
import numpy as np
import pyaudio
import librosa
import logging

logging.getLogger('nemo_toolkit').setLevel(logging.ERROR)

MODEL_NAME = "stt_en_fastconformer_ctc_large_ls" #"stt_en_fastconformer_transducer_large_ls"
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
OUTPUT_RATE = 16000  # Sample rate of model

RECORD_TIME = 2

SILENCE_TIME = 0.5
SILENCE_THRESHOLD = 300

#microphone settings
MICROPHONE_IDX = 12#11 and 12 are good
INPUT_RATE = 16000#48000 #sample rate of microphone

#load Teto player
print("Loading Teto player...")
player = Player()

# devices = player.getDevices()
# player.setDevice(devices[1].Item1, devices[1].Item2) #use device 1 (virtual cable) or 2 (normal output)
player.setDevice("speakers") #cable input, headphones, speakers

#load NeMo model
print("Loading NeMo model...")
asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name=MODEL_NAME)
asr_model.eval() # Set model to inference mode

# Initialize VoiceChanger
voice_changer = NemoVoiceChanger(player, asr_model)

#set up microphone input
p = pyaudio.PyAudio()


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=INPUT_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                #  input_device_index=MICROPHONE_IDX
                 )

print("\n--- Starting real-time transcription, press Ctrl+C to stop ---")

try:
    buffer = []
    
    while True:
        # Read a chunk of audio from the microphone
        data = stream.read(CHUNK_SIZE)
        buffer.append(data)
        
        #once buffer is big enough, transcribe
        num_chunks = int(SILENCE_TIME * (INPUT_RATE // CHUNK_SIZE))
        chunk = np.frombuffer(b''.join(buffer[-num_chunks:]), dtype=np.int16)
        print("spectral flatness:",spectral_flatness(chunk), end='\r')

        #done speaking and long enough buffer
        if spectral_flatness(chunk) > 0.003 and (len(buffer) > int(RECORD_TIME * (INPUT_RATE // CHUNK_SIZE))):
        # if len(buffer) > 60:
            #get the audio data
            audio_data_int16 = np.frombuffer(b''.join(buffer), dtype=np.int16)
            audio_data_float32 = audio_data_int16.astype(np.float32) / 32768.0

            if INPUT_RATE != OUTPUT_RATE:
                audio_data_float32 = librosa.resample(
                    y=audio_data_float32, 
                    orig_sr=INPUT_RATE, 
                    target_sr=OUTPUT_RATE
                )
            
            #transcribe and play
            voice_changer.transcribe(audio_data_float32)
            voice_changer.play()
            #clear audio buffer
            buffer.clear()
            

except KeyboardInterrupt:
    print("\n--- Stopping transcription ---")
finally:
    # 4. --- Cleanup ---
    stream.stop_stream()
    stream.close()
    p.terminate()