import pygame
import sys

WIDTH = 500
HEIGHT = 500
MENUACTIVECOLOR = (255, 0, 0)
MENUINACTIVECOLOR = (0, 255, 0)
MENUBUTTONWIDTH = 200
MENUBUTTONHEIGHT = 30


def terminate():
    pygame.quit()
    sys.exit()


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def menu_button(msg, buttonTop, action=None):
    x = (WIDTH - MENUBUTTONWIDTH) // 2
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + MENUBUTTONWIDTH > mouse[0] > x and buttonTop + MENUBUTTONHEIGHT > mouse[1] > buttonTop:
        pygame.draw.rect(screen, MENUACTIVECOLOR, (x, buttonTop, MENUBUTTONWIDTH, MENUBUTTONHEIGHT))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, MENUINACTIVECOLOR, (x, buttonTop, MENUBUTTONWIDTH, MENUBUTTONHEIGHT))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (MENUBUTTONWIDTH // 2)), (buttonTop + (MENUBUTTONHEIGHT // 2)))
    screen.blit(textSurf, textRect)


runningStatus = "menu"


def menu_buttons():
    buttonCount = 4
    top = (HEIGHT - buttonCount * MENUBUTTONHEIGHT - (buttonCount - 1) * MENUBUTTONHEIGHT // 2) // 2
    menu_button("Start Game", top, menu_startGame)
    top += MENUBUTTONHEIGHT * 1.5
    menu_button("Settings", top, menu_settings)
    top += MENUBUTTONHEIGHT * 1.5
    menu_button("Level Generator", top, menu_levelGenerator)
    top += MENUBUTTONHEIGHT * 1.5
    menu_button("Exit", top, terminate)


def menu_startGame():
    global runningStatus
    runningStatus = "game"


def menu_settings():
    global runningStatus
    runningStatus = "settings"


def menu_levelGenerator():
    global runningStatus
    runningStatus = "levelgenerator"


running = True
windowSize = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(windowSize)
pygame.font.init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.draw.rect(screen, (255, 255, 255), ((0, 0), windowSize))
    if runningStatus == "menu":
        menu_buttons()
    else:
        # game code runningStatus == game or settings or levelgenerator
        pygame.draw.rect(screen, (155, 155, 155), ((0, 0), windowSize))

    pygame.display.flip()
