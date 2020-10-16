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

class Ball:

    def __init__(self, x, y, r, v, color, angle):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = color
        self.angle = angle

    def move_ball(self):
        self.x += int(self.v / FPS * np.cos(np.pi * self.angle / 180))
        self.y += int(self.v / FPS * np.sin(np.pi * self.angle / 180))
        circle(screen, self.color, [self.x, self.y], self.r)

def bump(ball):
        """
        Функция проверяет удар мячика о стенку и считает новый угол
        ball - элемент списка pool, хранящий все характериcтики данного шара
        """
        # проверка на удар в вертикальные стены
        if ball.x + ball.r > display_width - 5:
            if ball.angle <= 180:
                ball.angle = 180 - ball.angle
            else:
                ball.angle = 540 - ball.angle
        if ball.x - ball.r <= 5:
            if ball.angle <= 180:
                ball.angle = 180 - ball.angle
            else:
                ball.angle = 540 - ball.angle
        # проверка на удар в горизонтальные стены
        if ball.y + ball.r >= display_height - 5:
            ball.angle = 360 - ball.angle
        if ball.y - ball.r <= 5:
            ball.angle = 360 - ball.angle

def score_bar(s):
    """
    score - значение счета игрока
    Функция вывод счет игрока в левый верхний угол экрана
    """
    score_line = 'Score' + ':' + str(s)
    score_text = score_screen.render(score_line, 1, (180, 0, 0))
    screen.blit(score_text, (0, 10))

pool = [] # список всех мячей
for i in range(number_of_balls):
    ball = Ball(randint(100, display_width - 100),
                                  randint(100, display_height - 100),
                                 randint(10, 70), randint(50, 100),
                                COLORS[randint(0, 5)],randint(0, 360))
    pool.append(ball)



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
            for ball in pool:
                if (event.pos[0] - ball.x) ** 2 + \
                        (event.pos[1] - ball.y) ** 2 <= ball.r ** 2:
                    if ball.r <= 20:
                        score += 2
                    else:
                        score += 1
                    pool.remove(ball)
                    new_ball = Ball(randint(100, display_width - 100),
                                  randint(100, display_height - 100),
                                 randint(10, 70), randint(50, 100),
                                COLORS[randint(0, 5)],randint(0, 360))
                    pool.append(new_ball)

                    miss = False
                    break
            if miss:
                score -= 1
                break
            if pygame.time.get_ticks() > 20000:
                print('You ran out of time')
                print('Your score is', score)
                finished = True
    for ball in pool:
        bump(ball)
        ball.move_ball()
    score_bar(score)
    pygame.display.update()
    screen.fill(BLACK)
    miss = True

pygame.quit()