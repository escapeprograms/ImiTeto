from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("Ready")
    recorder = AudioToTextRecorder(language="en", model="tiny")

    while True:
        recorder.text(process_text)