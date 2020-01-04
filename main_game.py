from Player import Player
import pygame
import os
import random


def main_cycle(name_file, two_players, screen, clock):
    WALL = 0
    EMPTY = 1
    ENTER = 2
    EXIT = 3
    COIN = 4
    BLACK = pygame.Color('black')
    UPDATE_SPRITES = 30
    clock.set_timer(UPDATE_SPRITES, 1000)

    STEP = 1
    FPS = 60

    ENTER_POS = []

    all_sprites = pygame.sprite.Group()
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
                            Coin(x, y, all_sprites)
                            coin_sprites_dict[(i, j)] = Coin(x, y, all_sprites)
                        elif self.board[i][j] == EXIT:
                            exit_sprites_dict[(i, j)] = Exit(x, y, all_sprites)
                        elif self.board[i][j] == ENTER:
                            enter_sprites_dict[(i, j)] = Enter(x, y, all_sprites)
                    else:
                        # Если стена:
                        self.kill_wall(i, j)
                        wall_sprites_dict[(i, j)] = []
                        # Логика того как должна прорисоваться стена
                        if j - 1 > -1 and self.board[i][j - 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 270, all_sprites))
                        if j + 1 < self.width and self.board[i][j + 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 90, all_sprites))
                        if i - 1 > - 1 and self.board[i - 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 180, all_sprites))
                        if i + 1 < self.height and self.board[i + 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 0, all_sprites))
                    x += self.cell_size
                y += self.cell_size

        def kill_wall(self, i, j):
            if (i, j) in wall_sprites_dict.keys():
                for wall in wall_sprites_dict[(i, j)]:
                    wall.kill()

        def open_board(self, name):
            '''Открывает доску из указанного файла'''
            file = open('levels/' + name)
            self.board = list(map(lambda x: list(map(int, x.split())), file.read().split('\n')))
            self.width = len(self.board[0])
            self.height = len(self.board)
            file.close()
            self.render()

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

    board = Board(name_file)
    list_cell_pos_enter = list(map(lambda x: (x[0] * board.get_cell_size(), x[1] * board.get_cell_size()),enter_sprites_dict.keys()))
    player_list = [Player(random.choices(list_cell_pos_enter))]
    if two_players:
        player_list.append(Player(random.choices(list_cell_pos_enter)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == UPDATE_SPRITES:
                all_sprites.update()

        screen.fill(BLACK)
        all_sprites.draw(screen)
        # Прямоугольник в котором можно работать
        pygame.draw.rect(screen, (139, 0, 255),
                         [board.x, board.y,
                          board.cell_size * board.width, board.height * board.cell_size], 1)
        clock.tick(FPS)
        pygame.display.flip()
