import pygame
import os
import random


def level_editor(x, y, screen, clock):
    '''Создать редактор уровня принимает
    x, y размеры поля
    screen, clock'''
    WALL = 0
    EMPTY = 1
    ENTER = 2
    EXIT = 3
    COIN = 4
    BLACK = pygame.Color('black')
    UPDATE_SPRITES = 30

    all_sprites = pygame.sprite.Group()
    wall_sprites_dict = dict()

    clock.set_timer(UPDATE_SPRITES, 1000)

    def load_image(name):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (board.get_cell_size(), board.get_cell_size()))
        image.set_colorkey(BLACK)
        return image

    class BoardEditor():
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.board = [[EMPTY] * width for _ in range(height)]
            self.cell_size = 32

        def set_cell_size(self, cell_size):
            '''Изменить размер клетки'''
            self.cell_size = cell_size

        def get_cell_size(self):
            return self.cell_size

        def render(self, screen):
            all_sprites.empty()
            y = 0
            for i in range(self.height):
                x = 0
                for j in range(self.width):
                    if self.board[i][j]:
                        # Если стена
                        if self.board[i][j] == COIN:
                            Coin(x, y, all_sprites)
                        elif self.board[i][j] == EXIT:
                            Exit(x, y, all_sprites)
                        elif self.board[i][j] == ENTER:
                            Enter(x, y, all_sprites)
                    else:
                        # Если стена
                        self.kill_wall(i, j)
                        wall_sprites_dict[(i, j)] = []
                        # Логика того как должна прорисоваться стена
                        if j - 1 > -1 and self.board[i][j - 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 270, all_sprites))
                        if j + 1 < self.width + 1 and self.board[i][j + 1]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 90, all_sprites))
                        if i - 1 > - 1 and self.board[i - 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 180, all_sprites))
                        if i + 1 < self.height + 1 and self.board[i + 1][j]:
                            wall_sprites_dict[(i, j)].append(Wall(x, y, 0, all_sprites))
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
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 1
                elif press[pygame.K_2]:
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 2
                elif press[pygame.K_3]:
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 3
                elif press[pygame.K_4]:
                    wall_sprites_dict[(i, j)] = []
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
            x1 = x // self.cell_size
            y1 = y // self.cell_size
            if x1 < 0 or x1 >= self.width:
                return None
            if y1 < 0 or y1 >= self.height:
                return None
            return x1, y1

        def kill_wall(self, i, j):
            if (i, j) in wall_sprites_dict.keys():
                for wall in wall_sprites_dict[(i, j)]:
                    wall.kill()

    board = BoardEditor(x, y)

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

    class Enter(Sprites):
        enter_im = load_image('enter.png')

        def __init__(self, x, y, *group):
            super().__init__(x, y, group)
            self.image = Enter.enter_im

    class Exit(Sprites):
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
        coin_im = load_image('coin.png')

        def __init__(self, x, y, *group):
            super().__init__(x, y, group)
            self.image = Coin.coin_im

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                board.get_click(event.pos)
            elif event.type == UPDATE_SPRITES:
                all_sprites.update()
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()
