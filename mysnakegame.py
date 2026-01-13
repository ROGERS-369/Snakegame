import pygame
import random

pygame.init()
pygame.mixer.init()

CELL_SIZE = 20
BACKGROUND_COLOR = (58, 158, 30)
FOOD_COLOR = (255, 0, 0)
SNAKE_COLOR = (255, 255, 0)
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1450
GAMEOVER_COLOR = (255, 0, 0)
BOUNDARY_COLOR = (0, 0, 0)

# Game Field Boundary
boundary_rect = pygame.Rect(
    CELL_SIZE,
    150 + CELL_SIZE,
    SCREEN_WIDTH - 2 * CELL_SIZE,
    SCREEN_HEIGHT - 650 - CELL_SIZE
)

# Selecting random direction
directions = {1: 'RIGHT', 2: 'LEFT', 3: 'UP', 4: 'DOWN'}
direction = random.choice(list(directions.values()))

# Screen definition
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

SNAKE_BODY = [(200, 340), (220, 340), (240, 340)]
SNAKE_FOOD = pygame.Rect(420, 460, CELL_SIZE, CELL_SIZE)

# Define button areas
button_width = 240
button_height = 100
button_margin = 50
up_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 3 * button_height - 3 * button_margin, button_width, button_height)
down_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - button_height - button_margin, button_width, button_height)
left_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width - button_margin, SCREEN_HEIGHT - 2 * button_height - 2 * button_margin, button_width, button_height)
right_button = pygame.Rect(SCREEN_WIDTH // 2 + button_margin, SCREEN_HEIGHT - 2 * button_height - 2 * button_margin, button_width, button_height)

# Load sounds
hiss_sound = pygame.mixer.Sound('Hiss sound effect.mp3')
game_over_sound = pygame.mixer.Sound('Game-Over-Sound-Effect.mp3')

running = True
game_over = False
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if up_button.collidepoint(event.pos) and direction != 'DOWN':
                direction = 'UP'
            elif down_button.collidepoint(event.pos) and direction != 'UP':
                direction = 'DOWN'
            elif left_button.collidepoint(event.pos) and direction != 'RIGHT':
                direction = 'LEFT'
            elif right_button.collidepoint(event.pos) and direction != 'LEFT':
                direction = 'RIGHT'

    # Moving Snake
    head = SNAKE_BODY[-1]
    if direction == 'RIGHT':
        new_head = (head[0] + CELL_SIZE, head[1])
    elif direction == 'LEFT':
        new_head = (head[0] - CELL_SIZE, head[1])
    elif direction == 'UP':
        new_head = (head[0], head[1] - CELL_SIZE)
    elif direction == 'DOWN':
        new_head = (head[0], head[1] + CELL_SIZE)

    if not game_over:
        SNAKE_BODY.append(new_head)

        # Snake and Food collision
        if SNAKE_FOOD.colliderect(pygame.Rect(new_head[0], new_head[1], CELL_SIZE, CELL_SIZE)):
            hiss_sound.play()
            score += 1
            SNAKE_FOOD = pygame.Rect(random.randint(boundary_rect.left, boundary_rect.right - CELL_SIZE) // CELL_SIZE * CELL_SIZE, random.randint(boundary_rect.top, boundary_rect.bottom - CELL_SIZE) // CELL_SIZE * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Check if food is on top of snake
            while any(SNAKE_FOOD.colliderect(pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)) for segment in SNAKE_BODY):
                SNAKE_FOOD = pygame.Rect(random.randint(boundary_rect.left, boundary_rect.right - CELL_SIZE) // CELL_SIZE * CELL_SIZE, random.randint(boundary_rect.top, boundary_rect.bottom - CELL_SIZE) // CELL_SIZE * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        else:
            SNAKE_BODY.pop(0)

        # Snake to Body & Snake to Boundary collision
        if (new_head[0] < boundary_rect.left or new_head[0] >= boundary_rect.right or new_head[1] < boundary_rect.top or new_head[1] >= boundary_rect.bottom) or new_head in SNAKE_BODY[:-1]:
            game_over_sound.play()
            game_over = True

    screen.fill(BACKGROUND_COLOR)

    if game_over:
        gameover_font = pygame.font.Font(None, 72)
        gameover_text = gameover_font.render("GAME OVER, YOU LOST!!", True, GAMEOVER_COLOR)
        screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - gameover_text.get_height() // 2))
    else:
        for segment in SNAKE_BODY:
            pygame.draw.circle(screen, SNAKE_COLOR, (segment[0] + CELL_SIZE // 2, segment[1] + CELL_SIZE // 2), CELL_SIZE // 2)
        pygame.draw.circle(screen, FOOD_COLOR, (SNAKE_FOOD.x + CELL_SIZE // 2, SNAKE_FOOD.y + CELL_SIZE // 2), CELL_SIZE // 2)

        # Draw boundary
        pygame.draw.rect(screen, BOUNDARY_COLOR, boundary_rect, 10)

        # Draw buttons
        pygame.draw.rect(screen, (255, 255, 255), up_button)
        pygame.draw.rect(screen, (255, 255, 255), down_button)
        pygame.draw.rect(screen, (255, 255, 255), left_button)
        pygame.draw.rect(screen, (255, 255, 255), right_button)

        # Defining font
        font = pygame.font.Font(None, 56)
        # Rendering Button labels
        text_up = font.render('UP', True, (0, 0, 0))
        text_down = font.render('DOWN', True, (0, 0, 0))
        text_left = font.render('LEFT', True, (0, 0, 0))
        text_right = font.render('RIGHT', True, (0, 0, 0))
        text_score = font.render(f'SCORE: {score}', True, (0, 0, 0))

        # Drawing Buttons onto the screen
        screen.blit(text_up, (up_button.centerx - text_up.get_width() // 2, up_button.centery - text_up.get_height() // 2))
        screen.blit(text_down, (down_button.centerx - text_down.get_width() // 2, down_button.centery - text_down.get_height() // 2))
        screen.blit(text_left, (left_button.centerx - text_left.get_width() // 2, left_button.centery - text_left.get_height() // 2))
        screen.blit(text_right, (right_button.centerx - text_right.get_width() // 2, right_button.centery - text_right.get_height() // 2))
        screen.blit(text_score, (340, 60))

    pygame.display.flip()
    pygame.time.Clock().tick(10)

    if game_over:
        pygame.time.delay(2000)
        running = False