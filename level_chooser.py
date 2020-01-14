import pygame
from os import listdir
from os.path import isfile, join
import sys
from menu_button import *
from consts import *
from level_editor import level_editor
from main_game import main_cycle


def level_chooser(screen, clock, isGameRunning=False):
    windowSize = (WIDTH, HEIGHT)
    running = True
    isPlayerChooser = False
    gameFileName = ''
    gameSize = 10

    def back_to_mainMenu():
        ev = pygame.event.Event(GOTOMAINMENU)
        pygame.event.post(ev)

    def create_new_level(params):
        ev = pygame.event.Event(CREATENEWLEVEL, {'file': params[0], 'size': params[1]})
        pygame.event.post(ev)
    def choose_players(params):
        ev = pygame.event.Event(CHOOSEPLAYERS, {'players': params})
        pygame.event.post(ev)

    def menu_level_buttons(top):
        newLevelMsg = 'Create new level'
        if isGameRunning:
            newLevelMsg = 'Play new level'
        draw_text(screen, newLevelMsg, 5, top, WIDTH)
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
        existingLevelMsg = 'Edit existing levels'
        if isGameRunning:
            existingLevelMsg = 'Play existing levels'
        draw_text(screen, existingLevelMsg, 5, top, WIDTH)
        for file in onlyfiles:
            top += MENUBUTTONHEIGHT * 1.5
            draw_button(screen, file, 5, top, MENUBUTTONWIDTH, create_new_level, (file, 0))

    def menu_player_buttons(top):
        draw_text(screen, 'Choose players', 5, top, WIDTH)
        top += MENUBUTTONHEIGHT * 2
        menu_button(screen, "One player", top, choose_players,1)
        top += MENUBUTTONHEIGHT * 1.5
        menu_button(screen, "Two players", top, choose_players,2)

    def menu_buttons():
        draw_button(screen, "Back to Menu", 5, 5, MENUBUTTONWIDTH, back_to_mainMenu)
        top = MENUBUTTONHEIGHT * 1.5 + 5
        if isPlayerChooser:
            menu_player_buttons(top)
        else:
            menu_level_buttons(top)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == GOTOMAINMENU:
                running = False
            if event.type == CREATENEWLEVEL:
                gameFileName = event.file
                gameSize = event.size
                if isGameRunning:
                    isPlayerChooser = True
                else:
                    running = False
                    level_editor(gameSize, gameSize, screen, clock, gameFileName)
            if event.type == CHOOSEPLAYERS:
                players = event.players
                running = False
                main_cycle(gameFileName, players == 2, gameSize, screen, clock)
        pygame.draw.rect(screen, (255, 255, 255), ((0, 0), windowSize))
        menu_buttons()
        pygame.display.flip()
