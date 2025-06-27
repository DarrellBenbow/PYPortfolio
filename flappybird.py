import pygame
import random

# --- Constants and Color Options ---
WIDTH, HEIGHT = 800, 600
FPS = 60
BIRD_SIZE = 30
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.5

# Color options for customization
COLOR_OPTIONS = {
    'Background': [(135, 206, 235), (0, 0, 0), (255, 255, 255)],
    'Bird': [(255, 255, 0), (255, 0, 0), (0, 255, 255)],
    'Pipe': [(0, 255, 0), (255, 0, 255), (255, 165, 0)]
}
COLOR_NAMES = {
    (135, 206, 235): 'Sky Blue', (0, 0, 0): 'Black', (255, 255, 255): 'White',
    (255, 255, 0): 'Yellow', (255, 0, 0): 'Red', (0, 255, 255): 'Cyan',
    (0, 255, 0): 'Green', (255, 0, 255): 'Magenta', (255, 165, 0): 'Orange'
}
# Add these color constants for use in text rendering
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 40)
menu_font = pygame.font.SysFont("Arial", 32)

# --- Customization Defaults ---
selected_colors = {
    'Background': COLOR_OPTIONS['Background'][0],
    'Bird': COLOR_OPTIONS['Bird'][0],
    'Pipe': COLOR_OPTIONS['Pipe'][0]
}

# --- Start Menu Logic ---
def start_menu():
    menu_items = list(COLOR_OPTIONS.keys()) + ['Start Game']
    selection = [0, 0, 0]  # Index for each color option
    current_item = 0
    while True:
        screen.fill((30, 30, 30))
        title = game_over_font.render('Flappy Bird - Customization', True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == current_item else (200, 200, 200)
            if item == 'Start Game':
                text = menu_font.render('> Start Game <' if i == current_item else 'Start Game', True, color)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 350))
            else:
                opt_idx = selection[i]
                opt_color = COLOR_OPTIONS[item][opt_idx]
                opt_name = COLOR_NAMES[opt_color]
                label = f"{item}: {opt_name}"
                text = menu_font.render(label, True, color)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 120 + i * 60))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_item = (current_item - 1) % len(menu_items)
                if event.key == pygame.K_DOWN:
                    current_item = (current_item + 1) % len(menu_items)
                if event.key == pygame.K_LEFT and current_item < 3:
                    selection[current_item] = (selection[current_item] - 1) % len(COLOR_OPTIONS[menu_items[current_item]])
                if event.key == pygame.K_RIGHT and current_item < 3:
                    selection[current_item] = (selection[current_item] + 1) % len(COLOR_OPTIONS[menu_items[current_item]])
                if event.key == pygame.K_RETURN and current_item == 3:
                    # Apply selected colors
                    for idx, key in enumerate(COLOR_OPTIONS.keys()):
                        selected_colors[key] = COLOR_OPTIONS[key][selection[idx]]
                    return

# --- Game Logic Functions ---
def create_pipe():
    height = random.randint(100, 400)
    top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    return {"top": top, "bottom": bottom, "passed": False}

def reset_game():
    global bird_movement, pipes, score, active
    bird.x, bird.y = 50, 300
    bird_movement = 0
    pipes.clear()
    score = 0
    active = True

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, selected_colors['Pipe'], pipe["top"])
        pygame.draw.rect(screen, selected_colors['Pipe'], pipe["bottom"])

def move_pipes():
    for pipe in pipes:
        pipe["top"].x -= 3
        pipe["bottom"].x -= 3

def remove_offscreen_pipes():
    global pipes
    pipes = [pipe for pipe in pipes if pipe["top"].right > 0]

def check_collision():
    for pipe in pipes:
        if bird.colliderect(pipe["top"]) or bird.colliderect(pipe["bottom"]):
            return True
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return True
    return False

def update_score():
    global score
    for pipe in pipes:
        if not pipe["passed"] and pipe["top"].right < bird.left:
            score += 1
            pipe["passed"] = True

def draw_score():
    score_surface = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))

def draw_game_over():
    game_over_text = game_over_font.render("Game Over", True, RED)
    restart_text = font.render("Press SPACE to Restart", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 90, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2))

# --- Main Game Loop ---
def main():
    global bird, bird_movement, score, active, pipes
    bird = pygame.Rect(50, 300, BIRD_SIZE, BIRD_SIZE)
    bird_movement = 0
    score = 0
    active = True
    pipes = []
    spawn_pipe = pygame.USEREVENT
    pygame.time.set_timer(spawn_pipe, 1500)
    running = True
    while running:
        screen.fill(selected_colors['Background'])  # Use selected background color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if active:
                    bird_movement = -8
                else:
                    reset_game()
            if event.type == spawn_pipe and active:
                pipes.append(create_pipe())
        if active:
            bird_movement += GRAVITY
            bird.y += bird_movement
            pygame.draw.ellipse(screen, selected_colors['Bird'], bird)  # Use selected bird color
            move_pipes()
            draw_pipes()
            remove_offscreen_pipes()
            if check_collision():
                active = False
            update_score()
            draw_score()
        else:
            draw_game_over()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()

# --- Run Start Menu then Game ---
if __name__ == "__main__":
    start_menu()  # Show customization menu before game starts
    main()
