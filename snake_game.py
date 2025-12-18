import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Get screen information for fullscreen mode
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# TODO: this doesnt handle running on a secondary bigger display as i takes the primary display size so make sure to have the screen
#       your running the program on, set as your main display (add some code to fix this in future)

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
SNAKE_SPEED = 6
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

    # boost berry variables
    boost_berry_size = SNAKE_BLOCK_SIZE * 2

    # reset walls and timers on game start
    wall_list = []
    wall_spawn_start_time = int(time.time())

    def display_speed(speed_value):
        value = speed_font.render("Speed: " + str(speed_value), True, WHITE)
        screen.blit(value, [0, 30])

    # Helper to generate a food position on grid not colliding with provided avoid list
    def generate_food_position():
        fx = random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        fy = random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        return round(fx), round(fy)

    def place_food(avoid_positions, max_attempts=200):
        for _ in range(max_attempts):
            nx, ny = generate_food_position()
            if [nx, ny] in avoid_positions:
                continue
            return nx, ny
        return None, None

    # Initialize snake + game state
    x1 = (SCREEN_WIDTH // 2)
    y1 = (SCREEN_HEIGHT // 2)
    x1_change = SNAKE_BLOCK_SIZE
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Start with two foods (behaviour matches original: first length+3, second length+2)
    foods = []
    fx, fy = place_food([])
    if fx is None:
        fx, fy = 0, 0
    foods.append({"x": fx, "y": fy, "big": False, "length_inc": 3})
    fx, fy = place_food([[foods[0]["x"], foods[0]["y"]]])
    if fx is None:
        fx, fy = 0, 0
    foods.append({"x": fx, "y": fy, "big": False, "length_inc": 2})

    clock = pygame.time.Clock()

    game_over = False
    game_close = False

    while not game_over:
        # Game-close (lost) loop
        while game_close:
            screen.fill(BLACK)
            message(f"You Lost! Score: {food_eaten} — Press Q to Quit or E to Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_e:
                        # Clean reset of local state (no recursion)
                        food_eaten = 0
                        wall_list = []
                        wall_spawn_start_time = int(time.time())
                        # reposition foods and snake
                        snake_list = []
                        length_of_snake = 1
                        x1 = (SCREEN_WIDTH // 2)
                        y1 = (SCREEN_HEIGHT // 2)
                        x1_change = SNAKE_BLOCK_SIZE
                        y1_change = 0
                        # place initial foods again (try to avoid collisions)
                        foods = []
                        fx, fy = place_food([])
                        if fx is None:
                            fx, fy = 0, 0
                        foods.append({"x": fx, "y": fy, "big": False, "length_inc": 3})
                        fx, fy = place_food([[foods[0]["x"], foods[0]["y"]]])
                        if fx is None:
                            fx, fy = 0, 0
                        foods.append({"x": fx, "y": fy, "big": False, "length_inc": 2})
                        game_close = False
                        break

        # Event handling (normal play)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Kill switch: quit immediately with 'q'
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                # Movement controls (no immediate reversal handling here; keep as before)
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

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Wrap-around (wall passthrough)
        if x1 < 0:
            x1 = SCREEN_WIDTH + x1
        if x1 >= SCREEN_WIDTH:
            x1 = SCREEN_WIDTH - x1
        if y1 < 0:
            y1 = SCREEN_HEIGHT + y1
        if y1 >= SCREEN_HEIGHT:
            y1 = SCREEN_HEIGHT - y1

        screen.fill(BLACK)

        # Draw foods (dynamic list)
        for f in foods:
            size = boost_berry_size if f.get("big", False) else SNAKE_BLOCK_SIZE
            pygame.draw.rect(screen, RED, [f["x"], f["y"], size, size])

        # Draw walls
        for wall in wall_list:
            pygame.draw.rect(screen, WHITE, [wall[0], wall[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # Snake head and self-collision check
        snake_head = [x1, y1]
        for segment in snake_list:
            if snake_head == segment:
                game_close = True
                break

        # Update snake list
        if not game_over:
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

        # Speed modifier (milder growth)
        speed_modifier = SNAKE_SPEED + food_eaten * 1

        # Draw snake and HUD
        our_snake(SNAKE_BLOCK_SIZE, snake_list)
        display_score(food_eaten)
        display_speed(speed_modifier)

        pygame.display.update()

        # --- Food collisions: check every food and respawn only that one ---
        for f in foods:
            if f.get("big", False):
                # big berry: rectangle collision (since it's double size)
                if (f["x"] <= x1 < f["x"] + boost_berry_size) and (f["y"] <= y1 < f["y"] + boost_berry_size):
                    length_of_snake += f.get("length_inc", 2)
                    food_eaten += 4
                    f["big"] = False
                    # respawn this food (avoid snake, other foods, walls)
                    attempts = 0
                    while attempts < 200:
                        attempts += 1
                        nx, ny = generate_food_position()
                        if [nx, ny] in snake_list:
                            continue
                        if any([nx, ny] == [o["x"], o["y"]] for o in foods):
                            continue
                        if [nx, ny] in wall_list:
                            continue
                        f["x"], f["y"] = nx, ny
                        break
            else:
                # small berry: exact grid match
                if x1 == f["x"] and y1 == f["y"]:
                    length_of_snake += f.get("length_inc", 2)
                    food_eaten += 2
                    # Toggle so next spawn of this food is a boost
                    f["big"] = True
                    attempts = 0
                    while attempts < 200:
                        attempts += 1
                        nx, ny = generate_food_position()
                        if [nx, ny] in snake_list:
                            continue
                        if any([nx, ny] == [o["x"], o["y"]] for o in foods):
                            continue
                        if [nx, ny] in wall_list:
                            continue
                        f["x"], f["y"] = nx, ny
                        break

        # --- Wall spawning logic: spawn wall(s) and APPEND a new food (permanent) ---
        MAX_FOODS = 5
        
        current_time = int(time.time())
        if current_time - wall_spawn_start_time >= wall_spawn_interval:
            new_wall_blocks = spawn_wall(length=random.randint(5, 10), snake_list=snake_list, foods=foods)
            if new_wall_blocks:
                wall_list.extend(new_wall_blocks)

                # Only add a new food if we are under the MAX_FOODS limit
                if len(foods) < MAX_FOODS:
                    for _ in range(200):
                        nx, ny = generate_food_position()
                        if [nx, ny] in snake_list:
                            continue
                        if any([nx, ny] == [o["x"], o["y"]] for o in foods):
                            continue
                        if [nx, ny] in wall_list:
                            continue
                        new_big = random.choice([True, False])
                        foods.append({"x": nx, "y": ny, "big": new_big, "length_inc": 2})
                        break
            wall_spawn_start_time = current_time

        # --- Collision with walls ---
        for wall in wall_list:
            if snake_head == wall:
                game_close = True
                break

        clock.tick(speed_modifier)

    pygame.quit()
    quit()

def spawn_wall(length, snake_list, foods, max_attempts=200):
    """Return a list of `length` wall blocks [[x,y], ...] that do not collide with the snake or foods.
    Falls back to a single block if no multi-block placement is found."""
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        orientation = random.choice([0, 1])  # 0 = horizontal, 1 = vertical
        start_x = random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        start_y = random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        wall_blocks = []
        valid = True
        for i in range(length):
            if orientation == 0:
                wx = start_x + i * SNAKE_BLOCK_SIZE
                wy = start_y
            else:
                wx = start_x
                wy = start_y + i * SNAKE_BLOCK_SIZE
            # out of bounds
            if wx < 0 or wy < 0 or wx >= SCREEN_WIDTH or wy >= SCREEN_HEIGHT:
                valid = False
                break
            # collision with snake
            if [wx, wy] in snake_list:
                valid = False
                break
            # collision with any food
            if any([wx, wy] == [f["x"], f["y"]] for f in foods):
                valid = False
                break
            wall_blocks.append([wx, wy])
        if valid and len(wall_blocks) == length:
            return wall_blocks

    # fallback: try to place a single block
    fallback_attempts = 0
    while fallback_attempts < max_attempts:
        fallback_attempts += 1
        wx = random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        wy = random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE + 1, SNAKE_BLOCK_SIZE)
        if [wx, wy] in snake_list:
            continue
        if any([wx, wy] == [f["x"], f["y"]] for f in foods):
            continue
        return [[wx, wy]]

    return []  # give up if nothing found

game_loop(food_eaten, SNAKE_SPEED)
