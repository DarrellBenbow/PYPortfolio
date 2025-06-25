import pygame as pg
import time
import random

# Initialize Pygame
pg.init()

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 15, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Display settings
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 10
SPEED = 15

# Initialize the game window
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Snake Game')

# Clock to control the game's frame rate
clock = pg.time.Clock() 

# Font settings
font_style = pg.font.SysFont("bahnschrift", 25)
def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])
    
def gameloop():
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0

    SNAKE = []
    length = 1

    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press C-Play Again or Q-Quit", RED, WIDTH / 6, HEIGHT / 3)
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pg.K_c:
                        gameloop()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pg.K_RIGHT:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pg.K_UP:
                    y_change = -SNAKE_SIZE
                    x_change = 0
                elif event.key == pg.K_DOWN:
                    y_change = SNAKE_SIZE
                    x_change = 0
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
    
        x += x_change
        y += y_change
        screen.fill(BLACK)
        pg.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
        
        SNAKE.append([x, y])
        if len(SNAKE) > length:
            del SNAKE[0]
        for segment in SNAKE[:-1]:
            if segment == [x, y]:
                game_close = True
        for segment in SNAKE:
            pg.draw.rect(screen, BLUE, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

        for segment in SNAKE:
            pg.draw.rect(screen, BLUE, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])
        
        pg.display.update()
        
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
            length += 1

        clock.tick(SPEED)
    pg.quit()
    quit()
gameloop()