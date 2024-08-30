import pyaudio
import pygame
import math

clock = pygame.time.Clock()

# === Initialize Audio === #
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,)


def get_audio_input_level():
    data = stream.read(CHUNK)
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (CHUNK / 2))
    return rms

def draw_sine_wave(amplitude):
    pass