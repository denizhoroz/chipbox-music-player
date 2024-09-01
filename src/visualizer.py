import pygame
import math
import pyaudio

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

running = True
amplitude = 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    amplitude_adjustment = get_audio_input_level() / 50
    amplitude = max(10, amplitude_adjustment)

    draw_sine_wave(amplitude=amplitude)
    print(get_audio_input_level())
    clock.tick(60)

pygame.quit()