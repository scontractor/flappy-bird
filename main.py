import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load images
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

background = pygame.image.load(os.path.join(image_path, 'background.jpg')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bird_img = pygame.image.load(os.path.join(image_path, 'bird.png')).convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))

pipe_img = pygame.image.load(os.path.join(image_path, 'pipe.png')).convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (70, 500))

# Bird properties
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe properties
pipe_width = 70
pipe_gap = 200
pipe_velocity = 3
pipes = []

# Game variables
score = 0
font = pygame.font.Font(None, 36)

def create_pipe():
    gap_y = random.randint(100, HEIGHT - 100 - pipe_gap)
    top_pipe = pipe_img
    bottom_pipe = pygame.transform.flip(pipe_img, False, True)
    return {
        "x": WIDTH,
        "top": {"y": gap_y - pipe_gap // 2 - pipe_img.get_height(), "image": top_pipe},
        "bottom": {"y": gap_y + pipe_gap // 2, "image": bottom_pipe}
    }

def draw_pipes():
    for pipe in pipes:
        screen.blit(pipe["top"]["image"], (pipe["x"], pipe["top"]["y"]))
        screen.blit(pipe["bottom"]["image"], (pipe["x"], pipe["bottom"]["y"]))

def check_collision(bird_rect):
    for pipe in pipes:
        top_rect = pygame.Rect(pipe["x"], pipe["top"]["y"], pipe_width, pipe_img.get_height())
        bottom_rect = pygame.Rect(pipe["x"], pipe["bottom"]["y"], pipe_width, pipe_img.get_height())
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    if bird_rect.top < 0 or bird_rect.bottom > HEIGHT:
        return True
    return False

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def game_over_screen():
    screen.blit(background, (0, 0))
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

    draw_button("Try Again", 50, 400, 140, 50, GREEN, WHITE)
    draw_button("Quit Game", 210, 400, 140, 50, RED, WHITE)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 50 <= mouse_pos[0] <= 190 and 400 <= mouse_pos[1] <= 450:
                    return True
                elif 210 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 450:
                    return False
    return False

def reset_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # Update bird position
    bird_velocity += gravity
    bird_y += bird_velocity

    # Create and move pipes
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
        pipes.append(create_pipe())

    for pipe in pipes:
        pipe["x"] -= pipe_velocity

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe["x"] + pipe_width > 0]

    # Check for collisions
    bird_rect = bird_img.get_rect(center=(bird_x, bird_y))
    if check_collision(bird_rect):
        if game_over_screen():
            reset_game()
        else:
            running = False
        continue

    # Update score
    score += 1

    # Draw everything
    screen.blit(background, (0, 0))
    draw_pipes()
    screen.blit(bird_img, bird_rect)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()