import pygame
import os


def create_player(board, player_pos, flag, player_group, all_sprites):
    def load_image(name):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (board.get_cell_size(), board.get_cell_size()))
        image.set_colorkey((0, 0, 0))
        return image

    class Player(pygame.sprite.Sprite):
        image10 = load_image('totem10.png')
        image11 = load_image('totem11.png')
        image12 = load_image('totem12.png')
        image13 = load_image('totem13.png')
        image20 = load_image('totem20.png')
        image21 = load_image('totem21.png')
        image22 = load_image('totem22.png')
        image23 = load_image('totem23.png')

        def __init__(self, pos, flag=0):
            super().__init__([player_group, all_sprites])
            self.flag = flag
            self.move = False
            self.direction = None
            if not self.flag:
                self.image = Player.image10
                self.rect = self.image.get_rect()
                self.rect.x = pos[0]
                self.rect.y = pos[1]
            else:
                self.image = Player.image20
                self.rect = self.image.get_rect()
                self.rect.x = pos[0]
                self.rect.y = pos[1]

        def set_move(self, move, direction=None):
            self.move = move
            self.direction = direction

        def moves(self):
            if self.move:
                if self.direction == 'RIGHT':
                    self.rect.x += 1
                elif self.direction == 'LEFT':
                    self.rect.x -= 1
                elif self.direction == 'UP':
                    self.rect.y -= 1
                elif self.direction == 'DOWN':
                    self.rect.y += 1

        def step_back(self):
            if self.direction == 'RIGHT':
                self.rect.x -= 1
            elif self.direction == 'LEFT':
                self.rect.x += 1
            elif self.direction == 'UP':
                self.rect.y += 1
            elif self.direction == 'DOWN':
                self.rect.y -= 1

        def update(self, *args):
            if not self.flag:
                if self.image is self.image10:
                    self.image = self.image11
                elif self.image is self.image11:
                    self.image = self.image12
                elif self.image is self.image12:
                    self.image = self.image13
                elif self.image is self.image13:
                    self.image = self.image10
            else:
                if self.image is self.image20:
                    self.image = self.image21
                elif self.image is self.image21:
                    self.image = self.image22
                elif self.image is self.image22:
                    self.image = self.image23
                elif self.image is self.image23:
                    self.image = self.image20

    return Player(player_pos, flag)
