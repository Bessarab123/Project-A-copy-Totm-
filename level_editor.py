import pygame
import os
import random


def level_editor(x, y, screen, clock, fileName):
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
    pygame.time.set_timer(UPDATE_SPRITES, 1000)
    width = screen.get_rect().w
    height = screen.get_rect().h
    screen = pygame.display.set_mode((max(x * 32, 500), max(y * 32, 500)))

    all_sprites = pygame.sprite.Group()
    wall_sprites_dict = dict()

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
            self.x = 0
            self.y = 0
            self.cell_size = 32

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
                        elif self.board[i][j] == EXIT:
                            Exit(x, y, all_sprites)
                        elif self.board[i][j] == ENTER:
                            Enter(x, y, all_sprites)
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

        def on_click(self, cell_coords):
            '''Определяет как должна реагировать клетка если на неё нажали'''
            j, i = cell_coords
            press = pygame.key.get_pressed()
            if any(press):
                # Если нажата хоть одна клавиша
                if press[pygame.K_w]:
                    self.board[i][j] = 0
                elif press[pygame.K_e]:
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 1
                elif press[pygame.K_i]:
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 2
                elif press[pygame.K_o]:
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 3
                elif press[pygame.K_m]:
                    wall_sprites_dict[(i, j)] = []
                    self.board[i][j] = 4
            else:
                # Если ни одна клавиша не нажата
                self.board[i][j] += 1
                if self.board[i][j] == COIN + 1:
                    self.board[i][j] = WALL
            self.render()

        def get_click(self, mouse_pos):
            cell_coords = self.get_cell(mouse_pos)
            if cell_coords:
                self.on_click(cell_coords)

        def get_cell(self, mouse_pos):
            '''Получить координату клетки на поле на которую нажали'''
            x, y = mouse_pos
            x -= self.x
            y -= self.y
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

        def save_board(self):
            '''Сохраняет доску в "levels/new_save_board.txt или в fileName"'''
            board_str = '\n'.join(list(map(lambda x: ' '.join(map(str, x)), self.board)))
            if fileName != '':
                file = open('levels/' + fileName, mode='w')
                file.write(board_str)
                file.close()
            else:
                file = open('levels/new_save_board.txt', mode='w')
                file.write(board_str)
                file.close()

        def open_board(self, name):
            '''Открывает доску из указанного файла'''
            file = open('levels/' + name)
            self.board = list(map(lambda x: list(map(int, x.split())), file.read().split('\n')))
            self.width = len(self.board[0])
            self.height = len(self.board)
            file.close()

        def move_board(self, move):
            if move == 'UP':
                self.y -= self.cell_size
            elif move == 'DOWN':
                self.y += self.cell_size
            elif move == 'RIGHT':
                self.x += self.cell_size
            elif move == 'LEFT':
                self.x -= self.cell_size
            elif move == 'remove':
                self.x = 0
                self.y = 0
            self.render()

    board = BoardEditor(x, y)
    if fileName != '':
        board.open_board(fileName)

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

    board.render()
    font = pygame.font.Font(None, 24)
    text = ["Справка:",
            "Переключение осуществляется кнопками мышки",
            "Зажмите W и нажимайте мышкой чтобы поставить стену",
            "Зажмите E и нажимайте мышкой чтобы очистить клетку",
            "Зажмите I и нажимайте мышкой чтобы поставить вход",
            "Зажмите O и нажимайте мышкой чтобы поставить выход",
            "Зажмите M и нажимайте мышкой чтобы поставить монетку",
            "Нажмите ctrl + s чтобы сохранить уровень",
            "Для перемещения доски используйте стрелочка",
            "Нажмите R чтобы вернуть доску в стартовое положение",
            "Нажмите Tab чтобы скрыть справку"]
    text = list(map(lambda x: font.render(x, 10, (255, 255, 255)), text))
    reference = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.set_mode((width, height))
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            elif event.type == UPDATE_SPRITES:
                all_sprites.update()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    board.save_board()
                elif pygame.key.get_pressed()[pygame.K_UP]:
                    board.move_board('UP')
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    board.move_board('DOWN')
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    board.move_board('RIGHT')
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    board.move_board('LEFT')
                elif pygame.key.get_pressed()[pygame.K_r]:
                    board.move_board('remove')
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    reference = not reference
                elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.display.set_mode((width, height))
                    return
        screen.fill(BLACK)
        # Прямоугольник в котором можно работать
        pygame.draw.rect(screen, (139, 0, 255),
                         [board.x, board.y,
                          board.cell_size * board.width, board.height * board.cell_size], 1)
        if reference:
            y = 0
            for t in text:
                screen.blit(t, (0, y))
                y += 24
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
