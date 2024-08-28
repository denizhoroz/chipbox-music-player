import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pygame
import os

# === Constants === #
WIDTH = 720
HEIGHT = 480
BG_COLOR = '#D3EBCD'
FG_COLOR = '#AEDBCE'
BUTTON_COLOR = '#839AA8'
SHADOW_COLOR = '#635666'

BUTTON_WIDTH = 8
BUTTON_HEIGHT = 1
BUTTON_FONT = ('Arial', 20, 'normal')
BUTTON_TEXT_COLOR = SHADOW_COLOR

FOOTER_FONT = ('Helvatica', 40, 'bold')

# color palette for reference: https://colorhunt.co/palette/d3ebcdaedbce839aa8635666


# === Interface Configuration === #
class Interface():
    def __init__(self, root) -> None:
        self.root = root
        self.title = 'Chipbox'
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.resizable(False, False)

        self.initialize_widgets()
        self.initialize_player()

    def initialize_widgets(self):
        
        # Initialize the background frame
        self.frame_main = tk.Frame(self.root,
                                 width=WIDTH,
                                 height=HEIGHT,
                                 bg=BG_COLOR)
        self.frame_main.place(x=0, y=0)
        
        # Initialize the duration area
        self.frame_duration = tk.Frame(self.frame_main,
                                 width=120,
                                 height=80,
                                 bg=FG_COLOR)
        self.frame_duration.place(x=20, y=20)

        self.duration = ttk.Label(self.frame_duration,
                                  text='00:00',
                                  font=('Helvatica', 32, 'bold'),
                                  background=FG_COLOR,
                                  foreground=SHADOW_COLOR)
        self.duration.place(x=3, y=12)

        # Initialize the audio spectrum
        self.spectrum = tk.Frame(self.frame_main,
                                 width=300,
                                 height=80,
                                 bg=FG_COLOR)
        self.spectrum.place(x=160, y=20)

        # Initialize the song information area
        self.frame_song_info = tk.Frame(self.frame_main,
                                  width=440,
                                  height=30,
                                  bg=FG_COLOR)
        self.frame_song_info.place(x=20, y=120)

        self.current_song = ''

        self.var_song_info = tk.StringVar()
        self.var_song_info.set('Please select a song from the playlist')

        style_song_info = ttk.Style()
        style_song_info.configure('Custom.TLabel',
                            font=('Helvatica', 10, 'normal'),
                            background=FG_COLOR)
        
        self.label_song_info = ttk.Label(self.frame_song_info, 
                                         textvariable=self.var_song_info,
                                         style='Custom.TLabel')
        self.label_song_info.place(x=5, y=5)

        # Initialize the song trackbar
        self.trackbar = tk.Frame(self.frame_main,
                                 width=300,
                                 height=20,
                                 bg=FG_COLOR)
        self.trackbar.place(x=20, y=160)

        self.var_progress = tk.DoubleVar().set(value=100)
        
        self.progress = ttk.Progressbar(self.trackbar,
                                  length=300,
                                  orient='horizontal',
                                  mode='determinate')
        self.progress.place(x=0, y=-2)

        # Initialize the volume bar
        self.volumebar = tk.Frame(self.frame_main,
                                  width=130,
                                  height=20,
                                  bg=FG_COLOR)
        self.volumebar.place(x=330, y=160)

        self.var_volume = tk.DoubleVar(value=1)
        
        style = ttk.Style()
        style.configure('TScale',
                        troughcolor=BG_COLOR,
                        background=BG_COLOR)

        self.volume_scale = ttk.Scale(self.volumebar,
                                     length=130,
                                     value=1,
                                     style='TScale',
                                     orient='horizontal',
                                     from_=0,
                                     to=1,
                                     variable=self.var_volume,
                                     command=self.set_volume)
        self.volume_scale.place(x=0, y=-2)


        # Initialize the buttons ⏮️⏯️⏭️
        self.button_prev = tk.Button(self.frame_main,
                                     text='⏮️',
                                     font=BUTTON_FONT,
                                     width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT,
                                     bg=BUTTON_COLOR,
                                     fg=BUTTON_TEXT_COLOR,
                                     command=self.play_previous)
        self.button_prev.place(x=20, y=200)
        
        self.var_play = tk.StringVar()
        self.var_play.set('Play')
        self.paused = False

        self.button_pause = tk.Button(self.frame_main,
                                     text='⏯️',
                                     font=BUTTON_FONT,
                                     width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT,
                                     bg=BUTTON_COLOR,
                                     fg=BUTTON_TEXT_COLOR,
                                     command=self.pause_song)
        self.button_pause.place(x=172, y=200)

        self.button_next = tk.Button(self.frame_main,
                                     text='⏯️',
                                     font=BUTTON_FONT,
                                     width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT,
                                     bg=BUTTON_COLOR,
                                     fg=BUTTON_TEXT_COLOR,
                                     command=self.play_next)
        self.button_next.place(x=323, y=200)

        # Initialize the playlist
        self.frame_playlist = tk.Frame(self.frame_main,
                                 width=220,
                                 height=390,
                                 bg=FG_COLOR)
        self.frame_playlist.place(x=480, y=20)

        self.playlist = tk.Listbox(self.frame_playlist,
                                   width=220,
                                   height=390)
        self.playlist.place(x=0, y=0)
        self.playlist.bind('<<ListboxSelect>>', self.play_selected)

        # Initialize import button
        self.import_button = tk.Button(self.frame_main,
                                       text='Import Music',
                                       font=('Helvatica', 10, 'normal'),
                                       width=10,
                                       height=1,
                                       bg=BUTTON_COLOR,
                                       fg=BUTTON_TEXT_COLOR,
                                       command=self.import_music)
        self.import_button.place(x=480, y=420)

        # Initialize footer
        self.footer_text = tk.Label(self.frame_main,
                                    text='CHIPBOX',
                                    font=FOOTER_FONT,
                                    anchor='sw',
                                    width=8,
                                    height=1,
                                    bg=BG_COLOR,
                                    fg=SHADOW_COLOR)
        self.footer_text.place(x=20, y=400)
    
    def initialize_player(self):
        pygame.init()
        pygame.mixer.init()

    def play_selected(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        self.current_song = selected_song
        pygame.mixer.music.load(self.current_song)
        self.var_song_info.set('Now Playing: ' + os.path.basename(self.current_song)[0:40] + '...')
        self.progress['maximum'] = pygame.mixer.Sound(self.current_song).get_length()
        self.update_progress()
        pygame.mixer.music.play()
        self.var_play.set('Pause')

    def play_previous(self):
        selection = self.playlist.curselection()
        if selection:
            ind_prev_song = int(selection[0]) - 1
            if ind_prev_song >= 0:
                prev_song = self.playlist.get(ind_prev_song)
                self.current_song = prev_song
                self.playlist.selection_set(ind_prev_song)
                self.playlist.selection_clear(selection)
                pygame.mixer.music.load(self.current_song)
                self.var_song_info.set('Now Playing: ' + os.path.basename(self.current_song)[0:60] + '...')
                pygame.mixer.music.play()
                self.var_play.set('Pause')
            else:
                messagebox.showwarning('Warning', 'This is the first song.')


    def pause_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.var_play.set('Pause')
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.var_play.set('Play')

    def play_next(self):
        selection = self.playlist.curselection()
        if selection:
            ind_next_song = int(selection[0]) + 1
            if ind_next_song < self.playlist.size():
                next_song = self.playlist.get(ind_next_song)
                self.current_song = next_song
                self.playlist.selection_set(ind_next_song)
                self.playlist.selection_clear(selection)
                pygame.mixer.music.load(self.current_song)
                self.var_song_info.set('Now Playing: ' + os.path.basename(self.current_song)[0:40] + '...')
                pygame.mixer.music.play()
                self.var_play.set('Pause')
            else:
                messagebox.showwarning('Warning', 'This is the last song.')

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def update_progress(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        self.progress['value'] = current_time
        minutes, seconds = divmod(int(current_time), 60)
        self.duration.config(text='{:02d}:{:02d}'.format(minutes, seconds))
        self.root.after(1000, self.update_progress)

    def import_music(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            if file_path not in self.playlist.get(0, tk.END):
                self.playlist.insert(tk.END, file_path)


if __name__ == '__main__':
    root = tk.Tk()
    interface = Interface(root)
    root.mainloop()