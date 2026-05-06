import os
import warnings

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pygame
import sys

pygame.init()


WIDTH = 1400
HEIGHT = 830

legend_surface = pygame.Surface((250,300), pygame.SRCALPHA)
legend_surface.fill((20,20,30,200))


bottom_surface = pygame.Surface((WIDTH - 300, 80), pygame.SRCALPHA)
bottom_surface.fill((20,20,30,200))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("skoulal - 1337")

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    bg_image = pygame.image.load("../assests/fly-in_bg.jpg") 
    
    # (Scaling) to prevent the small background
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except Exception:
    print(f"Error !")
    sys.exit()

# 4. L-Game Loop (L-Qalb N-Nabid d Pygame)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False

    screen.blit(bg_image, (0, 0))

    # blitting the surfaces
    screen.blit(legend_surface, (20, 20))
    screen.blit(bottom_surface, (0, HEIGHT - 100))
    
    pygame.draw.rect(screen, (100, 150, 255), pygame.Rect(20, 20, 250, 300), width=2, border_radius=10)
    pygame.draw.rect(screen, (150, 150, 5), pygame.Rect(0, HEIGHT - 100, WIDTH - 300, 80), width=2, border_radius=30)
    
    pygame.display.flip()

pygame.quit()
sys.exit()