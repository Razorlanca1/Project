import pygame
import os
import time
import sys
import random


all_sprites = pygame.sprite.Group()

tile_width = tile_height = 50


player = None

tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
eat_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Перемещение на стрелочки",
                  "У вас есть 60 секунд на сбор пиццы"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (640, 360))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    a = True
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                a = False  
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        a = []
        a = [line.strip() for line in mapFile]
        max_width = max(map(len, a))
        a = list(map(lambda x: x.ljust(max_width, '.'), a))
        a = list(map(lambda x: x * 3, a))
        level_map = []
        level_map.extend(a)
        level_map.extend(a)
        level_map.extend(a)
        

    return level_map



def check(x, y):
    for num, i in enumerate(rects):
        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
            return True, num
    return False, -1


def eat():
    eat_group.empty()
    x, y = random.choice(range(l2)), random.choice(range(l1))
    while mp[y][x] != '.':
        x, y = random.choice(range(l2)), random.choice(range(l1))
    a = Eat(x, y)
    a.add(eat_group)
    a = Eat(x + l2, y)
    a.add(eat_group)
    a = Eat(x - l2, y)
    a.add(eat_group)
    a = Eat(x, y + l1)
    a.add(eat_group)
    a = Eat(x, y - l1)
    a.add(eat_group)
    a = Eat(x + l2, y + l1)
    a.add(eat_group)
    a = Eat(x - l2, y - l1)
    a.add(eat_group)
    a = Eat(x - l2, y + l1)
    a.add(eat_group)
    a = Eat(x + l2, y - l1)
    a.add(eat_group)
    return x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj, player):
        if obj != player:
            obj.rect.x = self.dx + obj.sx * tile_width
            obj.rect.y = self.dy + obj.sy * tile_height
            
    
    def update(self, x, y):
        self.dx -= x * tile_width
        self.dy -= y * tile_height
        


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.sx = pos_x
        self.sy = pos_y
        self.x = self.rect.x
        self.y = self.rect.y
        
        
class Eat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(eat_group)
        self.image = tile_images['eat']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.sx = pos_x
        self.sy = pos_y
        self.x = self.rect.x
        self.y = self.rect.y
        

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 15)
        self.x = self.rect.x
        self.y = self.rect.y
    
    def new_rectengle(self, x, y):
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.x = self.rect.x
        self.y = self.rect.y


def generate_level(level):
    global mp
    mp = level
    new_player, x, y = None, None, None
    global l1, l2
    l1 = len(level) // 3
    l2 = len(level[0]) // 3
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.' or  level[y][x] == '@':
                a = Tile('empty', x - l2, y - l1)
                a.add(tiles_group)
            elif level[y][x] == '#':
                a = Tile('wall', x - l2, y - l1)
                a.add(tiles_group)
            
            
    for y in range(l1, l1 * 2):
        for x in range(l2, l2 * 2):
            if level[y][x] == '.':
                a = Tile('empty', x - l2, y - l1)
                a.add(tiles_group)
            elif level[y][x] == '#':
                a = Tile('wall', x - l2, y - l1)
                a.add(tiles_group)
            elif level[y][x] == '@':
                a = Tile('empty', x - l2, y - l1)
                a.add(tiles_group)
                new_player = Player(x - l2, y - l1)
                new_player.add(player_group)
                px = x - l2
                py = y - l1
    ex, ey = eat()
    return new_player, px, py, ex, ey


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'eat': load_image('eat.png')
}
player_image = load_image('mario.png')

def sup():
    class Board:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.bombs = []
            self.win = False
            while len(self.bombs) != 150:
                a = random.choices(range(30), k=2)
                if a not in self.bombs:
                    self.bombs.append(a)
            self.board = [[-1] * width for _ in range(height)]
            for i in self.bombs:
                self.board[i[0]][i[1]] = 10
            self.left = 10
            self.top = 10
            self.cell_size = 60
            self.op = False
            self.open_bombs = []
    
        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size
    
        def render(self, screen):
            stop = True
            for i in self.board:
                if -1 in i:
                    stop = False
                    break
            if stop and not self.op:
                self.win = True
                self.op = stop
            size = self.cell_size
            for j in range(len(self.board)):
                for i in range(len(self.board[j])):
                    rect = pygame.Rect(self.left + (i * size), self.top + (j * size), size, size)
                    if (j, i) in self.open_bombs:
                        pygame.draw.rect(screen, pygame.Color('blue'), rect, 0)
                        pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
                    elif self.board[j][i] == -1:
                        pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
                    elif self.board[j][i] == 10:
                        if self.op:
                            pygame.draw.rect(screen, pygame.Color('red'), rect, 0)
                            pygame.draw.rect(screen, pygame.Color('green'), rect, 1)
                        else:
                            pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
                    else:
                        font = pygame.font.Font(None, 30)
                        text = font.render(str(self.board[j][i]), True, (100, 255, 100))
                        text_x = self.left + i * size
                        text_y = self.top + j * size
                        text_w = size
                        text_h = size
                        screen.blit(text, (text_x + 5, text_y))
                        pygame.draw.rect(screen, (0, 255, 0), (text_x, text_y,
                                                               text_w, text_h), 1)  
    
    
        def get_click(self, mouse_pos, button):
            cell = self.get_cell(mouse_pos)
            if cell != None:
                if self.board[cell[0]][cell[1]] == 10 and not button and cell not in self.open_bombs:
                    self.op = True
                    self.open_bombs.clear()
                    for i in range(self.height):
                        for j in range(self.width):
                            self.open_cell((i, j))
                else:
                    if button:
                        if cell in self.open_bombs:
                            self.open_bombs.remove(cell)
                        elif self.board[cell[0]][cell[1]] == -1 or self.board[cell[0]][cell[1]] == 10:
                            self.open_bombs.append(cell)
                    elif cell not in self.open_bombs:
                        self.open_cell(cell, button)
    
        def get_cell(self, mouse_pos):
            size = self.cell_size
            if self.left < mouse_pos[0] < self.left + size * self.width:
                if self.top < mouse_pos[1] < self.top + size * self.height:
                    for j in range(len(self.board)):
                        if self.top + j * size <= mouse_pos[1] <= self.top + (j + 1) * size:
                            for i in range(len(self.board[j])):
                                if self.left + i * size <= mouse_pos[0] <= self.left + (i + 1) * size:
                                    return (j, i)
                else:
                    return None
            else:
                return None
    
        def open_cell(self, cell_coords, button=False):
            if cell_coords != None:
                i = cell_coords[0]
                j = cell_coords[1]
                if self.board[i][j] == -1:
                    a = 0
                    if i != 0:
                        if self.board[i - 1][j] == 10:
                            a += 1
                    if i != len(self.board) - 1:
                        if self.board[i + 1][j] == 10:
                            a += 1
                    if j != 0:
                        if self.board[i][j - 1] == 10:
                            a += 1
                    if j != len(self.board[i]) - 1:
                        if self.board[i][j + 1] == 10:
                            a += 1
                    if i != 0 and j != 0:
                        if self.board[i - 1][j - 1] == 10:
                            a += 1
                    if i != len(self.board) - 1 and j != len(self.board[i]) - 1:
                        if self.board[i + 1][j + 1] == 10:
                            a += 1
                    if i != 0 and j != len(self.board[i]) - 1:
                        if self.board[i - 1][j + 1] == 10:
                            a += 1
                    if i != len(self.board) - 1 and j != 0:
                        if self.board[i + 1][j - 1] == 10:
                            a += 1
                    self.board[i][j] = a
                    if a == 0:
                        if i != 0:
                            self.open_cell((i - 1, j))
                        if i != len(self.board) - 1:
                            self.open_cell((i + 1, j))
                        if j != 0:
                            self.open_cell((i, j - 1))
                        if j != len(self.board[i]) - 1:
                            self.open_cell((i, j + 1))
                        if i != 0 and j != 0:
                            self.open_cell((i - 1, j - 1))
                        if i != len(self.board) - 1 and j != len(self.board[i]) - 1:
                            self.open_cell((i + 1, j + 1))
                        if i != 0 and j != len(self.board[i]) - 1:
                            self.open_cell((i - 1, j + 1))
                        if i != len(self.board) - 1 and j != 0:
                            self.open_cell((i + 1, j - 1))
    
    
    pygame.display.set_caption('Сапёр')
    size = width, height = 640, 640
    screen = pygame.display.set_mode(size)
    board = Board(30, 30)
    board.set_view(20, 20, 20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not board.op:
                    if event.button == 3:
                        board.get_click(event.pos, True)
                    else:
                        board.get_click(event.pos, False)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        if board.op:
            time.sleep(2)
            pygame.display.quit()
            zastavka([board.win, 'sp'])
    time.sleep(2)
    pygame.display.quit()
    zastavka([board.win, 'sp'])    


def zme():
    class Board:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            self.directs = ['right']
            self.eat_count = 0
            self.snake = []
            self.snake.append([0, 13])
            self.snake.append([0, 14])
            self.snake.append([0, 15])
            self.snake.append([0, 16])
            for i in range(len(self.snake)):
                if i != len(self.snake) - 1:
                    self.board[self.snake[i][0]][self.snake[i][1]] = 2
                else:
                    self.board[self.snake[i][0]][self.snake[i][1]] = 3
            self.left = 10
            self.top = 10
            self.cell_size = 60
            self.stop = False
            self.eat = random.choices(range(30), k=2)
            while self.eat in self.snake:
                self.eat = random.choices(range(30), k=2)
            self.board[self.eat[0]][self.eat[1]] = 1
            self.repit = False
    
        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size
    
        def render(self, screen):
            size = self.cell_size
            rect = pygame.Rect(self.left, self.top, size * self.height, size * self.width)
            pygame.draw.rect(screen, pygame.Color('black'), rect, 0)
            if len(self.directs) != 0 and not self.stop:
                self.move()
            for j in range(len(self.board)):
                for i in range(len(self.board[j])):
                    rect = pygame.Rect(self.left + (i * size), self.top + (j * size), size, size)
                    if self.board[j][i] == 1:
                        pygame.draw.circle(screen, pygame.Color('red'), 
                                           (self.left + (i * size + int(size * 0.5)), self.top + (j * size + int(size * 0.5))), int(size * 0.25), 0)
                    elif self.board[j][i] == 2:
                        pygame.draw.circle(screen, pygame.Color('orange'), 
                                           (self.left + (i * size + int(size * 0.5)), self.top + (j * size + int(size * 0.5))), int(size * 0.5), 0)
                    if self.board[j][i] == 3:
                        pygame.draw.circle(screen, pygame.Color('orange'), 
                                           (self.left + (i * size + int(size * 0.5)), self.top + (j * size + int(size * 0.5))), int(size * 0.5), 0)
                        pygame.draw.circle(screen, pygame.Color('white'), 
                                           (self.left + (i * size + int(size * 0.5)) - 4, self.top + (j * size) + 6), int(size * 0.1), 0)
                        pygame.draw.circle(screen, pygame.Color('white'), 
                                           (self.left + (i * size + int(size * 0.5)) + 4, self.top + (j * size) + 6), int(size * 0.1), 0)
            rect = pygame.Rect(self.left, self.top, size * self.height, size * self.width)
            pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
            
            
        def add_direct(self, direct):
            if self.directs[-1] == 'up' and direct != 'down':
                self.directs.append(direct)
            elif self.directs[-1] == 'down' and direct != 'up':
                self.directs.append(direct)
            elif self.directs[-1] == 'left' and direct != 'right':
                self.directs.append(direct)
            elif self.directs[-1] == 'right' and direct != 'left':
                self.directs.append(direct)
        
        def rep(self):
            if len(self.directs) != 1:
                if self.repit:
                    self.directs.remove(self.directs[0])
                    self.repit = False
                    return self.rep()
                else:
                    return self.directs.pop(0)
            else:
                self.repit = True
                return self.directs[0]
            
    
        def move(self):
            d = self.rep()
            i1 = 0
            j1 = 0
            if d == 'up':
                i1 = -1
            elif d == 'down':
                i1 = 1
            elif d == 'left':
                j1 = -1
            elif d == 'right':
                j1 = 1
            self.board = [[0] * width for _ in range(height)]
            for i in range(len(self.snake)):
                if i != len(self.snake) - 1:
                    self.snake[i][0] = self.snake[i + 1][0]
                    self.snake[i][1] = self.snake[i + 1][1]
                    self.board[self.snake[i][0]][self.snake[i][1]] = 2
            if 0 <= self.snake[-1][0] + i1 < self.height and 0 <= self.snake[-1][1] + j1 < self.width :
                self.snake[-1][0] += i1
                self.snake[-1][1] += j1
                if self.snake[-1] not in self.snake[:-1]:
                    if self.snake[-1] == self.eat:
                        self.snake.insert(0, [2 * self.snake[0][0] - self.snake[1][0], 2 * self.snake[0][1] - self.snake[1][1]])
                        self.eat = random.choices(range(30), k=2)
                        while self.eat in self.snake:
                            self.eat = random.choices(range(30), k=2)
                        self.eat_count += 1
                else:
                    self.stop = True
                self.board[self.snake[-1][0]][self.snake[-1][1]] = 3
            else:
                self.stop = True
            self.board[self.eat[0]][self.eat[1]] = 1
    
    pygame.init()
    pygame.display.set_caption('Змейка')
    size = width, height = 640, 640
    screen = pygame.display.set_mode(size)
    board = Board(30, 30)
    board.set_view(20, 20, 20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not board.stop:
                    if event.key == pygame.K_UP:
                        board.add_direct('up')
                    elif event.key == pygame.K_DOWN:
                        board.add_direct('down')
                    elif event.key == pygame.K_LEFT:
                        board.add_direct('left')
                    elif event.key == pygame.K_RIGHT:
                        board.add_direct('right')
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        if board.stop:
            time.sleep(2)
            pygame.display.quit()
            zastavka([board.eat_count, 'sh'])
    time.sleep(2)
    pygame.display.quit()
    zastavka([board.eat_count, 'sh'])


def brod():
    print("Введите имя файла:")
    file = input()
    if os.path.exists(file):
        clock = pygame.time.Clock()
        t = clock.tick()
        player, x, y, ex, ey = generate_level(load_level(file))
        pygame.display.set_caption('Бродилка')
        size = width, height = 640, 360
        screen = pygame.display.set_mode(size)
        start_screen(screen)
        size = width, height = 550, 550
        screen = pygame.display.set_mode(size)
        running = True
        draw = True
        count = 0   
        camera = Camera()
        while running:
            if t < 60000:
                t += clock.tick()
            else:
                time.sleep(2)
                pygame.display.quit()
                zastavka([count, "br"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if y != 0:
                            if mp[y - 1 + l1][x + l2] == '.':
                                if y - 1 == ey and x == ex:
                                    ex, ey = eat()
                                    count += 1
                                y -= 1
                                camera.update(0, -1)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                        else:
                            if mp[l1 - 1 + l1][x + l2] != '#':
                                y = l1 - 1
                                camera.update(0, l1 - 1)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                    elif event.key == pygame.K_DOWN:
                        if y != l1 - 1:
                            if mp[y + 1 + l1][x + l2] != '#':
                                if y + 1 == ey and x == ex:
                                    ex, ey = eat()
                                    count += 1
                                y += 1
                                camera.update(0, 1)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                        else:
                            if mp[l1][x + l2] != '#':
                                y = 0
                                camera.update(0, -l1 + 1)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                    elif event.key == pygame.K_LEFT:
                        if x != 0:
                            if mp[y + l1][x - 1 + l2] != '#':
                                if y == ey and x - 1 == ex:
                                    ex, ey = eat()
                                    count += 1
                                x -= 1
                                camera.update(-1, 0)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                        else:
                            if mp[y + l1][l2 - 1 + l2] != '#':
                                x = l2 - 1
                                camera.update(l2 - 1, 0)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                    elif event.key == pygame.K_RIGHT:
                        if x != l2 - 1:
                            if mp[y + l1][x + 1 + l2] != '#':
                                if y == ey and x + 1 == ex:
                                    ex, ey = eat()
                                    count += 1
                                x += 1
                                camera.update(1, 0)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
                        else:
                            if mp[y + l1][l2] != '#':
                                x = 0
                                camera.update(-l2 + 1, 0)
                                for sprite in all_sprites:
                                    camera.apply(sprite, player)
                                for sprite in eat_group:
                                    camera.apply(sprite, player)
            screen.fill((0, 0, 0))
            tiles_group.draw(screen)
            eat_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            time.sleep(0.01)
        time.sleep(2)
        pygame.display.quit()
        zastavka([count, "br"])
        return True
    else:
        print("такого нет")
        pygame.quit()
    

br_count = 0
snake_count = 0
proiden = False

def zastavka(count=None):
    global br_count
    global snake_count
    global proiden
    intro_text = ["ВЫБОР ИГРЫ",
                  "Нажмите на кнопку для выбора игры",
                  "В Змейке и Бродилке управление на стрелочках",
                  "При запуске Бродилке введите названия файла уровня",
                  "В Сапёре ЛКМ - открыть клетку, ПКМ - поставить флаг"]
    pygame.display.set_caption('Выбор игры')
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)    
    fon = pygame.transform.scale(load_image('zastavka.jpg'), (640, 360))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    a = True
    for i, line in enumerate(intro_text):
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        if i == 0:
            intro_rect.x = 200
        else:
            intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    global rects
    rects = []
    rects_text = ["Бродилка",
                  "Змейка",
                  "Сапёр"]
    text_coord = 60
    a = True
    for i in range(3):
        string_rendered = font.render(rects_text[i], 1, pygame.Color('white'))
        r = string_rendered.get_rect()
        text_coord += 10
        r.left = text_coord + i * 200
        r.top = 260
        rects.append([70 + i * 200, 220, 100, 100])
        Rect = pygame.Rect(70 + i * 200, 220, 100, 100)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), Rect, 1)
        screen.blit(string_rendered, r)
    if count != None:
        if count[1] == "br":
            br_count = count[0]
        elif count[1] == 'sh':
            snake_count = count[0]
        elif count[1] == 'sp':
            proiden = count[0]
    string_rendered = font.render("Счёт: " + str(br_count), 1, pygame.Color('green'))
    r = string_rendered.get_rect()
    r.top = 190
    r.left = 80
    screen.blit(string_rendered, r)
    string_rendered = font.render("Счёт: " + str(snake_count), 1, pygame.Color('green'))
    r = string_rendered.get_rect()
    r.top = 190
    r.left = 280
    screen.blit(string_rendered, r)
    if proiden:
        string_rendered = font.render("Пройден", 1, pygame.Color('green'))
    else:
        string_rendered = font.render("Непройден", 1, pygame.Color('red'))
    r = string_rendered.get_rect()
    r.top = 190
    r.left = 470
    screen.blit(string_rendered, r)
        
        
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                b, i = check(x, y)  
                if b:
                    a = False
                    if rects_text[i] == 'Сапёр':
                        sup()
                    elif rects_text[i] == 'Змейка':
                        zme()
                    elif rects_text[i] == 'Бродилка':
                        brod()
        pygame.display.flip()
    
    
pygame.init()
zastavka()