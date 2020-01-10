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

    def create_new_level(params):
        ev = pygame.event.Event(CREATENEWLEVEL, {'file': params[0], 'size': params[1]})
        pygame.event.post(ev)

    def menu_buttons():
        draw_button(screen, "Back to Menu", 5, 5, MENUBUTTONWIDTH, back_to_mainMenu)
        top = MENUBUTTONHEIGHT * 1.5 + 5
        draw_text(screen, 'Create new level', 5, top, WIDTH)
        top += MENUBUTTONHEIGHT * 1.5
        levelButtonWidth = 110
        levelButtonPadding = (WIDTH - 10) // 4
        x = 5
        draw_button(screen, "Small", x, top, levelButtonWidth, create_new_level, ('', 10))
        x += levelButtonPadding
        draw_button(screen, "Medium", x, top, levelButtonWidth, create_new_level, ('', 20))
        x += levelButtonPadding
        draw_button(screen, "Large", x, top, levelButtonWidth, create_new_level, ('', 35))
        x += levelButtonPadding
        draw_button(screen, "Extralarge", x, top, levelButtonWidth, create_new_level, ('', 50))
        onlyfiles = [f for f in listdir('levels') if isfile(join('levels', f))]
        if len(onlyfiles) == 0:
            return
        top += MENUBUTTONHEIGHT * 1.5
        draw_text(screen, 'Edit existing levels', 5, top, WIDTH)
        for file in onlyfiles:
            top += MENUBUTTONHEIGHT * 1.5
            draw_button(screen, file, 5, top, MENUBUTTONWIDTH, create_new_level, (file, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == GOTOMAINMENU:
                running = False
            if event.type == CREATENEWLEVEL:
                running = False
                fileName = event.file
                size = event.size
                level_editor(5, 5, screen, clock, fileName, size)

        pygame.draw.rect(screen, (255, 255, 255), ((0, 0), windowSize))
        menu_buttons()
        pygame.display.flip()
