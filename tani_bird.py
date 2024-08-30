import pygame
import pygame.freetype
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tani Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load images
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

background = pygame.image.load(os.path.join(image_path, 'background.jpg')).convert()
bird_img = pygame.image.load(os.path.join(image_path, 'tani.png')).convert_alpha()
pipe_img = pygame.image.load(os.path.join(image_path, 'pipe.png')).convert_alpha()

# Load fonts
font = pygame.font.Font(None, 36)
try:
    fancy_font = pygame.freetype.Font(os.path.join(current_path, "fancy_font.ttf"), 72)
except:
    fancy_font = pygame.freetype.SysFont("Arial", 72)

# Game variables
score = 0
fullscreen = False


def scale_objects():
    global background, bird_img, pipe_img, bird_x, bird_y, pipe_width, pipe_gap

    # Scale background
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Scale bird (maintain aspect ratio)
    bird_scale = min(WIDTH, HEIGHT) / 15
    bird_img = pygame.transform.scale(bird_img, (int(bird_scale * 1.33), int(bird_scale)))

    # Scale pipe
    pipe_width = int(WIDTH / 5.7)
    pipe_img = pygame.transform.scale(pipe_img, (pipe_width, HEIGHT))

    # Adjust game elements
    bird_x = WIDTH // 8
    bird_y = HEIGHT // 2
    pipe_gap = HEIGHT // 3


def create_pipe():
    gap_y = random.randint(pipe_gap, HEIGHT - pipe_gap)
    top_pipe = pipe_img
    bottom_pipe = pygame.transform.flip(pipe_img, False, True)
    return {
        "x": WIDTH,
        "top": {"y": gap_y - pipe_gap - pipe_img.get_height(), "image": top_pipe},
        "bottom": {"y": gap_y, "image": bottom_pipe}
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

    # Draw "Tani Bird" in large, attractive text
    text_surface, _ = fancy_font.render("Tani Bird", WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(text_surface, text_rect)

    # Add a decorative underline
    pygame.draw.line(screen, WHITE,
                     (text_rect.left, text_rect.bottom + 5),
                     (text_rect.right, text_rect.bottom + 5), 3)

    # Game Over text
    game_over_text = font.render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(game_over_text, game_over_rect)

    # Score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(score_text, score_rect)

    # Buttons
    button_width, button_height = 140, 50
    draw_button("Try Again", WIDTH // 4 - button_width // 2, HEIGHT * 3 // 4, button_width, button_height, GREEN, WHITE)
    draw_button("Quit Game", WIDTH * 3 // 4 - button_width // 2, HEIGHT * 3 // 4, button_width, button_height, RED,
                WHITE)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 4 - button_width // 2 <= mouse_pos[
                    0] <= WIDTH // 4 + button_width // 2 and HEIGHT * 3 // 4 <= mouse_pos[
                    1] <= HEIGHT * 3 // 4 + button_height:
                    return True
                elif WIDTH * 3 // 4 - button_width // 2 <= mouse_pos[
                    0] <= WIDTH * 3 // 4 + button_width // 2 and HEIGHT * 3 // 4 <= mouse_pos[
                    1] <= HEIGHT * 3 // 4 + button_height:
                    return False
    return False


def reset_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0


# Initial scaling
scale_objects()

# Game properties
bird_velocity = 0
gravity = HEIGHT / 1200
jump_strength = -HEIGHT / 60
pipe_velocity = WIDTH / 133
pipes = []

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
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                WIDTH, HEIGHT = screen.get_size()
                scale_objects()
                reset_game()
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                scale_objects()
                reset_game()

    # Update bird position
    bird_velocity += gravity
    bird_y += bird_velocity

    # Create and move pipes
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - WIDTH // 2:
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