import random
import pygame
import sqlite3 as sq
import datetime


def lose():
    global lenght, snake, is_moving, x, y
    today = datetime.datetime.today()
    res = today.strftime('%d-%m-%Y %H:%M:%S')
    cursor.execute('insert into Рекорды values (?,?)', (res, lenght))
    db.commit()
    lenght = 1
    x, y = (random.randrange(320, 480, size), random.randrange(320, 480, size))
    snake = [(x, y)]
    is_moving = False


alfa = pygame.Surface([300, 300])
alfa.fill((255, 255, 255))


class Apple(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        apple_image = pygame.image.load(r"data\apple.png")
        apple_image.set_colorkey(apple_image.get_at((0, 0)))
        self.image = apple_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Snake(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load(r'data\snake_head6.png')
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 20
        self.angle = 0

    def update(self, x, y):
        self.rect.x = int(x)
        self.rect.y = int(y)

    def rotate(self, button):
        if self.angle == 0:
            if button == pygame.K_a:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 270
            elif button == pygame.K_d:
                self.image = pygame.transform.rotate(self.image, 270)
                self.angle = 90
        elif self.angle == 90:
            if button == pygame.K_w:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 0
            elif button == pygame.K_s:
                self.image = pygame.transform.rotate(self.image, 270)
                self.angle = 180
        elif self.angle == 180:
            if button == pygame.K_a:
                self.image = pygame.transform.rotate(self.image, 270)
                self.angle = 270
            elif button == pygame.K_d:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 90
        elif self.angle == 270:
            if button == pygame.K_w:
                self.image = pygame.transform.rotate(self.image, 270)
                self.angle = 0
            elif button == pygame.K_s:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 180


pygame.init()
size = 1000, 600
pygame.display.set_caption('Змейка')
screen = pygame.display.set_mode(size)
size = 40
running = True
x, y = (random.randrange(320, 480, size), random.randrange(320, 480, size))
apple_coords = (random.randrange(160, 560, size), random.randrange(160, 560, size))
dx = 0
dy = -1
lenght = 1
snake = [(x, y)]
clock = pygame.time.Clock()
fps = 5
is_moving = 0
w, d, s, a = 1, 1, 1, 1
db = sq.connect('Snake.db')
cursor = db.cursor()
cursor.execute('create table if not exists Рекорды(день str, счёт str)')
db.commit()
color = {'1': 'blue', '2': 'pink', '3': 'yellow', '4': 'orange', '5': 'green'}
color_current = 'green'
angel = 0
# Snake_group
Snake_group = pygame.sprite.Group()
nake = Snake()
Snake_group.add(nake)
# Snake_group


# Apple_group
Apple_group = pygame.sprite.Group()
pple = Apple(x=apple_coords[0], y=apple_coords[1])
Apple_group.add(pple)
# Apple_group
while running:
    if x > 1000 or x < 0 or y > 600 or y < 0:
        lose()
    if is_moving:
        score = pygame.font.Font(None, 32)
        res = score.render(f'Счёт:{lenght}', True, (100, 255, 100))
        screen.blit(res, (0, 0))
        n1, n2 = snake[-1]
        Snake_group.update(n1, n2)
        old_image = nake.image
        Snake_group.draw(screen)
        for n1, n2 in snake[:-1]:
            Snake_group.update(n1, n2)
            nake.image = pygame.image.load(r'data\snake_body.jpg')
            nake.image.fill(pygame.Color(0, 200, 0))
            Snake_group.draw(screen)
        Apple_group.draw(screen)
        nake.image = old_image
        x += dx * size
        y += dy * size
        snake.append((x, y))
        snake = snake[-lenght:]
    else:
        font = pygame.font.Font(None, 50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            data = cursor.execute('select * from Рекорды order by счёт desc').fetchall()[:5]
            start = 100
            text = font.render(f'День{" " * 20}Время{" " * 20}Счёт', True, (100, 255, 100))
            screen.blit(text, (80, 50))
            for j in data:
                start += 50
                d, t = j[0].split()
                res = d + " " * 10 + t + " " * 20 + str(j[1])
                text = font.render(res, True, (100, 255, 100))
                screen.blit(text, (70, start))
        else:
            text = font.render("Нажмите Пробел для старта", True, (100, 255, 100))
            _1 = font.render("Статистика (цифра 1)", True, (100, 255, 100))
            text_x = 1000 // 2 - text.get_width() // 2
            screen.blit(text, (text_x, 100))
            screen.blit(_1, (text_x + 50, 200))
    if snake[-1] == apple_coords:
        apple_coords = (random.randrange(160, 560, size), random.randrange(160, 560, size))
        pple.rect.x = apple_coords[0]
        pple.rect.y = apple_coords[1]
        lenght += 1
    if len(snake) != len(set(snake)):
        lose()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                color_current = color[event.unicode]
            if event.key == pygame.K_w and w:
                dx, dy = 0, -1
                w, s, d, a = 0, 0, 1, 1
                nake.rotate(event.key)
            if event.key == pygame.K_d and d:
                dx, dy = 1, 0
                d, a, s, w = 0, 0, 1, 1
                nake.rotate(event.key)
            if event.key == pygame.K_a and a:
                dx, dy = -1, 0
                d, a, s, w = 0, 0, 1, 1
                nake.rotate(event.key)
            if event.key == pygame.K_s and s:
                dx, dy = 0, 1
                w, s, d, a = 0, 0, 1, 1
                nake.rotate(event.key)
            if event.key == pygame.K_SPACE:
                is_moving = not is_moving
    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(10)

pygame.quit()
