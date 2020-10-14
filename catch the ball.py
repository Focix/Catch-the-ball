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
screen = pygame.display.set_mode((display_width, display_height))
number_of_balls = 8

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

# список, хранящий характеристики всеъ шаров
# [координата x, координата y], радиус, цвет, скорость, угол
global pool
pool = [[[randint(100, display_width - 100),
          randint(100, display_height - 100)],
         randint(10, 70), COLORS[randint(0, 5)],
         randint(50, 100), randint(0, 360)] for i in range(number_of_balls)]



def move_ball():
    """
    Функция передвигает мячи
    """
    for item in pool:
        bump(item)
        item[0][0] += int(item[3] / FPS * np.cos(np.pi * item[4] / 180))
        item[0][1] -= int(item[3] / FPS * np.sin(np.pi * item[4] / 180))
        circle(screen, item[2], item[0], item[1])


def bump(item):
    """
    Функция проверяет удар мячика о стенку и считает новый угол
    unit - элемент списка pool, хранящий все характеричтики данного шара
    """
    # проверка на удар в вертикальные стены
    if item[0][0] + item[1] > display_width - 5:
        if item[4] <= 180:
            item[4] = 180 - item[4]
        else:
            item[4] = 540 - item[4]
    if item[0][0] - item[1] <= 5:
        if item[4] <= 180:
            item[4] = 180 - item[4]
        else:
            item[4] = 540 - item[4]
    # проверка на удар в горизонтальные стены
    if item[0][1] + item[1] >= display_height - 5:
        item[4] = 360 - item[4]
    if item[0][1] - item[1] <= 5:
        item[4] = 360 - item[4]


def score_bar(s):
    """
    score - значение счета игрока
    Функция вывод счет игрока в левый верхний угол экрана
    """
    score_line = 'Score' + ':' + str(s)
    score_text = score_screen.render(score_line, 1, (180, 0, 0))
    screen.blit(score_text, (0, 10))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(score)
            finished = True
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for unit in pool:
                if (event.pos[0] - unit[0][0]) ** 2 + \
                        (event.pos[1] - unit[0][1]) ** 2 <= unit[1] ** 2:
                    if unit[1] <= 20:
                        score += 2
                    else:
                        score += 1
                    pool.remove(unit)
                    pool.append([[randint(100, display_width - 100),
                                  randint(100, display_height - 100)],
                                 randint(10, 70), COLORS[randint(0, 5)],
                                 randint(50, 100), randint(0, 360)])
                    miss = False
                    break
            if miss:
                score -= 1
                break
            if pygame.time.get_ticks() > 20000:
                print('You ran out of time')
                print('Your score is', score)
                finished = True
    move_ball()
    score_bar(score)
    pygame.display.update()
    screen.fill(BLACK)
    miss = True

pygame.quit()
