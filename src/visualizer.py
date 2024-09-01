import pygame
import math
import pyaudio
import sys
import wave

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
pygame.init()
pygame.display.set_caption('Gerald Visualiser')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# === Initialize Audio === #
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def get_audio_input_level(data):
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (CHUNK / 2))
    return rms

def draw_sine_wave(amplitude):
    screen.fill((0, 0, 0))
    points = []
    if amplitude > 10:
        for x in range(SCREEN_WIDTH):
            y = SCREEN_HEIGHT / 2 + int(amplitude * math.sin(x * 0.02))
            points.append((x, y))
    else:
        points.append((0, SCREEN_WIDTH / 2))
        points.append((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    pygame.display.flip()

filepath = 'samples\RiveR - Solo.wav'

with wave.open(filepath, 'rb') as wf:
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    frames_per_buffer=CHUNK)

    running = True
    amplitude = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        data = wf.readframes(CHUNK)
        amplitude_adjustment = get_audio_input_level(data=data) / 100
        amplitude = max(15, amplitude_adjustment)

        draw_sine_wave(amplitude=amplitude)
        clock.tick(60)

pygame.quit()