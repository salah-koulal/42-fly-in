import os
import warnings

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pygame
import sys


# --- 1. INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 1400, 830
pygame.display.set_caption("skoulal - 1337")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Setup Transparent Panels
legend_surface = pygame.Surface((250,350), pygame.SRCALPHA)
legend_surface.fill((20,20,30,150))

bottom_surface = pygame.Surface((WIDTH - 300, 80), pygame.SRCALPHA)
bottom_surface.fill((20,20,30,100))




# main_font = pygame.font.SysFont(None, 36)
# small_font = pygame.font.SysFont(None, 24)
# test_font = pygame.font.SysFont(['centurygothic', 'msgothic', 'arial'],24)
try:
    bg_image = pygame.image.load("../assets/fly-in_bg.jpg") 
    drone_image = pygame.image.load("../assets/dronegid")
    # (Scaling) & resizing to prevent the small background
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    drone_image = pygame.transform.scale(drone_image, (40,45))
except Exception:
    print(f"Error !")
    sys.exit()

# 4. L-Game Loop (L-Qalb N-Nabid d Pygame)
running = True

# --- VARIABLES FOR OUR TEST MAP ---
hub_1 = (300,400)
hub_2 = (600, 400)
drone_pos = (575,375)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            drone_pos = (285, 380)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            drone_pos = (585,380)


            

    screen.blit(bg_image, (0, 0))

    #TODO: DRAWING CONNECTION, ZONES
    # pygame.draw.line(surface, color, start_pos, end_pos, width)
    pygame.draw.line(screen, (255, 255, 255), hub_1, hub_2, 5)
    
    # pygame.draw.circle(surface, color, center, radius, width)
    pygame.draw.circle(screen, (50, 200, 100), hub_1, 30)
    pygame.draw.circle(screen, (200, 50, 50), hub_2, 30)
    
    pygame.draw.circle(screen, (255, 255, 255), hub_1, 30, 3) 
    pygame.draw.circle(screen, (255, 255, 255), hub_2, 30, 3)
    
    # Positioning the drone : test
    screen.blit(drone_image, (drone_pos))
    
    # title_text = main_font.render("Map: 01_linear_path", True, (255, 255, 255))
    # turn_text = main_font.render("Turn: 2 / 4", True, (100, 200, 255))
    
    # Blit the text surfaces onto the screen
    # screen.blit(title_text, (20, HEIGHT - 60))
    # screen.blit(turn_text, (WIDTH // 2 - 50, HEIGHT - 60))

    # blitting the UI-PANELS
    screen.blit(legend_surface, (20, 20))
    screen.blit(bottom_surface, (0, HEIGHT - 100))
    pygame.draw.rect(screen, (100, 150, 255), pygame.Rect(20, 20, 250, 350), width=2, border_radius=10)
    pygame.draw.rect(screen, (150, 150, 5), pygame.Rect(0, HEIGHT - 100, WIDTH - 300, 80), width=2, border_radius=30)
    
    
    
    # test_font.render("text", True, (100,150, 105))
    pygame.display.flip()

pygame.quit()
sys.exit()