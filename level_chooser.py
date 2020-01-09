import pygame
from os import listdir
from os.path import isfile, join
import sys
from menu_button import *
from consts import *
from Board import level_editor


def level_chooser(screen, clock):
    windowSize = (WIDTH, HEIGHT)
    running = True

    def back_to_mainMenu():
        ev = pygame.event.Event(GOTOMAINMENU)
        pygame.event.post(ev)

    def create_new_level(filename):
        ev = pygame.event.Event(CREATENEWLEVEL, {'file': filename})
        pygame.event.post(ev)

    def menu_buttons():
        draw_button(screen, "Back to Menu", 5, 5, back_to_mainMenu)
        top = MENUBUTTONHEIGHT * 1.5 + 5
        draw_button(screen, "Create new level", 5, top, create_new_level, '')
        onlyfiles = [f for f in listdir('levels') if isfile(join('levels', f))]
        for file in onlyfiles:
            top += MENUBUTTONHEIGHT * 1.5
            draw_button(screen, "Edit " + file, 5, top, create_new_level, file)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == GOTOMAINMENU:
                running = False
            if event.type == CREATENEWLEVEL:
                running = False
                fileName = event.file
                level_editor(5, 5, screen, clock, fileName)

        pygame.draw.rect(screen, (255, 255, 255), ((0, 0), windowSize))
        menu_buttons()
        pygame.display.flip()
