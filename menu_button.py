import pygame
from consts import WIDTH, HEIGHT

MENUACTIVECOLOR = (255, 0, 0)
MENUINACTIVECOLOR = (0, 255, 0)
MENUBUTTONWIDTH = 200
MENUBUTTONHEIGHT = 30


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def draw_text(screen, msg, x, y, width):
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (width // 2)), (y + (MENUBUTTONHEIGHT // 2)))
    screen.blit(textSurf, textRect)


def draw_button(screen, msg, buttonLeft, buttonTop, buttonWidth, action=None, actionParam=None):
    x = buttonLeft
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x +  buttonWidth > mouse[0] > x and buttonTop + MENUBUTTONHEIGHT > mouse[1] > buttonTop:
        pygame.draw.rect(screen, MENUACTIVECOLOR, (x, buttonTop, buttonWidth, MENUBUTTONHEIGHT))

        if click[0] == 1 and action != None:
            if actionParam != None:
                action(actionParam)
            else:
                action()
    else:
        pygame.draw.rect(screen, MENUINACTIVECOLOR, (x, buttonTop, buttonWidth, MENUBUTTONHEIGHT))
    draw_text(screen, msg, x, buttonTop, buttonWidth)


def menu_button(screen, msg, buttonTop, action=None, actionParams=None):
    x = (WIDTH - MENUBUTTONWIDTH) // 2
    draw_button(screen, msg, x, buttonTop,MENUBUTTONWIDTH, action,actionParams)
