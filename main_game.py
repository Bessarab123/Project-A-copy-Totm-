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
FPS = 60
BLACK = pygame.Color('black')


def main_cycle(name_file, two_players, screen, clock):
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
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 270, True, all_sprites, wall_group))
                        if j + 1 < self.width and self.board[i][j + 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 90, True, all_sprites, wall_group))
                        if i - 1 > - 1 and self.board[i - 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 180, True, all_sprites, wall_group))
                        if i + 1 < self.height and self.board[i + 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 0, True, all_sprites, wall_group))

                        if (i + 1 < self.height and not self.board[i + 1][j] and
                                j - 1 > -1 and not self.board[i][j - 1] and self.board[i + 1][j - 1]):
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 270, False, all_sprites, wall_group))
                        if (j + 1 < self.width and not self.board[i][j + 1] and
                                i - 1 > - 1 and not self.board[i - 1][j] and self.board[i - 1][j + 1]):
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 90, False, all_sprites, wall_group))
                        if (j + 1 < self.width and not self.board[i][j + 1] and
                                i + 1 < self.height and not self.board[i + 1][j] and self.board[i + 1][j + 1]):
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 0, False, all_sprites, wall_group))
                        if (j - 1 > -1 and not self.board[i][j - 1] and
                                i - 1 > - 1 and not self.board[i - 1][j] and self.board[i - 1][j - 1]):
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 180, False, all_sprites, wall_group))
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

    class Wall(Sprites):
        '''Класс стены'''
        wall_1 = load_image('WALL_1.png')
        wall_2 = load_image('WALL_2.png')
        wall_3 = load_image('WAll_3.png')

        def __init__(self, x, y, alpha, wall, *group):
            super().__init__(x, y, group)
            if wall:
                self.image = pygame.transform.rotate(random.choice((Wall.wall_1, Wall.wall_2)), alpha)
            else:
                self.image = pygame.transform.rotate(Wall.wall_3, alpha)

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
            self.dx = 0
            self.dy = 0

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

    width = screen.get_rect().w
    height = screen.get_rect().h
    board.render()
    font = pygame.font.Font(None, 24)
    point_1 = 0 # Очки
    list_cell_pos_enter = list(
        map(lambda x: (x[1] * board.get_cell_size(), x[0] * board.get_cell_size()), enter_sprites_dict.keys()))
    plr_list = [create_player(board, random.choice(list_cell_pos_enter), 0, player_group, all_sprites)]
    if two_players:
        # Если два игрока
        point_2 = 0
        plr_list.append(create_player(board, random.choice(list_cell_pos_enter), 1, player_group, all_sprites))
    camera = Camera()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == UPDATE_SPRITES:
                all_sprites.update()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                screen = pygame.display.set_mode((width, height))
            elif pygame.key.get_pressed()[pygame.K_f]:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Определить направление движения
            elif pygame.key.get_pressed()[pygame.K_UP]:
                if not plr_list[0] is None and not plr_list[0].move:
                    plr_list[0].set_move(True, 'UP')
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if not plr_list[0] is None and not plr_list[0].move:
                    plr_list[0].set_move(True, 'DOWN')
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                if not plr_list[0] is None and not plr_list[0].move:
                    plr_list[0].set_move(True, 'RIGHT')
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if not plr_list[0] is None and not plr_list[0].move:
                    plr_list[0].set_move(True, 'LEFT')
            if two_players:
                if pygame.key.get_pressed()[pygame.K_w]:
                    if not plr_list[1].move:
                        not plr_list[1] is None and plr_list[1].set_move(True, 'UP')
                elif pygame.key.get_pressed()[pygame.K_s]:
                    if not plr_list[1] is None and not plr_list[1].move:
                        plr_list[1].set_move(True, 'DOWN')
                elif pygame.key.get_pressed()[pygame.K_d]:
                    if not plr_list[1] is None and not plr_list[1].move:
                        plr_list[1].set_move(True, 'RIGHT')
                elif pygame.key.get_pressed()[pygame.K_a]:
                    if not plr_list[1] is None and not plr_list[1].move:
                        plr_list[1].set_move(True, 'LEFT')
        width = screen.get_rect().w
        height = screen.get_rect().h

        if not plr_list[0] is None and pygame.sprite.spritecollide(plr_list[0], wall_group, False):
            # Движение если упёрся в стену
            plr_list[0].step_back()
            plr_list[0].set_move(False)
        if two_players and not plr_list[1] is None and pygame.sprite.spritecollide(plr_list[1], wall_group, False):
            plr_list[1].step_back()
            plr_list[1].set_move(False)

        for coin in coin_group:
            # Сбор монеток
            if not plr_list[0] is None and pygame.sprite.collide_mask(plr_list[0], coin):
                coin.kill()
                # Можно вести подсчёт очков
                point_1 += 1
            if two_players and not plr_list[1] is None and pygame.sprite.collide_mask(plr_list[1], coin):
                coin.kill()
                point_2 += 1

        for exit in exit_group:
            # Вышли ли игроки
            if not plr_list[0] is None and pygame.sprite.collide_mask(plr_list[0], exit):
                plr_list[0].kill()
                plr_list[0] = None
                if not two_players:
                    return
                    # WIN!!!
            elif two_players and not plr_list[1] is None and pygame.sprite.collide_mask(plr_list[1], exit):
                plr_list[1].kill()
                plr_list[1] = None

        screen.fill(BLACK)
        screen.blit(font.render(str(point_1), 0, (255, 255, 0)), (0, 0))
        if two_players:
            f = font.render(str(point_2), 0, (0, 0, 255))
            screen.blit(f, (width - f.get_rect().w, 0))
            # Обработка движения для 2 игроков
            if not plr_list[0] is None and not plr_list[1] is None:
                plr_list[0].moves()
                plr_list[1].moves()
                camera.update2((plr_list[0].rect.x + plr_list[1].rect.x + board.get_cell_size()) // 2,
                               (plr_list[0].rect.y + plr_list[1].rect.y + board.get_cell_size()) // 2)
            elif plr_list[0] is None and plr_list[1] is None:
                return
                # WIN!!!
            elif not plr_list[0] is None:
                plr_list[0].moves()
                camera.update(plr_list[0])
            elif not plr_list[1] is None:
                plr_list[1].moves()
                camera.update(plr_list[1])
        else:
            plr_list[0].moves()
            camera.update(plr_list[0])
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        # Прямоугольник в котором можно работать
        clock.tick(FPS)
        pygame.display.flip()
