import pygame
import random
import sys 

# Initialize Pygame
pygame.init()

#screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS = 6
LANE_HEIGHT = HEIGHT // ROWS
STEP = 20 #smaller jump size
JUMP_DELAY = 200 #milliseconds

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Frog class
class frog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 40
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.reset_position()
        self.last_jump = pygame.time.get_ticks()
    
    def reset_position(self):
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        
    def update(self, keys):
        now = pygame.time.get_ticks()
        if now - self.last_jump >= JUMP_DELAY:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= STEP
                self.last_jump = now
            elif keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += STEP
                self.last_jump = now
            elif keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= STEP 
                self.last_jump = now
            elif keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += STEP
                self.last_jump = now

# Car Class
class Car(pygame.sprite.Sprite):
    def __init__(self, y, speed):
        super().__init__()
        self.image = pygame.Surface((random.randint(60, 120,), 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-150, WIDTH + 150])
        self.rect.y = y
        self.speed = speed if self.rect.right < 0 else -speed
        
    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = WIDTH

#Setup
def create_cars(level):
    cars = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(frog)
    for i in range(1, ROWS - 1):
        for _ in range(4):
            car = Car(i * LANE_HEIGHT + 10, random.randint(3 + level, 6 + level))
            cars.add(car)
            all_sprites.add(car)
    return cars, all_sprites

frog = frog()
level = 1
score = 0 
lives = 3
cars, all_sprites = create_cars(level)

# Game Loop
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    frog.update(keys)
    cars.update()
    
    # Collision detection
    if pygame.sprite.spritecollideany(frog, cars):
        lives -= 1
        frog.reset_position()
        if lives == 0:
            print("Game Over!")
            running = False
    # Victory condition
    if frog.rect.top < 10:
        score += 1
        level += 1
        frog.reset_position()
        cars, all_sprites = create_cars(level)
        
    # Drawing
    screen.fill(WHITE)
    
    # Draw sidewalk and road
    pygame.draw.rect(screen, DARK_GRAY, (0, LANE_HEIGHT, WIDTH, LANE_HEIGHT * (ROWS - 2))) # road
    pygame.draw.rect(screen, GRAY, (0,0, WIDTH, LANE_HEIGHT)) # TOP SIDEWALK
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - LANE_HEIGHT,WIDTH,LANE_HEIGHT)) # bottom sidewalk
    
    all_sprites.draw(screen)
    
    # Draw score and lives
    score_text = font.render(f"score: {score}]", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 130, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
    

    
        