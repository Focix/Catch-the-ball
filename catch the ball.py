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
user_name = str(input('What is your name?'))
result = user_name
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

    def __init__(self, x, y, r, v, color, angle):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = color
        self.angle = angle

    def move(self):
        self.x += int(self.v / FPS * np.cos(np.pi * self.angle / 180))
        self.y += int(self.v / FPS * np.sin(np.pi * self.angle / 180))
        circle(screen, self.color, [self.x, self.y], self.r)

class Square:

    def __init__(self, x, y, r, v, color, angle):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = color
        self.angle = angle

    def move(self):
        self.x += int(self.v / FPS * np.cos(np.pi * self.angle / 180))
        self.y += int(self.v / FPS * np.sin(np.pi * self.angle / 180))
        rect(screen, self.color, [self.x - self.r // 2, self.y - self.r // 2, self.r, self.r])


def bump(ball):
        """
        Функция проверяет удар мячика о стенку и считает новый угол
        ball - элемент класса Ball, хранящийся в списке pool
        """
        # проверка на удар в вертикальные стены
        if ball.x + ball.r > display_width :
            if ball.angle <= 180:
                ball.angle = 180 - ball.angle
            else:
                ball.angle = 540 - ball.angle
        if ball.x - ball.r <= 0:
            if ball.angle <= 180:
                ball.angle = 180 - ball.angle
            else:
                ball.angle = 540 - ball.angle
        # проверка на удар в горизонтальные стены
        if ball.y + ball.r >= display_height:
            ball.angle = 360 - ball.angle
        if ball.y - ball.r <= 0:
            ball.angle = 360 - ball.angle

def score_bar(s):
    """
    score - значение счета игрока
    Функция вывод счет игрока в левый верхний угол экрана
    """
    score_line = 'Score' + ':' + str(s)
    score_text = score_screen.render(score_line, 1, (180, 0, 0))
    screen.blit(score_text, (0, 10))

def recording(stroka, score):
    stroka = str(score) + ' - ' + stroka
    with open('score_board', 'r') as reading:
        lines = [stroka]
        for line in reading:
            if line!='\n':
                lines.append(line)
        lines.sort()
    with open('score_board', 'w') as writing:
        for line in lines:
            print(line, file=writing)

pool = [] # список всех мячей

for i in range(number_of_balls):
    ball = Ball(randint(100, display_width - 100),
                                  randint(100, display_height - 100),
                                 randint(10, 70), randint(50, 100),
                                COLORS[randint(0, 5)],randint(0, 360))
    pool.append(ball)

for i in range(number_of_squares):
    square = Square(randint(100, display_width - 100),
                                  randint(100, display_height - 100),
                                 randint(10, 70), randint(50, 100),
                                COLORS[randint(0, 5)],randint(0, 360))
    pool.append(square)

classes = [Ball, Square] # список классов

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
                if (event.pos[0] - item.x) ** 2 + \
                        (event.pos[1] - item.y) ** 2 <= item.r ** 2:
                    if type(item) == Ball:
                        if item.r <= 20:
                            score += 2
                        else:
                            score += 1
                    else:
                        score += 3
                    new_item = classes[randint(0, 1)]\
                        (randint(100, display_width - 100),
                                        randint(100, display_height - 100),
                                        randint(10, 70), randint(50, 100),
                                        COLORS[randint(0, 5)], randint(0, 360))
                    pool.remove(item)
                    pool.append(new_item)
                    miss = False
                    break
            if miss:
                score -= 1
                break
        if pygame.time.get_ticks() > 20000:
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
