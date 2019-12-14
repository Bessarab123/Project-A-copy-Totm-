import pygame
import os

WALL = 0
EMPTY = 1
EXIT = 3
ENTER = 2
COIN = 4

class BoardEditor():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[EMPTY] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        y = self.top
        for i in range(self.height):
            x = self.left
            for j in range(self.width):
                width = 0 if self.board[i][j] == 0 else 1
                pygame.draw.rect(screen, (255, 0, 255), (x, y, self.cell_size, self.cell_size), width)
                # TODO Сделать красивае рисование с условиями
                x += self.cell_size
            y += self.cell_size

    def on_click(self, cell_coords):
        j, i = cell_coords
        self.board[i][j] += 1
        if self.board[i][j] == COIN + 1:
            self.board[i][j] = WALL

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

def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image

pygame.init()
w = 800
h = 600
screen = pygame.display.set_mode((w, h))
board = BoardEditor(w // 30, h // 30)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
