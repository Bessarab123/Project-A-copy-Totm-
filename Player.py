import pygame
import os
from consts import STEP


def create_player(board, player_pos, flag, player_group, all_sprites):
    def load_image(name):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (board.get_cell_size(), board.get_cell_size()))
        image.set_colorkey((0, 0, 0))
        return image

    class Player(pygame.sprite.Sprite):
        image10_RIGHT = load_image('totem10.png')
        image11_RIGHT = load_image('totem11.png')
        image12_RIGHT = load_image('totem12.png')
        image13_RIGHT = load_image('totem13.png')
        image10_LEFT = pygame.transform.flip(image10_RIGHT, True, False)
        image11_LEFT = pygame.transform.flip(image11_RIGHT, True, False)
        image12_LEFT = pygame.transform.flip(image12_RIGHT, True, False)
        image13_LEFT = pygame.transform.flip(image13_RIGHT, True, False)
        image20_RIGHT = load_image('totem20.png')
        image21_RIGHT = load_image('totem21.png')
        image22_RIGHT = load_image('totem22.png')
        image23_RIGHT = load_image('totem23.png')
        image20_LEFT = pygame.transform.flip(image20_RIGHT, True, False)
        image21_LEFT = pygame.transform.flip(image21_RIGHT, True, False)
        image22_LEFT = pygame.transform.flip(image22_RIGHT, True, False)
        image23_LEFT = pygame.transform.flip(image23_RIGHT, True, False)

        def __init__(self, pos, flag=0):
            super().__init__([player_group, all_sprites])
            self.flag = flag
            self.move = False
            self.direction = None
            self.num_im = 0
            if not self.flag:
                self.image = Player.image10_RIGHT
                self.rect = self.image.get_rect()
                self.rect.x = pos[0]
                self.rect.y = pos[1]
            else:
                self.image = Player.image20_LEFT
                self.rect = self.image.get_rect()
                self.rect.x = pos[0]
                self.rect.y = pos[1]

        def set_move(self, move, direction=None):
            self.move = move
            self.direction = direction

        def moves(self):
            if self.move:
                if self.direction == 'RIGHT':
                    self.rect.x += STEP
                elif self.direction == 'LEFT':
                    self.rect.x -= STEP
                elif self.direction == 'UP':
                    self.rect.y -= STEP
                elif self.direction == 'DOWN':
                    self.rect.y += STEP

        def step_back(self):
            if self.direction == 'RIGHT':
                self.rect.x -= STEP
            elif self.direction == 'LEFT':
                self.rect.x += STEP
            elif self.direction == 'UP':
                self.rect.y += STEP
            elif self.direction == 'DOWN':
                self.rect.y -= STEP

        def update(self, *args):
            if not self.flag:
                if self.num_im == 0:
                    if self.direction == 'LEFT':
                        self.image = self.image10_LEFT
                    else:
                        self.image = self.image10_RIGHT
                    self.num_im += 1
                elif self.num_im == 1:
                    if self.direction == 'LEFT':
                        self.image = self.image11_LEFT
                    else:
                        self.image = self.image11_RIGHT
                    self.num_im += 1
                elif self.num_im == 2:
                    if self.direction == 'LEFT':
                        self.image = self.image12_LEFT
                    else:
                        self.image = self.image12_RIGHT
                    self.num_im += 1
                elif self.num_im == 3:
                    if self.direction == 'LEFT':
                        self.image = self.image13_LEFT
                    else:
                        self.image = self.image13_RIGHT
                    self.num_im = 0
            else:
                if self.num_im == 0:
                    if self.direction == 'RIGHT':
                        self.image = self.image20_RIGHT
                    else:
                        self.image = self.image20_LEFT
                    self.num_im += 1
                elif self.num_im == 1:
                    if self.direction == 'RIGHT':
                        self.image = self.image21_RIGHT
                    else:
                        self.image = self.image21_LEFT
                    self.num_im += 1
                elif self.num_im == 2:
                    if self.direction == 'RIGHT':
                        self.image = self.image22_RIGHT
                    else:
                        self.image = self.image22_LEFT
                    self.num_im += 1
                elif self.num_im == 3:
                    if self.direction == 'RIGHT':
                        self.image = self.image23_RIGHT
                    else:
                        self.image = self.image23_LEFT
                    self.num_im = 0

    return Player(player_pos, flag)
