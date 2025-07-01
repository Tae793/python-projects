import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Screen Dimensions ---
# Use fixed dimensions for simplicity, or uncomment lines for fullscreen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# If you want fullscreen, uncomment these lines and comment out the above:
# info = pygame.display.Info()
# SCREEN_WIDTH = info.current_w
# SCREEN_HEIGHT = info.current_h
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Simple Racing Game")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# --- Game Variables ---
CAR_WIDTH = 50
CAR_HEIGHT = 80
LANE_WIDTH = SCREEN_WIDTH // 3 # Divide screen into 3 equal lanes
ROAD_LEFT_EDGE = (SCREEN_WIDTH - (LANE_WIDTH * 3)) // 2 # Center the road
ROAD_RIGHT_EDGE = ROAD_LEFT_EDGE + (LANE_WIDTH * 3)

PLAYER_SPEED = 7
OBSTACLE_SPEED = 5 # Initial obstacle speed
SPEED_INCREASE_INTERVAL = 5000 # Increase speed every 5 seconds (in ms)
SPEED_INCREASE_AMOUNT = 0.5

SCORE_FONT_SIZE = 30
GAME_OVER_FONT_SIZE = 60

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([CAR_WIDTH, CAR_HEIGHT])
        self.image.fill(BLUE) # Player car color
        self.rect = self.image.get_rect()
        self.rect.centerx = ROAD_LEFT_EDGE + LANE_WIDTH + (LANE_WIDTH // 2) # Start in middle lane
        self.rect.bottom = SCREEN_HEIGHT - 20 # Start near bottom of screen
        self.lane = 1 # 0 for left, 1 for middle, 2 for right

    def update(self):
        # Handle player input to change lanes
        pass # Movement handled directly by game loop for simplicity here

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.rect.centerx = ROAD_LEFT_EDGE + (self.lane * LANE_WIDTH) + (LANE_WIDTH // 2)

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            self.rect.centerx = ROAD_LEFT_EDGE + (self.lane * LANE_WIDTH) + (LANE_WIDTH // 2)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([CAR_WIDTH, CAR_HEIGHT])
        self.image.fill(RED) # Obstacle car color
        self.rect = self.image.get_rect()

        # Randomly choose a lane for the obstacle
        lane_choice = random.randint(0, 2)
        self.rect.centerx = ROAD_LEFT_EDGE + (lane_choice * LANE_WIDTH) + (LANE_WIDTH // 2)
        self.rect.bottom = 0 # Start off-screen at the top

    def update(self, speed):
        self.rect.y += speed
        # Remove obstacle if it goes off-screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Remove from all sprite groups

# --- Drawing Functions ---

def draw_road_and_lanes(screen):
    screen.fill(GRAY) # Road color

    # Draw lane lines
    for i in range(1, 3): # Two lines for three lanes
        line_x = ROAD_LEFT_EDGE + (i * LANE_WIDTH)
        pygame.draw.line(screen, WHITE, (line_x, 0), (line_x, SCREEN_HEIGHT), 5) # White lines

    # Draw road edges
    pygame.draw.rect(screen, BLACK, (0, 0, ROAD_LEFT_EDGE, SCREEN_HEIGHT)) # Left border
    pygame.draw.rect(screen, BLACK, (ROAD_RIGHT_EDGE, 0, SCREEN_WIDTH - ROAD_RIGHT_EDGE, SCREEN_HEIGHT)) # Right border

def display_score(screen, score):
    font = pygame.font.Font(None, SCORE_FONT_SIZE)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10)) # Top-left corner

def game_over_screen(screen, score):
    font_large = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
    font_small = pygame.font.Font(None, SCORE_FONT_SIZE)

    game_over_text = font_large.render("Game Over!", True, RED)
    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True # Restart
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# --- Main Game Loop ---

def game():
    player = Player()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True
    game_over = False
    score = 0
    current_obstacle_speed = OBSTACLE_SPEED

    # Timers for obstacle spawning and speed increase
    obstacle_spawn_time = pygame.time.get_ticks()
    speed_increase_time = pygame.time.get_ticks()
    OBSTACLE_SPAWN_DELAY = 1500 # milliseconds

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        if not game_over:
            # Spawn new obstacles
            current_time = pygame.time.get_ticks()
            if current_time - obstacle_spawn_time > OBSTACLE_SPAWN_DELAY:
                obstacle = Obstacle()
                # Ensure obstacle doesn't spawn on existing obstacles immediately (optional, for simple game might be okay)
                # while pygame.sprite.spritecollideany(obstacle, obstacles):
                #     obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                obstacle_spawn_time = current_time

            # Increase speed over time
            if current_time - speed_increase_time > SPEED_INCREASE_INTERVAL:
                current_obstacle_speed += SPEED_INCREASE_AMOUNT
                OBSTACLE_SPAWN_DELAY = max(500, OBSTACLE_SPAWN_DELAY - 50) # Make obstacles spawn faster, min 0.5s
                speed_increase_time = current_time

            # Update sprites
            obstacles.update(current_obstacle_speed)

            # Check for collisions
            if pygame.sprite.spritecollideany(player, obstacles):
                game_over = True

            # Score logic (based on time or obstacles passed)
            # For simplicity, score increases with time
            score += 1 # Increase score every frame

        # Drawing
        draw_road_and_lanes(screen)
        all_sprites.draw(screen) # Draw all sprites
        display_score(screen, score // 10) # Divide by 10 for a more reasonable score

        pygame.display.flip()
        clock.tick(60) # 60 frames per second

        if game_over:
            if game_over_screen(screen, score // 10):
                game() # Restart the game
            else:
                running = False # Quit

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    print("race")
    game()