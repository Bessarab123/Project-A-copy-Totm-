from Player import create_player
import pygame
import os
import random

WALL = 0
EMPTY = 1
ENTER = 2
EXIT = 3
COIN = 4
STEP = 1
FPS = 240
BLACK = pygame.Color('black')


def main_cycle(name_file, two_players, screen, clock):
    width = screen.get_rect().w
    height = screen.get_rect().h
    UPDATE_SPRITES = 30
    pygame.time.set_timer(UPDATE_SPRITES, 1000)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()

    wall_sprites_dict = dict()
    enter_sprites_dict = dict()
    exit_sprites_dict = dict()
    coin_sprites_dict = dict()

    def load_image(name):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (board.get_cell_size(), board.get_cell_size()))
        image.set_colorkey(BLACK)
        return image

    class Board:
        def __init__(self, name):
            self.x = 0
            self.y = 0
            self.cell_size = 32
            self.open_board(name)

        def set_cell_size(self, cell_size):
            '''Изменить размер клетки'''
            self.cell_size = cell_size

        def get_cell_size(self):
            return self.cell_size

        def render(self):
            '''Обновить все объекты на поле'''
            all_sprites.empty()
            y = self.y
            for i in range(self.height):
                x = self.x
                for j in range(self.width):
                    if self.board[i][j]:
                        # Если не стена то:
                        if self.board[i][j] == COIN:
                            coin_sprites_dict[(i, j)] = Coin(x, y, all_sprites, coin_group)
                        elif self.board[i][j] == EXIT:
                            exit_sprites_dict[(i, j)] = Exit(x, y, all_sprites, exit_group)
                        elif self.board[i][j] == ENTER:
                            enter_sprites_dict[(i, j)] = Enter(x, y, all_sprites)
                    else:
                        # Если стена:
                        wall_sprites_dict[(i, j)] = []
                        # Логика того как должна прорисоваться стена
                        if j - 1 > -1 and self.board[i][j - 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 270, all_sprites, wall_group))
                        if j + 1 < self.width and self.board[i][j + 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 90, all_sprites, wall_group))
                        if i - 1 > - 1 and self.board[i - 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 180, all_sprites, wall_group))
                        if i + 1 < self.height and self.board[i + 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 0, all_sprites, wall_group))
                    x += self.cell_size
                y += self.cell_size

        def open_board(self, name):
            '''Открывает доску из указанного файла'''
            file = open('levels/' + name)
            self.board = list(map(lambda x: list(map(int, x.split())), file.read().split('\n')))
            self.width = len(self.board[0])
            self.height = len(self.board)
            file.close()

    board = Board(name_file)

    class Sprites(pygame.sprite.Sprite):
        '''Общий класс всех спрайтов'''
        empty_im = load_image('Empty.png')

        def __init__(self, x, y, *group):
            super().__init__(group)
            self.image = Sprites.empty_im
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def move_sprite(self, move):
            if move == 'UP':
                self.y -= STEP
            elif move == 'DOWN':
                self.y += STEP
            elif move == 'RIGHT':
                self.x += STEP
            elif move == 'LEFT':
                self.x -= STEP

    class Wall(Sprites):
        '''Класс стены'''
        wall_1 = load_image('WALL_1.png')
        wall_2 = load_image('WALL_2.png')

        def __init__(self, x, y, alpha, *group):
            super().__init__(x, y, group)
            self.image = pygame.transform.rotate(random.choice((Wall.wall_1, Wall.wall_2)), alpha)

    class Enter(Sprites):
        '''Клласс входа'''
        enter_im = load_image('enter.png')

        def __init__(self, x, y, *group):
            super().__init__(x, y, group)
            self.image = Enter.enter_im

    class Exit(Sprites):
        '''Класс выхода'''
        exit_im_1 = load_image('exit1.png')
        exit_im_2 = load_image('exit2.png')

        def __init__(self, x, y, *group):
            super().__init__(x, y, group)
            self.image = Exit.exit_im_1

        def update(self, *args):
            if self.image is Exit.exit_im_1:
                self.image = Exit.exit_im_2
            else:
                self.image = Exit.exit_im_1

    class Coin(Sprites):
        '''Класс монетки'''
        coin_im = load_image('coin.png')

        def __init__(self, x, y, *group):
            super().__init__(x, y, group)
            self.image = Coin.coin_im
            self.mask = pygame.mask.from_surface(self.image)

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 1
            self.dy = 1

        # сдвинуть объект obj на смещение камеры
        def apply(self, obj):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

        # позиционировать камеру на объекте target
        def update(self, target):
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
            self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

        def update2(self, x, y):
            self.dx = -(x - width // 2)
            self.dy = -(y - height // 2)

    board.render()
    list_cell_pos_enter = list(
        map(lambda x: (x[1] * board.get_cell_size(), x[0] * board.get_cell_size()), enter_sprites_dict.keys()))
    plr_list = [create_player(board, random.choice(list_cell_pos_enter), 0, player_group, all_sprites)]
    if two_players:
        plr_list.append(create_player(board, random.choice(list_cell_pos_enter), 1, player_group, all_sprites))
    camera = Camera()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == UPDATE_SPRITES:
                all_sprites.update()
            elif pygame.key.get_pressed()[pygame.K_UP]:
                if not plr_list[0].move:
                    plr_list[0].set_move(True, 'UP')
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if not plr_list[0].move:
                    plr_list[0].set_move(True, 'DOWN')
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                if not plr_list[0].move:
                    plr_list[0].set_move(True, 'RIGHT')
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if not plr_list[0].move:
                    plr_list[0].set_move(True, 'LEFT')
            if two_players:
                if pygame.key.get_pressed()[pygame.K_w]:
                    if not plr_list[1].move:
                        plr_list[1].set_move(True, 'UP')
                elif pygame.key.get_pressed()[pygame.K_s]:
                    if not plr_list[1].move:
                        plr_list[1].set_move(True, 'DOWN')
                elif pygame.key.get_pressed()[pygame.K_d]:
                    if not plr_list[1].move:
                        plr_list[1].set_move(True, 'RIGHT')
                elif pygame.key.get_pressed()[pygame.K_a]:
                    if not plr_list[1].move:
                        plr_list[1].set_move(True, 'LEFT')

        if pygame.sprite.spritecollide(plr_list[0], wall_group, False):
            plr_list[0].step_back()
            plr_list[0].set_move(False)
        if pygame.sprite.spritecollide(plr_list[1], wall_group, False):
            plr_list[1].step_back()
            plr_list[1].set_move(False)

        for coin in coin_group:
            if pygame.sprite.collide_mask(plr_list[0], coin):
                coin.kill()
                # Можно вести подсчёт очков
            if pygame.sprite.collide_mask(plr_list[1], coin):
                coin.kill()
        plr_list[0].moves()
        plr_list[1].moves()
        if two_players:
            camera.update2((plr_list[0].rect.x + plr_list[1].rect.x + board.get_cell_size()) // 2,
                           (plr_list[0].rect.y + plr_list[1].rect.y + board.get_cell_size()) // 2)
        else:
            camera.update(plr_list[0])
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(BLACK)
        all_sprites.draw(screen)
        # Прямоугольник в котором можно работать
        clock.tick(FPS)
        pygame.display.flip()
