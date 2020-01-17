import pygame
from os import listdir
from os.path import isfile, join
from menu_button import *
from consts import *
from level_editor import level_editor
from main_game import main_cycle


def level_chooser(screen, clock, is_game_running=False):
    window_size = (WIDTH, HEIGHT)
    running = True
    is_player_chooser = False
    game_file_name = ''
    game_size = 10

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
        new_level_msg = 'Create new level'
        if is_game_running:
            new_level_msg = ''
        draw_text(screen, new_level_msg, 5, top, WIDTH)
        level_button_width = 110
        level_button_padding = (WIDTH - 10) // 4
        x = 5
        if not is_game_running:
            top += MENUBUTTONHEIGHT * 1.5
            draw_button(screen, "Small", x, top, level_button_width, create_new_level, ('', 10))
            x += level_button_padding
            draw_button(screen, "Medium", x, top, level_button_width, create_new_level, ('', 20))
            x += level_button_padding
            draw_button(screen, "Large", x, top, level_button_width, create_new_level, ('', 35))
            x += level_button_padding
            draw_button(screen, "Extralarge", x, top, level_button_width, create_new_level, ('', 50))
            top += MENUBUTTONHEIGHT * 1.5
        onlyfiles = [f for f in listdir('levels') if isfile(join('levels', f))]
        if len(onlyfiles) == 0:
            return
        existing_level_msg = 'Edit existing levels'
        if is_game_running:
            existing_level_msg = 'Play existing levels'
        draw_text(screen, existing_level_msg, 5, top, WIDTH)
        for file in onlyfiles:
            top += MENUBUTTONHEIGHT * 1.5
            draw_button(screen, file, 5, top, MENUBUTTONWIDTH, create_new_level, (file, 0))

    def menu_player_buttons(top):
        draw_text(screen, 'Choose players', 5, top, WIDTH)
        top += MENUBUTTONHEIGHT * 2
        draw_button(screen, "One player", WIDTH // 2 + 45, top, MENUBUTTONWIDTH, choose_players, 1)
        top += MENUBUTTONHEIGHT * 1.5
        draw_button(screen, "Two players", WIDTH // 2 + 45, top, MENUBUTTONWIDTH, choose_players, 2)

    def menu_buttons():
        draw_button(screen, "Back to Menu", 5, 5, MENUBUTTONWIDTH, back_to_mainMenu)
        top = MENUBUTTONHEIGHT * 1.5 + 5
        if is_player_chooser:
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
                game_file_name = event.file
                game_size = event.size
                if is_game_running:
                    is_player_chooser = True
                else:
                    running = False
                    level_editor(game_size, screen, clock, game_file_name)
            if event.type == CHOOSEPLAYERS:
                players = event.players
                running = False
                main_cycle(game_file_name, players == 2, screen, clock)
        pygame.draw.rect(screen, (255, 255, 255), ((0, 0), window_size))
        menu_buttons()
        pygame.display.flip()
