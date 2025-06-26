import pygame as pg
import time

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Tron Game")
clock = pg.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)   
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLOCK_SIZE = 10
SPEED = 30

class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.position = start_pos
        self.direction = (0, 0)
        self.trail = []

    def move(self):
        if self.direction != (0, 0):
            new_pos = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            self.trail.append(self.position)
            self.position = new_pos

    def change_direction(self, new_direction):
        # Prevent reversing direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, surface):
        for pos in self.trail:
            pg.draw.rect(surface, self.color, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def customization_menu():
    COLORS = [RED, BLUE, GREEN, YELLOW, WHITE]
    COLOR_NAMES = ["Red", "Blue", "Green", "Yellow", "White"]
    idx1, idx2 = 0, 1
    customizing = True
    font = pg.font.SysFont(None, 36)
    while customizing:
        screen.fill(BLACK)
        t1 = font.render(f'Player 1 Color: {COLOR_NAMES[idx1]}', True, COLORS[idx1])
        t2 = font.render(f'Player 2 Color: {COLOR_NAMES[idx2]}', True, COLORS[idx2])
        t3 = font.render('Arrows: P1, WASD: P2', True, WHITE)
        t4 = font.render('Left/Right: P1 Color, A/D: P2 Color', True, WHITE)
        t5 = font.render('Press SPACE to Start', True, WHITE)
        screen.blit(t1, (220, 150))
        screen.blit(t2, (220, 200))
        screen.blit(t3, (220, 250))
        screen.blit(t4, (120, 300))
        screen.blit(t5, (220, 400))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    idx1 = (idx1 - 1) % len(COLORS)
                if event.key == pg.K_RIGHT:
                    idx1 = (idx1 + 1) % len(COLORS)
                if event.key == pg.K_a:
                    idx2 = (idx2 - 1) % len(COLORS)
                if event.key == pg.K_d:
                    idx2 = (idx2 + 1) % len(COLORS)
                if event.key == pg.K_SPACE:
                    customizing = False
    return COLORS[idx1], COLORS[idx2]

def main():
    p1_color, p2_color = customization_menu()
    player1 = Player(p1_color, (100, 100))
    player1.direction = (BLOCK_SIZE, 0)
    player2 = Player(p2_color, (700, 500))
    player2.direction = (-BLOCK_SIZE, 0)
    players = [player1, player2]
    running = True
    game_over = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        # Player 1: Arrow keys
        if keys[pg.K_LEFT]: player1.change_direction((-BLOCK_SIZE, 0))
        if keys[pg.K_RIGHT]: player1.change_direction((BLOCK_SIZE, 0))
        if keys[pg.K_UP]: player1.change_direction((0, -BLOCK_SIZE))
        if keys[pg.K_DOWN]: player1.change_direction((0, BLOCK_SIZE))
        # Player 2: WASD
        if keys[pg.K_a]: player2.change_direction((-BLOCK_SIZE, 0))
        if keys[pg.K_d]: player2.change_direction((BLOCK_SIZE, 0))
        if keys[pg.K_w]: player2.change_direction((0, -BLOCK_SIZE))
        if keys[pg.K_s]: player2.change_direction((0, BLOCK_SIZE))
        if not game_over:
            screen.fill(BLACK)
            for player in players:
                player.move()
            # Collision detection
            for idx, player in enumerate(players):
                # Wall collision
                x, y = player.position
                if x < 0 or x >= 800 or y < 0 or y >= 600:
                    game_over = True
                # Trail collision (with self and other)
                for other in players:
                    for pos in other.trail:
                        if player.position == pos:
                            game_over = True
            for player in players:
                player.draw(screen)
            pg.display.flip()
            clock.tick(SPEED)
        else:
            font = pg.font.SysFont(None, 48)
            text = font.render('Game Over! Press R to Restart or Q to Quit', True, WHITE)
            screen.blit(text, (100, 250))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        main()
                        return
                    if event.key == pg.K_q:
                        running = False
    pg.quit()

if __name__ == "__main__":
    main()