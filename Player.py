import pygame
import os
#import sys

def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
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
        self.pos = pos
        self.flag = flag
        self.move = False
        if not self.flag:
            self.player_image = Player.image10
            self.rect = self.player_image.get_rect()
        else:
            self.player_image  = Player.image20
            self.rect = self.player_image.get_rect()

    def set_move(self, move, direction=None):
        if move:
            if direction == RIGHT:
                self.rect.x += 1
            elif direction == LEFT:
                self.rect.x -= 1
            elif direction == UP:
                self.rect.y -= 1
            elif direction == DOWN:
                self.rect.y += 1

    def update(self, *args):
        if not self.flag:
            if self.player_image is self.image10:
                self.player_image = self.image11
            elif self.player_image is self.image11:
                self.player_image = self.image12
            elif self.player_image is self.image12:
                self.player_image = self.image13
            elif self.player_image is self.image13:
                self.player_image = self.image10
        else:
            if self.player_image is self.image20:
                self.player_image = self.image21
            elif self.player_image is self.image21:
                self.player_image = self.image22
            elif self.player_image is self.image22:
                self.player_image = self.image23
            elif self.player_image is self.image23:
                self.player_image = self.image20





