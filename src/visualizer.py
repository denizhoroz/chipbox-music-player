import pygame
import math
import pyaudio
import sys
import wave

class Visualizer:
    def __init__(self, width, height) -> None:
        # Configurations
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNEL = 1
        self.RATE = 44100
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        pygame.display.init()
        pygame.display.update()

    def get_audio_input_level(self, data):
        rms = 0
        for i in range(0, len(data), 2):
            sample = int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
            rms += sample * sample
        rms = math.sqrt(rms / (self.CHUNK / 2))
        return rms
    
    def draw_sine_wave(self, amplitude):
        self.screen.fill((0, 0, 0))
        points = []
        if amplitude >= 1:
            for x in range(self.width):
                y = self.height / 2 + int(amplitude * math.sin(x * 0.02))
                points.append((x, y))
        else:
            points.append((0, self.width / 2))
            points.append((self.width, self.height))

        pygame.draw.lines(self.screen, (255, 255, 255), False, points, 2)
        pygame.display.flip()

    def load_file(self, filename):
        self.wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        self.stream = p.open(format=
                        p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        frames_per_buffer=self.CHUNK)

        amplitude = 100

        self.data = self.wf.readframes(self.CHUNK)

    def run(self):
        self.stream.write(self.data)
        self.data = self.wf.readframes(self.CHUNK)
        # for event in pygame.event.get():      
        #     if event.type == pygame.QUIT: 
        #         running = False

        amplitude_adjustment = self.get_audio_input_level(self.data) / 500
        amplitude = max(1, amplitude_adjustment)

        self.draw_sine_wave(amplitude)
        self.clock.tick(60)


if __name__ == '__main__':
    visualizer = Visualizer(300, 80)
    filename = 'samples/RiveR - Solo.wav'
    
    visualizer.load_file(filename=filename)
    while True:
        visualizer.run()

# === Testing === #
'''
def get_audio_input_level(data):
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (chunk / 2))
    return rms

def draw_sine_wave(amplitude):
    screen.fill((0, 0, 0))
    points = []
    if amplitude >= 1:
        for x in range(width):
            y = height / 2 + int(amplitude * math.sin(x * 0.02))
            points.append((x, y))
    else:
        points.append((0, width / 2))
        points.append((width, height))

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    pygame.display.flip()

if __name__ == '__main__':
    chunk = 1024
    format = pyaudio.paInt16
    channel = 1
    rate = 44100
    clock = pygame.time.Clock()
    width = 300
    height = 80
    screen = pygame.display.set_mode((width, height))

    pygame.display.init()
    pygame.display.update()

    filename = 'samples\RiveR - Solo.wav'

    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=
                    p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    frames_per_buffer=chunk)

    amplitude = 100

    data = wf.readframes(chunk)

    running = True
    while running:  
            stream.write(data)
            data = wf.readframes(chunk)
            for event in pygame.event.get():      
                if event.type == pygame.QUIT: 
                    running = False

            amplitude_adjustment = get_audio_input_level(data) / 500
            amplitude = max(1, amplitude_adjustment)

            draw_sine_wave(amplitude)
            clock.tick(60)

    # cleanup stuff.
    wf.close()
    stream.close()    
    p.terminate()
'''
