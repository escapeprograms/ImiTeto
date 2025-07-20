import nemo.collections.asr as nemo_asr
import numpy as np
import pyaudio

# --- Configuration ---
MODEL_NAME = "stt_en_fastconformer_transducer_large_ls"
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Sample rate (must match model's sample rate)

# 1. --- Load a streaming-capable NeMo model ---
print("Loading NeMo model...")
# Using a Transducer model as they are excellent for streaming
asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name=MODEL_NAME)
asr_model.eval() # Set model to inference mode

# 2. --- Set up PyAudio to capture microphone audio ---

p = pyaudio.PyAudio()
microphone_index = 11

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=1)

print("\n--- Starting real-time transcription, press Ctrl+C to stop ---")

# 3. --- Main processing loop ---
try:
    # This is a simplified conceptual loop. NeMo's streaming API can be more complex.
    # The `transcribe_realtime` method is a conceptual wrapper for the underlying
    # setup_streaming, process_chunk, and get_hypotheses steps.
    # We will simulate this by collecting chunks and transcribing periodically.
    
    buffer = []
    
    while True:
        # Read a chunk of audio from the microphone
        data = stream.read(CHUNK_SIZE)
        buffer.append(data)
        
        # Periodically process the buffered audio to get a transcription update
        if len(buffer) > 40: # Transcribe every ~1.5 seconds of audio
            # Convert the list of byte chunks into a single numpy array
            audio_data_int16 = np.frombuffer(b''.join(buffer), dtype=np.int16)
            audio_data_float32 = audio_data_int16.astype(np.float32) / 32768.0

            # Get the current transcription
            # Note: For true low-latency, you'd use the model's internal streaming state.
            # This periodic transcription is a practical way to demo it.
            current_transcription = asr_model.transcribe([audio_data_float32], batch_size=1)[0]
            
            # Print the transcription, overwriting the previous line
            print(f"Transcription: {current_transcription.text}", end='\r')
            
            # Clear the buffer to start fresh for the next segment
            buffer.clear()

except KeyboardInterrupt:
    print("\n--- Stopping transcription ---")
finally:
    # 4. --- Cleanup ---
    stream.stop_stream()
    stream.close()
    p.terminate()