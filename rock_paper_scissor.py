import random
import pygame
import sys

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

# --- Game Choices ---
CHOICES = ['Rock', 'Paper', 'Scissors']
BUTTONS = []  # Will hold button rects and labels

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)

# --- Helper to Draw Buttons ---
def draw_buttons():
    BUTTONS.clear()
    for i, choice in enumerate(CHOICES):
        rect = pygame.Rect(60 + i*140, 300, 120, 50)
        pygame.draw.rect(screen, BLUE, rect)
        label = font.render(choice, True, WHITE)
        screen.blit(label, (rect.x + 10, rect.y + 10))
        BUTTONS.append((rect, choice))

# --- Helper to Draw Buttons with Animation ---
def draw_buttons(active_idx=None, shake_offset=0):
    BUTTONS.clear()
    for i, choice in enumerate(CHOICES):
        # Animate button color on hover/click
        color = (70, 130, 180) if i == active_idx else BLUE
        rect = pygame.Rect(60 + i*140 + (shake_offset if i == active_idx else 0), 300, 120, 50)
        pygame.draw.rect(screen, color, rect)
        label = font.render(choice, True, WHITE)
        screen.blit(label, (rect.x + 10, rect.y + 10))
        BUTTONS.append((rect, choice))

# --- Helper to Get Winner ---
def get_winner(player, computer):
    if player == computer:
        return "Draw!"
    if (player == 'Rock' and computer == 'Scissors') or \
       (player == 'Paper' and computer == 'Rock') or \
       (player == 'Scissors' and computer == 'Paper'):
        return "You Win!"
    return "You Lose!"

# --- Splash Screen for Win Condition ---
def show_winner(winner):
    # Display a splash screen when someone reaches 5 wins
    while True:
        screen.fill((50, 205, 50))
        msg = font.render(f"{winner} Wins!", True, WHITE)
        play_again = small_font.render("Press SPACE to play again or Q to quit", True, BLACK)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
        screen.blit(play_again, (WIDTH//2 - play_again.get_width()//2, HEIGHT//2 + 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Play again
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# --- Main Game Loop ---
def main():
    player_score = 0
    computer_score = 0
    player_choice = None
    computer_choice = None
    result = ""
    running = True
    animating = False
    anim_idx = None
    shake_frames = 0
    WIN_SCORE = 5  # Win condition
    while running:
        screen.fill(GRAY)
        title = font.render("Rock Paper Scissors", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        # Draw score counter
        score_text = small_font.render(f"You: {player_score}   Computer: {computer_score}", True, BLACK)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 70))
        # Handle animation
        shake_offset = 0
        if animating and shake_frames > 0:
            shake_offset = (-5 if shake_frames % 2 == 0 else 5)
            shake_frames -= 1
            if shake_frames == 0:
                animating = False
        # Draw buttons with animation
        mouse_pos = pygame.mouse.get_pos()
        hover_idx = None
        for i, (rect, _) in enumerate(BUTTONS):
            if rect.collidepoint(mouse_pos):
                hover_idx = i
        draw_buttons(active_idx=anim_idx if animating else hover_idx, shake_offset=shake_offset)
        # Show choices and result
        if player_choice:
            player_text = small_font.render(f"You: {player_choice}", True, BLACK)
            comp_text = small_font.render(f"Computer: {computer_choice}", True, BLACK)
            result_text = font.render(result, True, BLACK)
            screen.blit(player_text, (60, 120))
            screen.blit(comp_text, (60, 160))
            screen.blit(result_text, (60, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not animating:
                pos = pygame.mouse.get_pos()
                for idx, (rect, choice) in enumerate(BUTTONS):
                    if rect.collidepoint(pos):
                        # Start shake animation for selected button
                        animating = True
                        anim_idx = idx
                        shake_frames = 6
                        # Set choices and result after animation
                        player_choice = choice
                        computer_choice = random.choice(CHOICES)
                        result = get_winner(player_choice, computer_choice)
                        # Update scores
                        if result == "You Win!":
                            player_score += 1
                        elif result == "You Lose!":
                            computer_score += 1
                        # Check win condition
                        if player_score == WIN_SCORE or computer_score == WIN_SCORE:
                            winner = "You" if player_score == WIN_SCORE else "Computer"
                            play_again = show_winner(winner)
                            if play_again:
                                # Reset scores and choices
                                player_score = 0
                                computer_score = 0
                                player_choice = None
                                computer_choice = None
                                result = ""
                            else:
                                running = False
        pygame.display.update()
        pygame.time.delay(30)
    pygame.quit()
    sys.exit()

# --- Run the Game ---
if __name__ == "__main__":
    main()