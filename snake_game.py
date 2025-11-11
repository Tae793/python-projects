import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Get screen information for fullscreen mode
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# TODO: this doesnt handle running on a secondary bigger display as i takes the primary display size so make sure to have the screen your running the program on, set as your main display (add some code to fix this in future)

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
SNAKE_SPEED = 8
wall_spawn_start_time = int(time.time())  # Track game start time
wall_list = []
wall_spawn_interval = 5.5  # seconds

# initial game state
food1_big = False
food2_big = False

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

def game_loop(food_eaten, SNAKE_SPEED):
    global wall_spawn_start_time
    global wall_list
    global food1_big
    global food2_big

    # boost berry variables
    boost_berry_size = SNAKE_BLOCK_SIZE * 2
    
    wall_list = [] # reset walls on game start
    wall_spawn_start_time = int(time.time())  # Also reset wall timer
    
    def display_speed(SNAKE_SPEED):
        value = speed_font.render("Speed: " + str(SNAKE_SPEED), True, WHITE)
        screen.blit(value, [0, 30])
        
        (SNAKE_SPEED + food_eaten*1.5)
    
    # game rules
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
            display_score(food_eaten)
            pygame.display.update()
            wall_blocks == spawn_wall(0)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(0, 6) # Restart the game

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
        
        if food1_big == True:
            pygame.draw.rect(screen, RED, [food_x, food_y, boost_berry_size, boost_berry_size])
        else:
            pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        if food2_big == True:
            pygame.draw.rect(screen, RED, [food_x2, food_y2, boost_berry_size, boost_berry_size])
        else:
            pygame.draw.rect(screen, RED, [food_x2, food_y2, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # food1_last_eaten = False
        # food2_last_eaten = False

        # Draw all walls
        for wall in wall_list:
            pygame.draw.rect(screen, WHITE, [wall[0], wall[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # Assuming x1, y1 are the new coordinates for the snake's head
        snake_head = [x1, y1]

        # --- Check for self-collision BEFORE adding the new head to snake_list ---
        for segment in snake_list: # Iterate through the *existing* snake body
            if snake_head == segment: # Compare the new head's position with existing body segments
                game_close = True
                break # No need to check further if a collision is found

        # --- If no collision, then update the snake's list ---
        if not game_over: # Only proceed if game is not over
            snake_list.append(snake_head)

            # Maintain the snake's length
            if len(snake_list) > length_of_snake:
                del snake_list[0]

        #speed increase
        speed_modifier = SNAKE_SPEED + food_eaten*4

        # drawing the snake and displaying the score
        our_snake(SNAKE_BLOCK_SIZE, snake_list)
        display_score(food_eaten)
        display_speed(speed_modifier)

        pygame.display.update()

        # FOOD1 Collision (Check if head position matches food position)
        if food1_big:
            if (food_x <= x1 < food_x + boost_berry_size) and (food_y <= y1 < food_y + boost_berry_size):
                # Snake eats the big fruit
                food_x, food_y = generate_food_position()
                length_of_snake += 3
                food_eaten += 2
                food1_big = False  # Reset to normal after eating
                while [food_x, food_y] in snake_list:
                    food_x, food_y = generate_food_position()
        else:
            if x1 == food_x and y1 == food_y:
                food_x, food_y = generate_food_position()
                length_of_snake += 3
                food_eaten += 1
                food1_big = True
                # Important: Make sure new food doesn't spawn on the snake
                # This is a common bug: the food should NOT be on the current snake body
                while [food_x, food_y] in snake_list:
                    food_x, food_y = generate_food_position()

        # FOOD2 Collision for x2 and y2(Check if head position matches food position)
        if food2_big:
            if (food_x2 <= x1 < food_x2 + boost_berry_size) and (food_y2 <= y1 < food_y2 + boost_berry_size):
                # Snake eats the big fruit
                food_x2, food_y2 = generate_food_position()
                length_of_snake += 2
                food_eaten += 1
                food2_big = False  # Reset to normal after eating
                while [food_x2, food_y2] in snake_list:
                    food_x2, food_y2 = generate_food_position()
        else:
            if x1 == food_x2 and y1 == food_y2:
                food_x2, food_y2 = generate_food_position()
                length_of_snake += 2
                food_eaten += 1
                food2_big = True
                # Important: Make sure new food doesn't spawn on the snake (for x2 and y2)
                # This is a common bug: the food should NOT be on the current snake body
                while [food_x2, food_y2] in snake_list:
                    food_x2, food_y2 = generate_food_position()

        # walls implementation
        def spawn_wall(length):
            # Randomly choose orientation: 0 = horizontal, 1 = vertical
            orientation = random.choice([0, 1])
            while True:
                wall_blocks = []
                wall_x = random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
                wall_y = random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
                for i in range(length):
                    if orientation == 0:  # horizontal
                        wx = wall_x + i * SNAKE_BLOCK_SIZE
                        wy = wall_y
                    else:  # vertical
                        wx = wall_x
                        wy = wall_y + i * SNAKE_BLOCK_SIZE
                    # Check bounds
                    if wx >= SCREEN_WIDTH or wy >= SCREEN_HEIGHT:
                        break
                    wall_blocks.append([wx, wy])
                # Make sure all blocks are valid and not on snake or food
                if (len(wall_blocks) == length and
                    all(block not in snake_list and
                        block != [food_x, food_y] and
                        block != [food_x2, food_y2] for block in wall_blocks)):
                    return wall_blocks
        # Generate a wall block not on the snake or food
            while True:
                wall_x = random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
                wall_y = random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
                if ([wall_x, wall_y] not in snake_list and
                    [wall_x, wall_y] != [food_x, food_y] and
                    [wall_x, wall_y] != [food_x2, food_y2]):
                    wall_spawn_start_time = current_time
                    return [wall_x, wall_y]
    
        # --- Wall spawning logic ---
        current_time = int(time.time())
        if current_time - wall_spawn_start_time >= wall_spawn_interval:
            wall_blocks = spawn_wall(length=random.randint(5, 10))
            wall_list.extend(wall_blocks)
            wall_spawn_start_time = current_time  # <-- Reset timer here

        # --- Check for collision with walls ---
        for wall in wall_list:
            if snake_head == wall:
                game_close = True
                break
               
        clock.tick(speed_modifier)

    pygame.quit()
    quit()

game_loop(food_eaten, SNAKE_SPEED)
