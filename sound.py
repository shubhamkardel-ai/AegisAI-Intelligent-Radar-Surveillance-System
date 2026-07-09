import pygame
import os

# Initialize the mixer
pygame.mixer.init()

# Get the absolute path of the current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the assets folder
ASSETS = os.path.join(BASE_DIR, "assets")

# Load MP3 sound files
sweep = pygame.mixer.Sound(os.path.join(ASSETS, "sweep.mp3"))
beep = pygame.mixer.Sound(os.path.join(ASSETS, "beep.mp3"))
alert = pygame.mixer.Sound(os.path.join(ASSETS, "alert.mp3"))

# Set volume
sweep.set_volume(0.2)
beep.set_volume(0.5)
alert.set_volume(0.8)


def play_sweep():
    sweep.play()


def play_beep():
    beep.play()


def play_alert():
    alert.play()


def stop_all():
    pygame.mixer.stop()