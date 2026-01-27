import pygame
class Mixer:
    def __init__(self):
        pygame.mixer.init()
        self.music_playing = False
        self.music_paused = False

    def load_music(self, music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.music_playing = True

        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")
            self.music_playing = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()