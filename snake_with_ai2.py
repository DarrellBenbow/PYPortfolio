import pygame
import time
import random

#initialize pygame
pygame.init()

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

#Display settings
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 10
SPEED = 15

#Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake with AI') 

#clock to control game speed
clock = pygame.time.Clock()

#Font settings
font_style = pygame.font.SysFont("bahnschrift", 25)

#High Score
high_score = 0

def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])
    
def ai_move(x, y, food_x, food_y, snake):
    possible_moves = [(-SNAKE_SIZE, 0), (SNAKE_SIZE, 0), (0, -SNAKE_SIZE), (0, SNAKE_SIZE)]
    best_move = None
    min_distance = float('inf')
    
    for move in possible_moves:
        new_x, new_y = x + move[0], y + move[1]
        if [new_x, new_y] in snake or new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            continue # Avoid moving into itself or out of bounds
        
        distance = abs(new_x - food_x) + abs(new_y - food_y)
        if distance < min_distance:
            min_distance = distance
            best_move = move
            
    return best_move if best_move else (0, 0) # Defult to no movement if stuck

# --- Color Customization Menu ---
def color_menu():
    COLORS = [GREEN, BLUE, RED, WHITE]
    COLOR_NAMES = ["Green", "Blue", "Red", "White"]
    idx = 0
    font = pygame.font.SysFont("bahnschrift", 30)
    selecting = True
    while selecting:
        screen.fill(BLACK)
        title = font.render("Select Snake Color", True, WHITE)
        color_name = font.render(COLOR_NAMES[idx], True, COLORS[idx])
        prompt = font.render("Left/Right to change, Space to select", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(color_name, (WIDTH//2 - color_name.get_width()//2, HEIGHT//2))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    idx = (idx - 1) % len(COLORS)
                if event.key == pygame.K_RIGHT:
                    idx = (idx + 1) % len(COLORS)
                if event.key == pygame.K_SPACE:
                    selecting = False
    return COLORS[idx]

# --- Optimized Game Loop with Color Customization ---
def game_loop():
    global high_score
    # Let player choose snake color at the start
    snake_color = color_menu()
    game_over = False
    game_close = False
    is_ai = False
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0
    snake = []
    length = 1
    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message(f"Game Over! Score: {length-1} High Score: {high_score}", RED, WIDTH / 6, HEIGHT / 3)
            message("Press Q-Quit or C-Play Again", RED, WIDTH / 6, HEIGHT / 2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return game_loop()  # Restart with color selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_ai = not is_ai  # Toggle AI Control
                elif event.key == pygame.K_LEFT:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_SIZE
                    x_change = 0
        if is_ai:
            x_change, y_change = ai_move(x, y, food_x, food_y, snake)
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        x += x_change
        y += y_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
        snake.append([x, y])
        if len(snake) > length:
            del snake[0]
        for segment in snake[:-1]:
            if segment == [x, y]:
                game_close = True
        # Draw the snake with the selected color
        for segment in snake:
            pygame.draw.rect(screen, snake_color, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])
        pygame.display.update()
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
            length += 1
            high_score = max(high_score, length - 1)
        clock.tick(SPEED)
    pygame.quit()
    quit()
    
game_loop()
