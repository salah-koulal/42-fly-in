import sys
import pygame


class Renderer2D:
    def __init__(self, map_data, engine_history):
        self.map = map_data
        self.history = engine_history
        
        # State Variables
        self.current_turn = 0
        self.max_turns = len(engine_history)
        self.is_paused = True
        
        # setup pygame
        pygame.init()
        self.WIDTH, self.HEIGHT = 1400, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("SKOULAL | Fly-In Simulator")
        
        #  ASSESTS INIT
        self._load_assets()
    
    
        def _load_assests(self):
            # Setup Transparent Panels
            legend_surface = pygame.Surface((250,350), pygame.SRCALPHA)
            legend_surface.fill((20,20,30,150))

            bottom_surface = pygame.Surface((self.WIDTH - 300, 80), pygame.SRCALPHA)
            bottom_surface.fill((20,20,30,100))
            try:
                bg_image = pygame.image.load("../assets/fly-in_bg.jpg") 
                drone_image = pygame.image.load("../assets/dronegid")
                # (Scaling) & resizing to prevent the small background
                bg_image = pygame.transform.scale(bg_image, (self.WIDTH, self.HEIGHT))
                drone_image = pygame.transform.scale(drone_image, (40,45))
            except Exception:
                print(f"Error while loading assets! \
                    (Make sure to specify the correct assets path)")
                sys.exit()