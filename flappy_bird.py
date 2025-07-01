import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100  # Height of the ground from the bottom

BIRD_SIZE = 20
BIRD_X = 70  # Fixed X position of the bird

GRAVITY = 0.4
JUMP_STRENGTH = -8

PIPE_WIDTH = 65
PIPE_GAP = 140  # Gap between top and bottom pipes
PIPE_SPEED = 4

SCORE_FONT_SIZE = 48

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)
BROWN = (139, 69, 19) # Ground color
YELLOW = (255, 255, 0) # Bird color

# --- Set up the display ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird (Basic)")

# --- Fonts ---
font = pygame.font.Font(None, SCORE_FONT_SIZE)
game_over_font = pygame.font.Font(None, 64)
restart_font = pygame.font.Font(None, 32)

# --- Game Variables ---
bird_y = SCREEN_HEIGHT // 2 - BIRD_SIZE // 2
bird_velocity = 0
score = 0
game_active = True # True when game is running, False when game over

# List to store pipes (each pipe is a dictionary with 'top_rect', 'bottom_rect', 'passed')
pipes = []

# --- Functions ---

def create_pipe():
    """Creates a new pair of top and bottom pipes."""
    # Random height for the gap's center
    pipe_center_y = random.randint(PIPE_GAP, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP)

    # Top pipe rectangle (x, y, width, height)
    top_pipe_height = pipe_center_y - PIPE_GAP // 2
    top_pipe_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, top_pipe_height)

    # Bottom pipe rectangle
    bottom_pipe_height = SCREEN_HEIGHT - GROUND_HEIGHT - (pipe_center_y + PIPE_GAP // 2)
    bottom_pipe_rect = pygame.Rect(SCREEN_WIDTH, pipe_center_y + PIPE_GAP // 2, PIPE_WIDTH, bottom_pipe_height)

    pipes.append({'top_rect': top_pipe_rect, 'bottom_rect': bottom_pipe_rect, 'passed': False})

def draw_pipes():
    """Draws all pipes on the screen."""
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe['top_rect'])
        pygame.draw.rect(screen, GREEN, pipe['bottom_rect'])

def move_pipes():
    """Moves pipes from right to left and removes off-screen pipes."""
    global score, game_active

    for pipe in pipes:
        pipe['top_rect'].x -= PIPE_SPEED
        pipe['bottom_rect'].x -= PIPE_SPEED

        # Check if bird passed the pipe for scoring
        if not pipe['passed'] and pipe['top_rect'].right < BIRD_X:
            score += 1
            pipe['passed'] = True

    # Remove pipes that have moved off-screen
    pipes[:] = [pipe for pipe in pipes if pipe['top_rect'].right > 0]

def check_collisions(bird_rect):
    """Checks for collisions between the bird and pipes or ground."""
    global game_active

    # Collision with ground
    if bird_rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
        game_active = False
        return

    # Collision with ceiling
    if bird_rect.top <= 0:
        game_active = False
        return

    # Collision with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top_rect']) or bird_rect.colliderect(pipe['bottom_rect']):
            game_active = False
            return

def draw_ground():
    """Draws the ground at the bottom of the screen."""
    pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    # Add a thin black line to separate ground from sky
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 2)

def reset_game():
    """Resets all game variables for a new game."""
    global bird_y, bird_velocity, score, game_active, pipes
    bird_y = SCREEN_HEIGHT // 2 - BIRD_SIZE // 2
    bird_velocity = 0
    score = 0
    pipes = []
    game_active = True
    create_pipe_event() # Re-schedule pipe creation

# --- Custom Events ---
# Event for creating new pipes at regular intervals
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500) # Create a new pipe every 1.5 seconds

# This function is called once to initially schedule pipe creation
def create_pipe_event():
    pygame.time.set_timer(SPAWNPIPE, 1500) # Ensure timer is set when game resets

# --- Game Loop ---
clock = pygame.time.Clock()
create_pipe_event() # Initial call to start pipe creation

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_velocity = JUMP_STRENGTH
            if event.key == pygame.K_SPACE and not game_active:
                reset_game() # Restart game on spacebar press if game over

        if event.type == SPAWNPIPE and game_active:
            create_pipe()

    if game_active:
        # Bird movement
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Keep bird within screen bounds (top)
        if bird_y < 0:
            bird_y = 0
            bird_velocity = 0 # Stop upward movement if hit ceiling

        # Update bird rectangle for collision detection
        bird_rect = pygame.Rect(BIRD_X, bird_y, BIRD_SIZE, BIRD_SIZE)

        # Pipe movement and collision
        move_pipes()
        check_collisions(bird_rect)

    # --- Drawing ---
    screen.fill(BLUE) # Sky background

    draw_pipes()
    draw_ground()

    # Draw bird
    bird_rect = pygame.Rect(BIRD_X, bird_y, BIRD_SIZE, BIRD_SIZE)
    pygame.draw.rect(screen, YELLOW, bird_rect, border_radius=5) # Bird with rounded corners

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Game Over screen
    if not game_active:
        game_over_text = game_over_font.render("GAME OVER", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(game_over_text, game_over_rect)

        restart_text = restart_font.render("Press SPACE to Restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(restart_text, restart_rect)


    pygame.display.flip() # Update the full display Surface to the screen
    clock.tick(60) # Cap the frame rate at 60 FPS