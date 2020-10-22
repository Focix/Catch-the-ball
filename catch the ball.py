import pygame
from pygame.draw import *
from random import randint
import numpy as np

pygame.init()

miss = True
score = 0
FPS = 30
display_width = 1200
display_height = 700
number_of_balls = 8
number_of_squares = 3
result = str(input('What is your name?\n'))
screen = pygame.display.set_mode((display_width, display_height))

# поверхность для вывода счета
score_screen = pygame.font.Font(None, 36)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:

    def __init__(self, x, y, r, v, color, angle, count):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = color
        self.angle = angle
        self.score = count

    def move(self):
        """
        Метод передвигает круг на новое местоположение
        """
        self.x += int(self.v / FPS * np.cos(np.pi * self.angle / 180))
        self.y += int(self.v / FPS * np.sin(np.pi * self.angle / 180))
        circle(screen, self.color, [self.x, self.y], self.r)


class Square:

    def __init__(self, x, y, r, v, color, angle, count):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = color
        self.angle = angle
        self.score = count

    def move(self):
        """
        Метод передвигает квадрат на новое местоположение
        """
        self.angle += 40
        n = randint(0, 9)
        self.x += int(((-1) ** n) * self.v / FPS + n * self.v /
                      FPS * np.cos(np.pi * self.angle / 180))
        self.y += int(((-1) ** n) * self.v / FPS + n * self.v /
                      FPS * np.sin(np.pi * self.angle / 180))
        rect(screen, self.color, [self.x - self.r // 2, self.y - self.r // 2,
                                  self.r, self.r])


def bump(figure):
    """
        Функция проверяет удар фигуры о стенку и считает новый угол
        figure - фигура на экране (квадрат или круг)
        """
    # проверка на удар в вертикальные стены
    if figure.x + figure.r > display_width:
        if figure.angle <= 180:
            figure.angle = 180 - ball.angle
        else:
            figure.angle = 540 - ball.angle
    if figure.x - figure.r <= 0:
        if figure.angle <= 180:
            figure.angle = 180 - figure.angle
        else:
            figure.angle = 540 - figure.angle
    # проверка на удар в горизонтальные стены
    if figure.y + figure.r >= display_height:
        figure.angle = 360 - figure.angle
    if figure.y - figure.r <= 0:
        figure.angle = 360 - figure.angle


def score_bar(s):
    """
    score - значение счета игрока
    Функция вывод счет игрока в левый верхний угол экрана
    """
    score_line = 'Score' + ':' + str(s)
    score_text = score_screen.render(score_line, 1, (180, 0, 0))
    screen.blit(score_text, (0, 10))


def recording(s, count):
    """
    Функция записывает в файл 'score_board.txt' результаты игроков
    и сортирует их
    s - строка, содержащаяа имя игрока
    count - результат игрока
    """
    s = str(count) + ' - ' + s
    with open('score_board', 'r') as reading:
        lines = [s.split()]
        for line in reading:
            if line != '\n' and line != '':
                lines.append(line.split())
        lines.sort(key=lambda x: x[0])
        lines.reverse()
    with open('score_board', 'w') as writing:
        writing.truncate()
        for line in lines:
            print(' '.join(line), file=writing)


def new():
    """
    Функция создает новую фигуру на поле
    """
    n = randint(0, 1)
    if n == 0:
        new_item = Ball(
            randint(100, display_width - 100),
            randint(100, display_height - 100),
            randint(10, 70), randint(50, 100),
            COLORS[randint(0, 5)], randint(0, 360), 1)
    else:
        new_item = Square(
            randint(100, display_width - 100),
            randint(100, display_height - 100),
            randint(40, 70), randint(50, 100),
            COLORS[randint(0, 5)], randint(0, 360), 3)
    pool.append(new_item)


pool = []  # список всех фигур

for i in range(number_of_balls):
    ball = Ball(randint(100, display_width - 100),
                randint(100, display_height - 100), randint(10, 70),
                randint(50, 100), COLORS[randint(0, 5)], randint(0, 360), 1)
    pool.append(ball)

for i in range(number_of_squares):
    square = Square(randint(100, display_width - 100),
                    randint(100, display_height - 100), randint(40, 70),
                    randint(50, 100), COLORS[randint(0, 5)],
                    randint(0, 360), 3)
    pool.append(square)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            recording(result, score)
            finished = True
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for item in pool:
                if type(item) == Ball:
                    if (event.pos[0] - item.x) ** 2 + \
                            (event.pos[1] - item.y) ** 2 <= item.r ** 2:
                        if item.r <= 20:
                            score += 2
                        else:
                            score += 1
                        new()
                        pool.remove(item)
                        miss = False
                        break
                elif item.x - item.r // 2 < event.pos[0] < \
                        item.x + item.r // 2 and \
                        item.y - item.r // 2 < event.pos[1] < \
                        item.y + item.r // 2:
                    score += item.score
                    new()
                    pool.remove(item)
                    miss = False
                    break
            if miss:
                score -= 1
                break
    if pygame.time.get_ticks() > 10000:
        print('You ran out of time')
        print('Your score is', score)
        recording(result, score)
        finished = True
    for ball in pool:
        bump(ball)
        ball.move()
    score_bar(score)
    pygame.display.update()
    screen.fill(BLACK)
    miss = True

pygame.quit()
