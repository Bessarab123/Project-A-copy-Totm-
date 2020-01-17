import pygame
import sys
import os
from menu_button import *
from level_chooser import level_chooser


def terminate():
    pygame.quit()
    sys.exit()


def menu_buttons():
    button_count = 4
    top = (HEIGHT - button_count * MENUBUTTONHEIGHT - (button_count - 1) * MENUBUTTONHEIGHT // 2) // 2
    menu_button(screen, "Start Game", top, menu_start_game)
    top += MENUBUTTONHEIGHT * 1.5
    menu_button(screen, "Level Generator", top, menu_level_generator)
    top += MENUBUTTONHEIGHT * 1.5
    menu_button(screen, "Exit", top, terminate)


def menu_start_game():
    global runningStatus
    runningStatus = "game"


def menu_level_generator():
    global runningStatus
    runningStatus = "levelchooser"


pygame.init()
pygame.mixer.init()
runningStatus = "menu"
clock = pygame.time.Clock()
running = True
windowSize = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(windowSize)
pygame.font.init()
pygame.mixer.music.load('super-mario-boss-boss-muzyka-iz-igry-nintendo.mp3')
pygame.mixer.music.play(-1)
try:
    open('levels')
except PermissionError:
    pass
except FileNotFoundError:
    os.makedirs('levels')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.draw.rect(screen, (255, 255, 255), ((0, 0), windowSize))
    if runningStatus == "menu":
        menu_buttons()
    elif runningStatus == "game":
        level_chooser(screen, clock, True)
        screen = pygame.display.set_mode(windowSize)
        runningStatus = "menu"
    elif runningStatus == 'levelchooser':
        level_chooser(screen, clock)
        runningStatus = 'menu'
    else:
        pygame.draw.rect(screen, (155, 155, 155), ((0, 0), windowSize))

    pygame.display.flip()
