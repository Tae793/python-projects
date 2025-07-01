import pygame
import random

# Initialize Pygame
pygame.init()

# Get screen information for fullscreen mode
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Create the screen in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Simple Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake properties
SNAKE_BLOCK_SIZE = 20 # Keep this consistent for grid
food_eaten = 0

# Fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
speed_font = pygame.font.SysFont(None, 35)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
    screen.blit(mesg, text_rect)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

def game_loop(food_eaten):
    
    def display_speed(SNAKE_SPEED):
        value = speed_font.render("Speed: " + str(SNAKE_SPEED), True, WHITE)
        screen.blit(value, [0, 30])
        
        (SNAKE_SPEED + food_eaten*2)
    
    # snake spped and game rules
    
    SNAKE_SPEED = 6
    print(SNAKE_SPEED)
    game_over = False
    game_close = False

    # Snake initial position - ensuring it starts perfectly on the grid
    # We want it roughly in the center, snapped to the block size
    x1 = (SCREEN_WIDTH // 2)
    y1 = (SCREEN_HEIGHT // 2)

    # Snake initial direction (e.g., starts moving right)
    x1_change = SNAKE_BLOCK_SIZE
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Function to generate food position on the grid
    def generate_food_position():
        # Generate coordinates that are perfect multiples of SNAKE_BLOCK_SIZE
        # Ensure food spawns within bounds, leaving space for the block itself
        food_x = random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        food_y = random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        return round(food_x),round(food_y)

    food_x, food_y = generate_food_position()
    food_x2, food_y2 = generate_food_position()

    clock = pygame.time.Clock()

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop() # Restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Prevent immediate reversal
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK_SIZE
                    x1_change = 0

        # Update snake position. These are always perfectly on the grid.
        x1 += x1_change
        y1 += y1_change

        # --- Collision Checks ---

        # Wall passthrough
        if x1 < 0:
            x1 = SCREEN_WIDTH + x1
        
        if x1 >= SCREEN_WIDTH:
            x1 = SCREEN_WIDTH - x1
        
        if y1 < 0: 
            y1 = SCREEN_HEIGHT+ y1

        if y1 >= SCREEN_HEIGHT:
            y1 = SCREEN_HEIGHT - y1
        

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
        pygame.draw.rect(screen, RED, [food_x2, food_y2, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # Prepare snake head and add to list
        snake_head = [x1, y1] # Using list literal for clarity
        snake_list.append(snake_head)

        for x, y in snake_list[1:]:
            if len(snake_list) > 1 and snake_head[0] == x and snake_head[1] == y:
                game_over = False # TODO FIX THIS

        # Remove tail if snake is too long
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # drawing the snake and displaying the score
        our_snake(SNAKE_BLOCK_SIZE, snake_list)
        display_score(length_of_snake - 1)
        display_speed(SNAKE_SPEED + food_eaten*2)

        pygame.display.update()

        # Food Collision (Check if head position matches food position)
        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food_position()
            length_of_snake += 3
            food_eaten += 1

            # Important: Make sure new food doesn't spawn on the snake
            # This is a common bug: the food should NOT be on the current snake body
            while [food_x, food_y] in snake_list:
                food_x, food_y = generate_food_position()

        # Food Collision for x2 and y2(Check if head position matches food position)
        if x1 == food_x2 and y1 == food_y2:
            food_x2, food_y2 = generate_food_position()
            length_of_snake += 3
            food_eaten += 1

            # Important: Make sure new food doesn't spawn on the snake (for x2 and y2)
            # This is a common bug: the food should NOT be on the current snake body
            while [food_x2, food_y2] in snake_list:
                food_x2, food_y2 = generate_food_position()

        clock.tick(SNAKE_SPEED + food_eaten*2)

    pygame.quit()
    quit()

game_loop(food_eaten)