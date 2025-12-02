import sounddevice as sd
import numpy as np
import wave

def record_audio(filename, duration=5, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording finished.")
    # Save as WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

def play_audio(filename):
    with wave.open(filename, 'rb') as wf:
        fs = wf.getframerate()
        channels = wf.getnchannels()
        frames = wf.readframes(wf.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)
        if channels == 2:
            audio = audio.reshape(-1, 2)
        sd.play(audio, fs)
        sd.wait()