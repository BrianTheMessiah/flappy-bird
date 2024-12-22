import pygame
import random
from constants import (
    WHITE, BLACK, GREEN, RED,
    BIRD_WIDTH, BIRD_HEIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GRAVITY, JUMP_HEIGHT,
    PIPES_WIDTH, PIPE_GAP, PIPE_VELOCITY,
    FPS
)

pygame.init()

bird_x = 100
bird_y = SCREEN_HEIGHT / 2
bird_velocity = 0
pipes = []
score = 0

pipe_image = pygame.image.load('assets/pipe.png')
pipe_image = pygame.transform.scale(pipe_image, (100, 600))
pipe_image_flipped = pygame.transform.flip(pipe_image, False, True)

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

def generate_pipes():
    pipe_height = random.randint(100, SCREEN_HEIGHT - 200 - 100)
    return {
        "top": pygame.Rect(SCREEN_WIDTH, pipe_height - 200 / 2, 100, 200 - 100),
        "bottom": pygame.Rect(SCREEN_WIDTH, pipe_height + 200 / 2 + 100, 100, SCREEN_HEIGHT - pipe_height - 200 / 2 - 100)
    }
    
def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_image_flipped, pipe["top"])
        screen.blit(pipe_image, pipe["bottom"])

def move_pipes(pipes):
    for pipe in pipes:
        pipe["top"].x -= 2
        pipe["bottom"].x -= 2
        
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT

running = True
pipes.append(generate_pipes())
pipe_spawn_timer = 0
start_button = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 25, 100, 50)
start = False

while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
            start = True
    screen.fill(WHITE)
    start_text = font.render("Click to start", True, BLACK)
    screen.blit(start_text, (start_button.x + 10, start_button.y + 10))
    pygame.draw.rect(screen, GREEN, start_button)
    pygame.display.flip()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10
    bird_velocity += 0.5
    bird_y += bird_velocity
    bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
    if check_collision(bird_rect, pipes):
        running = False
    if pipes[0]["top"].x + 100 < 0:
        pipes.pop(0)
        pipes.append(generate_pipes())
        score += 1
    draw_pipes(pipes)
    move_pipes(pipes)
    pygame.draw.rect(screen, GREEN, bird_rect)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)
    pipe_spawn_timer += 1
    if pipe_spawn_timer == 100:
        pipes.append(generate_pipes())
        pipe_spawn_timer = 0
