import os
os.system("pip install pygame")
os.system("pip3 install pygame")
os.system("pip install wget")
os.system("pip3 install wget")

import pygame
import json
import sys
import ctypes
import threading
import subprocess
import platform
import wget
from zipfile import ZipFile
from os.path import exists

## Game board
pygame.init()
width, height = 1920, 1080
fpsClock = pygame.time.Clock()
WIN = pygame.display.set_mode((width, height))

BLACK = (0,0,0)
BLUE = "#0f208a"
GREEN = "#167c80"
WHITE = (255,255,255)
RED = (93.3,13.3,16.1)
YELLOW = "#83d313"

TITLE_FONT = pygame.font.SysFont('comicsans', 50)
SUBTITLE_FONT = pygame.font.SysFont('comicsans', 40)
MEDIUM_FONT = pygame.font.SysFont('comicsans', 35)
SMALL_FONT = pygame.font.SysFont('comicsans', 25)
SMALLEST_FONT = pygame.font.SysFont('comicsans', 20)


## Game Values
FPS = 60
MAX_CARDS = 108
INITIAL_CARDS = 7
MAX_TURN_TIME = 30
clock = pygame.time.Clock()
small_font = pygame.font.Font(None, 35)
smallest_font = pygame.font.Font(None, 30)
warning_font = pygame.font.Font(None, 30)
count_font = pygame.font.Font(None, 50)
mini_font = pygame.font.Font(None, 20)

# Player values
downloads = open("devices.json")
downloads = json.load(downloads)


## App Info
icon = pygame.image.load('assets/icons/logo.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("Galaxy J5 Downloader")


# Game Assets

# Title Screen
logo = pygame.transform.scale(pygame.image.load(os.path.join("assets/logo", "logo.png")), (700, 300))
render = pygame.transform.scale(pygame.image.load(os.path.join("assets/logo", "render.png")), (1200, 800))

# Icons
mouse = pygame.transform.scale(pygame.image.load(os.path.join("assets/icons", "mouse.png")), (75, 75))

# Loader
loader_01 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_0_delay-0.1s.gif")), (100,100))
loader_02 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_1_delay-0.1s.gif")), (100,100))
loader_03 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_2_delay-0.1s.gif")), (100,100))
loader_04 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_3_delay-0.1s.gif")), (100,100))
loader_05 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_4_delay-0.1s.gif")), (100,100))
loader_06 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_5_delay-0.1s.gif")), (100,100))
loader_07 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_6_delay-0.1s.gif")), (100,100))
loader_08 = pygame.transform.scale(pygame.image.load(os.path.join('assets/loader', "frame_7_delay-0.1s.gif")), (100,100))


# Button
button = pygame.image.load(os.path.join("assets/icons", "button.png"))
button_dark = pygame.image.load(os.path.join("assets/icons", "button_dark.png"))
button_green = pygame.image.load(os.path.join("assets/icons", "button_green.png"))
button_lineage = pygame.image.load(os.path.join("assets/icons", "button_lineage.png"))

# Android logo
aosp = pygame.transform.scale(pygame.image.load(os.path.join("assets/icons", "aosp.png")), (150, 80))

# Los Animation
los = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_010_delay-0.05s.gif")), (1000, 400))
