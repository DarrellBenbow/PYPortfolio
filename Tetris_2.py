import pygame
import random

#initialize pygame
pygame.init()

#Screen/grid setup
CELL_SIZE = 30
COLUMNS = 12  # Was 10
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH + 120, HEIGHT))  # Extra width for next piece box
pygame.display.set_caption("Tetris")
CLOCK = pygame.time.Clock()

#Colors
BLACK = (0, 0, 0)
GRAY = (128, 128,128)
COLORS = [
    (255, 0, 0),   # Red I
    (0, 255, 0),   # Green J
    (0, 0, 255),   # Blue L
    (255, 255, 0), # Yellow O
    (255, 165, 0), # Orange S
    (75, 0, 130),  # Indigo T
    (238, 130, 238) # Violet Z   
    
]

#Tetromino shapes with full rotation states
SHAPES = [
    # I
    [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    # J
    [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    # L
    [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ],
    [    # O
        [[1, 1],
         [1, 1]]
    ],
    [    # S
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    [    # T
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    [    # Z
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]    
        ]
    ]     
]


# Grid builder
def create_grid(locked_positions):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLUMNS):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

# piece class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0
    def image(self):
        return self.shape[self.rotation % len(self.shape)]
    def cells(self):
        positions = []
        shape = self.image()
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val == 1:
                    positions.append((self.x + j, self.y + i))
        return positions

# Helper functions
def convert_shape_format(piece):
    return piece.cells()

def valid_space(piece, grid):
    valid = [[(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
    valid = [pos for now in valid for pos in now]
    for pos in convert_shape_format(piece):
        if pos not in valid:
            if pos[1] >= 0:
                return False
    return True

def check_lost(locked):
    return any(y < 1 for (_, y) in locked)

def get_shape():
    return Piece(3, 0, random.choice(SHAPES))

def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(screen, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for y in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))
    for x in range(COLUMNS):
        pygame.draw.line(screen, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
        
def clear_rows(grid, locked_positions):
    cleared = 0
    for y in range(ROWS - 1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            for x in range(COLUMNS):
                try:
                    del locked_positions[(x, y)]
                except:
                    continue
            for key in sorted(list(locked_positions), key=lambda k: k[1])[::-1]:
                x, y2 = key
                if y2 < y:
                    new_key = (x, y2 + 1)
                    locked_positions[new_key] = locked_positions.pop(key)
    return cleared

# Draws the window, including the next piece preview

def draw_window(grid, next_piece):
    screen.fill(BLACK)
    draw_grid(grid)
    # Draw next piece preview box
    pygame.draw.rect(screen, GRAY, (WIDTH + 20, 30, 80, 80), 2)
    font = pygame.font.SysFont('Arial', 20)
    label = font.render('Next:', True, (255, 255, 255))
    screen.blit(label, (WIDTH + 30, 10))
    # Draw next piece in the preview box
    preview = next_piece.image()
    for i, row in enumerate(preview):
        for j, val in enumerate(row):
            if val == 1:
                pygame.draw.rect(
                    screen,
                    next_piece.color,
                    (WIDTH + 30 + j * CELL_SIZE // 2, 40 + i * CELL_SIZE // 2, CELL_SIZE // 2, CELL_SIZE // 2)
                )
    pygame.display.update()

# Start menu function

def start_menu():
    font = pygame.font.SysFont('Arial', 40)
    small_font = pygame.font.SysFont('Arial', 24)
    waiting = True
    while waiting:
        screen.fill(BLACK)
        title = font.render('TETRIS', True, (255, 255, 255))
        prompt = small_font.render('Press SPACE to Start', True, (200, 200, 200))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Main game loop

def main():
    start_menu()  # Show start menu before game starts
    locked_positions = {}
    current_piece = get_shape()
    next_piece = get_shape()
    grid = create_grid(locked_positions)
    fall_time = 0
    fall_speed = 0.4
    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += CLOCK.get_rawtime()
        CLOCK.tick()
        # Piece falls every fall_speed seconds
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()
                if check_lost(locked_positions):
                    running = False
        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
        # Draw current piece on grid
        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                grid[y][x] = current_piece.color
        clear_rows(grid, locked_positions)
        draw_window(grid, next_piece)
    pygame.quit()
# start the game
if __name__ == "__main__":
    main()

