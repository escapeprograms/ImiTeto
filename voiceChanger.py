import numpy as np

class RealTimeVoiceChanger:
    def __init__(self, player):
        self.player = player


    def transcribe(self, text):
        self.player.resetParts()

        cur_time = 0
        for w in text.split(" "):
            word_time = len(w) * 100
            pitch = np.random.randint(60, 71) 
            self.player.addNote(cur_time, word_time, pitch, w)
            cur_time += word_time

    def play(self):
        self.player.play()

    def export(self, outputUstx):
        self.player.exportUstx(outputUstx)
        print(f"Exported to {outputUstx}")

class NemoVoiceChanger:
    def __init__(self, player, asr_model):
        self.player = player
        self.asr_model = asr_model

        self.should_play = False

    def transcribe(self, audio_data_float32):
        self.player.resetParts()

        current_transcription = self.asr_model.transcribe([audio_data_float32], batch_size=1, timestamps=True, verbose=False)[0]
        print(f"Transcription: {current_transcription.text}")
        
        #no word, wait some more
        words = current_transcription.timestamp['word']
        if len(words) == 0:
            self.should_play = False
            print("...")
            return

        #use magic to make teto repeat
        offset = words[0]['start_offset']

        for w in words:
            print(int(w['start_offset']-offset)*100, int(w['end_offset']-w['start_offset'])*100, w['word'])
            self.player.addNote(int(w['start_offset']-offset)*100, int(w['end_offset']-w['start_offset'])*100, 60, w['word'])

        self.should_play = True

    def play(self):
        if not self.should_play:
            return
        
        self.player.play()

    def export(self, outputUstx):
        self.player.exportUstx(outputUstx)
        print(f"Exported to {outputUstx}")