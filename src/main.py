import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pygame
import os
import time

# === Default Constants === #
WIDTH = 720
HEIGHT = 480
BG_COLOR = '#D3EBCD'
FG_COLOR = '#AEDBCE'
BUTTON_COLOR = '#839AA8'
SHADOW_COLOR = '#635666'
BUTTON_TEXT_COLOR = BG_COLOR
BUTTON_WIDTH = 8
BUTTON_HEIGHT = 1
CONTROL_BUTTON_FONT = ('Arial', 20, 'normal')
BUTTON_FONT = ('Arial', 10, 'normal')
TEXT_COLOR = 'black'

# color palettes for reference: 
# https://colorhunt.co/palette/d3ebcdaedbce839aa8635666
# https://colorhunt.co/palette/1e201e3c3d37697565ecdfcc

# === Interface Configuration === #
class Interface():
    def __init__(self, root) -> None:
        self.root = root
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.resizable(False, False)
        self.root.iconbitmap('assets/ico32.ico')

        self.var_theme_is = 'light'
        self.var_theme = tk.StringVar()
        self.configure_theme(theme='light')

        self.initialize_widgets()
        self.initialize_player()

    def configure_theme(self, theme):
        global BG_COLOR
        global FG_COLOR
        global BUTTON_COLOR
        global SHADOW_COLOR
        global BUTTON_TEXT_COLOR
        global TEXT_COLOR

        if theme == 'dark':
            # === dark === #
            BG_COLOR = '#1E201E'
            FG_COLOR = '#3C3D37'
            BUTTON_COLOR = '#697565'
            SHADOW_COLOR = '#ECDFCC'
            self.footer = tk.PhotoImage(file='assets/footer_dark.png')
            TEXT_COLOR = 'white'
            self.var_theme.set('☀️')
        else:
            # === light === #
            BG_COLOR = '#D3EBCD'
            FG_COLOR = '#AEDBCE'
            BUTTON_COLOR = '#839AA8'
            SHADOW_COLOR = '#635666'
            self.footer = tk.PhotoImage(file='assets/footer_light.png')
            TEXT_COLOR = 'black'
            self.var_theme.set('🌙')
        BUTTON_TEXT_COLOR = SHADOW_COLOR

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
                                 bg=FG_COLOR,
                                 highlightbackground=BUTTON_COLOR,
                                 highlightthickness=1)
        self.frame_duration.place(x=20, y=20)

        self.duration = ttk.Label(self.frame_duration,
                                  text='00:00 /\n   00:00',
                                  font=('Arial', 22, 'bold'),
                                  background=FG_COLOR,
                                  foreground=SHADOW_COLOR)
        self.duration.place(x=8, y=5)

        # Initialize the audio spectrum
        self.spectrum = tk.Frame(self.frame_main,
                                 width=300,
                                 height=80,
                                 bg=FG_COLOR,
                                 highlightbackground=BUTTON_COLOR,
                                 highlightthickness=1)
        self.spectrum.place(x=160, y=20)

        # Initialize the song information area
        self.frame_song_info = tk.Frame(self.frame_main,
                                  width=440,
                                  height=30,
                                  bg=FG_COLOR,
                                  highlightbackground=BUTTON_COLOR,
                                  highlightthickness=1)
        self.frame_song_info.place(x=20, y=120)

        self.current_song = ''

        self.var_song_info = tk.StringVar()
        self.var_song_info.set('Please select a song from the playlist')

        style_song_info = ttk.Style()
        style_song_info.configure('Custom.TLabel',
                            font=BUTTON_FONT,
                            background=FG_COLOR,
                            foreground=TEXT_COLOR)
        
        self.label_song_info = ttk.Label(self.frame_song_info, 
                                         textvariable=self.var_song_info,
                                         style='Custom.TLabel')
        self.label_song_info.place(x=5, y=3)

        # Initialize the song trackbar
        self.trackbar = tk.Frame(self.frame_main,
                                 width=300,
                                 height=20,
                                 bg=FG_COLOR,)
        self.trackbar.place(x=20, y=160)

        self.var_progress = tk.DoubleVar().set(value=100)
        
        self.progress = ttk.Scale(self.trackbar,
                                 length=300,
                                 orient='horizontal',
                                 from_=0,
                                 to=1,
                                 variable=self.var_progress,
                                 command=self.update_progress)
        self.progress.place(x=0, y=0)

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
        self.volume_scale.place(x=0, y=0)


        # Initialize the buttons ⏮️⏯️⏭️
        self.button_prev = tk.Button(self.frame_main,
                                     text='⏮️',
                                     font=CONTROL_BUTTON_FONT,
                                     width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT,
                                     bg = FG_COLOR,
                                     fg=BUTTON_TEXT_COLOR,
                                     borderwidth=1,
                                     command=self.play_previous)
        self.button_prev.place(x=20, y=200)
        
        self.var_play = tk.StringVar()
        self.var_play.set('▶️')
        self.paused = False
        self.time_paused = 0

        self.button_pause = tk.Button(self.frame_main,
                                     textvariable=self.var_play,
                                     font=CONTROL_BUTTON_FONT,
                                     width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT,
                                     bg=FG_COLOR,
                                     fg=BUTTON_TEXT_COLOR,
                                     borderwidth=1,
                                     command=self.pause_song)
        self.button_pause.place(x=172, y=200)

        self.button_next = tk.Button(self.frame_main,
                                     text='⏭️',
                                     font=CONTROL_BUTTON_FONT,
                                     width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT,
                                     bg=FG_COLOR,
                                     fg=BUTTON_TEXT_COLOR,
                                     borderwidth=1,
                                     command=self.play_next)
        self.button_next.place(x=323, y=200)

        # Initialize the playlist
        self.frame_playlist = tk.Frame(self.frame_main,
                                 width=220,
                                 height=388,
                                 bg=FG_COLOR,)
        self.frame_playlist.place(x=480, y=20)

        self.song_dict = {}
        self.playlist = tk.Listbox(self.frame_playlist,
                                   width=36,
                                   height=24,
                                   bg=FG_COLOR,
                                   fg=TEXT_COLOR,)
        self.playlist.place(x=0, y=0)
        self.playlist.bind('<<ListboxSelect>>', self.play_selected)


        # Initialize import button
        self.import_button = tk.Button(self.frame_main,
                                       text='Import Music',
                                       font=('Arial', 10, 'normal'),
                                       width=10,
                                       height=1,
                                       bg=FG_COLOR,
                                       fg=TEXT_COLOR,
                                       borderwidth=1,
                                       command=self.import_music)
        self.import_button.place(x=480, y=420)
        
        # Initialize theme toggle button
        self.theme_toggle = tk.Button(self.frame_main,
                                      textvariable=self.var_theme,
                                      anchor='w',
                                      font=BUTTON_FONT,
                                      width=2,
                                      height=1,
                                      bg=FG_COLOR,
                                      fg=TEXT_COLOR,
                                      borderwidth=1,
                                      command=self.change_theme)
        self.theme_toggle.place(x=676, y=420)

        # Initialize footer
        self.footer_text = tk.Label(self.frame_main,
                                    image=self.footer,
                                    bg=BG_COLOR)
        self.footer_text.place(x=0, y=380)

    def initialize_player(self):
        pygame.init()
        pygame.mixer.init()

    def play_selected(self, event):
        selected_song = list(self.song_dict.values())[self.playlist.curselection()[0]]
        self.current_song = selected_song
        pygame.mixer.music.load(self.current_song)
        self.update_song_info()
        self.progress.config(to=self.song_length)
        pygame.mixer.music.play()
        self.song_start_time = time.time()
        self.update_progress()
        self.var_play.set('⏸️')

    def play_previous(self):
        selection = self.playlist.curselection()
        if selection:
            ind_prev_song = int(selection[0]) - 1
            if ind_prev_song >= 0:
                prev_song = list(self.song_dict.values())[ind_prev_song]
                self.current_song = prev_song
                self.playlist.selection_set(ind_prev_song)
                self.playlist.selection_clear(selection)
                pygame.mixer.music.load(self.current_song)
                self.update_song_info()
                pygame.mixer.music.play()
                self.song_start_time = time.time()
                self.var_play.set('⏸️')
            else:
                messagebox.showwarning('Warning', 'This is the first song.')

    def is_finished(self):
        if pygame.mixer.music.get_busy():
            return False
        else:
            return True
        
    def is_lastsong(self):
        selection = self.playlist.curselection()
        if selection:
            ind_next_song = int(selection[0]) + 1
            if ind_next_song < self.playlist.size():
                return False
            else:
                return True
            
    def pause_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.time_paused = 0
            self.paused = False
            self.update_progress()
            self.var_play.set('⏸️')
        elif self.is_finished():
            pygame.mixer.music.play()
            self.paused = False
            self.var_play.set('⏸️')
        else:
            pygame.mixer.music.pause()
            self.time_paused = time.time()
            self.paused = True
            self.var_play.set('▶️')
                
    def play_next(self):
        selection = self.playlist.curselection()
        if selection:
            ind_next_song = int(selection[0]) + 1
            if ind_next_song < self.playlist.size():
                next_song = list(self.song_dict.values())[ind_next_song]
                self.current_song = next_song
                self.playlist.selection_set(ind_next_song)
                self.playlist.selection_clear(selection)
                pygame.mixer.music.load(self.current_song)
                pygame.mixer.music.play()
                self.song_start_time = time.time()
                self.update_song_info()
                self.var_play.set('⏸️')
            else:
                messagebox.showwarning('Warning', 'This is the last song.')

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def update_progress(self, val=None):
        global_current_time = time.time() 
        if val:
            self.song_time_elapsed = float(val)
            pygame.mixer.music.set_pos(self.song_time_elapsed)
            self.progress.config(value=val)
            self.song_start_time = global_current_time - self.song_time_elapsed
        else:
            if self.paused:
                time_since_paused = global_current_time - self.song_time_elapsed
            else:
                self.song_time_elapsed = global_current_time - self.song_start_time 
                self.progress.config(value=self.song_time_elapsed)
                self.root.after(1000, self.update_progress)
            
        prog_minutes, prog_seconds = divmod(int(float(self.song_time_elapsed)), 60)
        total_minutes, total_seconds = divmod(int(self.song_length), 60) # change here
        self.duration.config(text='{:02d}:{:02d} /\n   {:02d}:{:02d}'.format(prog_minutes, prog_seconds, total_minutes, total_seconds))

        if self.is_finished() and not self.is_lastsong() and not self.paused:
            self.play_next()

    def update_song_info(self):
        self.var_song_info.set(os.path.basename(self.current_song)[0:80])
        self.song_length = pygame.mixer.Sound(self.current_song).get_length()

    def import_music(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            if file_path not in self.song_dict.values():
                song_name = os.path.basename(file_path)
                self.song_dict[song_name] = file_path
                self.playlist.insert(tk.END, song_name)

    def change_theme(self):
        if self.var_theme_is == 'light':
            self.var_theme.set('🌙')
            self.var_theme_is = 'dark'
            self.configure_theme(theme='dark')
            self.initialize_widgets()
            self.initialize_player()
        else:
            self.var_theme.set('☀️')
            self.var_theme_is = 'light'
            self.configure_theme(theme='light')
            self.initialize_widgets()
            self.initialize_player()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Chipbox')
    interface = Interface(root)
    root.mainloop()


