import pygame
import os
#import sys

pygame.init()
player_group = pygame.sprite.Group()
player1 = None
player2 = None
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
        if not flag:
            self.image = Player.image1
            self.rect = self.image.get_rect()
        else:
            self.image = Player.image2
            self.rect = self.image.get_rect()



all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = tile_height = 50

#class Tile(pygame.sprite.Sprite):
    #def __init__(self, tile_type, pos_x, pos_y):
        #super().__init__(tiles_group, all_sprites)
        #self.image = tile_images[tile_type]
        #self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

running = True
clock = pygame.time.Clock()
IsStart = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            IsStart = True
    if flag == 1:
        if IsStart:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                player1.update((-tile_width, 0))
            if pressed[pygame.K_RIGHT]:
                player1.update((tile_width, 0))
            if pressed[pygame.K_UP]:
                player1.update((0, tile_width))
            if pressed[pygame.K_DOWN]:
                player1.update((0, tile_width))

    else:
        if IsStart:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                player2.update((-tile_width, 0))
            if pressed[pygame.K_RIGHT]:
                player2.update((tile_width, 0))
            if pressed[pygame.K_UP]:
                player2.update((0, tile_height))
            if pressed[pygame.K_DOWN]:
                player2.update((0, tile_height))


    #screen.fill(pygame.Color(0, 0, 0))
    #tiles_group.draw(screen)
    #player_group.draw(screen)
    #pygame.display.flip()
    #clock.tick(FPS)