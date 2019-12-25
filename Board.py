import pygame
import os
import random

WALL = 0
EMPTY = 1
EXIT = 3
ENTER = 2
COIN = 4
BLACK = pygame.Color('black')

pygame.init()
w = 800
h = 600
screen = pygame.display.set_mode((w, h))


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    image.set_colorkey(BLACK)
    return image


class BoardEditor():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[EMPTY] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 32

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        y = self.top
        for i in range(self.height): 0
        x = self.left
        for j in range(self.width):
            if self.board[i][j]:
                pass
            else:
                # Если стена
                if j - 1 > -1 and not self.board[i][j - 1]:
                    pass
                elif j + 1 < self.width + 1 and not self.board[i][j + 1]:
                    pass  # TODO

            x += self.cell_size
        y += self.cell_size


def on_click(self, cell_coords):
    j, i = cell_coords
    press = pygame.key.get_pressed()
    if any(press):
        # Если нажата хоть одна клавиша
        if press[pygame.K_0]:
            self.board[i][j] = 0
        elif press[pygame.K_1]:
            self.board[i][j] = 1
        elif press[pygame.K_2]:
            self.board[i][j] = 2
        elif press[pygame.K_3]:
            self.board[i][j] = 3
        elif press[pygame.K_4]:
            self.board[i][j] = 4
    else:
        # Если ни одна клавиша не нажата
        self.board[i][j] += 1
        if self.board[i][j] == COIN + 1:
            self.board[i][j] = WALL
    self.render(screen)


def get_click(self, mouse_pos):
    cell_coords = self.get_cell(mouse_pos)
    if cell_coords:
        self.on_click(cell_coords)


def get_cell(self, mouse_pos):
    x, y = mouse_pos
    x1 = (x - self.left) // self.cell_size
    y1 = (y - self.top) // self.cell_size
    if x1 < 0 or x1 >= self.width:
        return None
    if y1 < 0 or y1 >= self.height:
        return None
    return x1, y1


class Sprites(pygame.sprite.Sprite):
    empty_im = load_image('Empty.png')

    def __init__(self, x, y, *group):
        super().__init__(group)
        self.image = Sprites.empty_im
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall(Sprites):
    wall_1 = load_image('WALL_1.png')
    wall_2 = load_image('WALL_2.png')

    def __init__(self, x, y, alpha, *group):
        super().__init__(x, y, group)
        self.image = pygame.transform.rotate(random.choice((Wall.wall_1, Wall.wall_2)), alpha)


class Coin(Sprites):
    coin_im = load_image('coin.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, group)
        self.image = Coin.coin_im


all_sprites = pygame.sprite.Group()
wall_sprites_list = []

board = BoardEditor(w // 32, h // 32)
Wall(50, 50, 0, all_sprites)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            board.get_click(event.pos)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
