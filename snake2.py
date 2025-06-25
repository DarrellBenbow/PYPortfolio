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
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
SNAKE_COLORS = [BLUE, RED, GREEN, YELLOW, CYAN, PURPLE]
SNAKE_COLOR_NAMES = ["Blue", "Red", "Green", "Yellow", "Cyan", "Purple"]

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
#customization_menu
# This function allows the player to customize the snake's color
def customization_menu():
    color_idx = 0
    customizing = True
    while customizing:
        screen.fill(BLACK)
        message("Snake Customization", WHITE, WIDTH // 3, HEIGHT // 6)
        message(f"Color: {SNAKE_COLOR_NAMES[color_idx]}", SNAKE_COLORS[color_idx], WIDTH // 3, HEIGHT // 3)
        message("Left/Right to change color", WHITE, WIDTH // 3, HEIGHT // 2)
        message("Enter to confirm, B to go back", WHITE, WIDTH // 3, HEIGHT // 2 + 40)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    color_idx = (color_idx - 1) % len(SNAKE_COLORS)
                if event.key == pg.K_RIGHT:
                    color_idx = (color_idx + 1) % len(SNAKE_COLORS)
                if event.key == pg.K_RETURN:
                    customizing = False
                    return SNAKE_COLORS[color_idx]
                if event.key == pg.K_b:
                    return None

def start_menu():
    menu = True
    snake_color = BLUE
    while menu:
        screen.fill(BLACK)
        message("Welcome to Snake!", BLUE, WIDTH // 3, HEIGHT // 4)
        message("Press SPACE to Start", WHITE, WIDTH // 3, HEIGHT // 2)
        message("Press C for Customization", WHITE, WIDTH // 3, HEIGHT // 2 + 40)
        message("Press Q to Quit", WHITE, WIDTH // 3, HEIGHT // 2 + 80)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    menu = False
                if event.key == pg.K_c:
                    color = customization_menu()
                    if color:
                        snake_color = color
                if event.key == pg.K_q:
                    pg.quit()
                    quit()
    return snake_color

def gameloop(snake_color):
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
                        gameloop(snake_color)
                        return
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and x_change == 0:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pg.K_RIGHT and x_change == 0:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pg.K_UP and y_change == 0:
                    y_change = -SNAKE_SIZE
                    x_change = 0
                elif event.key == pg.K_DOWN and y_change == 0:
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
            pg.draw.rect(screen, snake_color, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])
        pg.display.update()
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
            length += 1
        clock.tick(SPEED)
    pg.quit()
    quit()

snake_color = start_menu()
gameloop(snake_color)