import os
import warnings

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=RuntimeWarning)

import sys
import pygame


class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.is_dragging = False
        self.last_mouse_pos = (0, 0)

    def apply(self, pos):
        """Kat-7ewel L-Coordinate mn L-Kharita (World) l L-Checha (Screen)"""
        screen_x = (pos[0] + self.offset_x) * self.zoom
        screen_y = (pos[1] + self.offset_y) * self.zoom
        return (int(screen_x), int(screen_y))

    def handle_event(self, event):
        """Kat-qra L-Harakat d L-Mouse w kat-beddel Zoom w Offset"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Tleq L-Click
                self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging: # Ila knti wark w kat-7erek L-Mouse
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                # Kan-qsmou 3la zoom bach L-jerr y-bqa 1:1 wakha t-koun m-zomi
                self.offset_x += dx / self.zoom
                self.offset_y += dy / self.zoom
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEWHEEL: # Scroll d L-Mouse (Zoom)
            # Zoom In/Out b 10%
            self.zoom += event.y * 0.1
            # Mat-khellihch y-zomi bzaf wla y-sgher bzaf (Min 0.2, Max 3.0)
            self.zoom = max(0.2, min(self.zoom, 3.0))

class Renderer2D:
    def __init__(self, map_data, engine_history):
        self.map_data = map_data # Fix 3
        self.history = engine_history
        
        # State Variables
        self.current_turn = 0
        self.max_turns = len(engine_history)
        self.is_paused = True
        
        self.camera = Camera()
        
        # setup pygame
        pygame.init()
        self.WIDTH, self.HEIGHT = 1400, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("SKOULAL | Fly-In Simulator")
        
        # ASSETS & COORDS INIT
        self._load_assets()
        self._calculate_coord_mapping() # N-7sbou L-Math d L-Pixels merra we7da!

    # Fix 1: Indentation m-regla
    def _load_assets(self):
        # Fix 2: self. l-ay 7aja ghadi n-7tajouha mn be3d
        self.main_font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.legend_surface = pygame.Surface((250, 500), pygame.SRCALPHA)
        self.legend_surface.fill((20, 20, 30, 150))
        
        self.bottom_surface = pygame.Surface((self.WIDTH - 150, 80), pygame.SRCALPHA)
        self.bottom_surface.fill((20, 20, 30, 150))
        
        try:
            self.bg_image = pygame.image.load("assets/fly-in_bg.jpg") 
            # drone_image = pygame.image.load("../assets/dronegid") 
            self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))
            # self.drone_image = pygame.transform.scale(drone_image, (40,45))
        except Exception:
            print("Error loading background, using default color.")
            # Fallback 
            self.bg_image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg_image.fill((30, 35, 45)) 

    def _calculate_coord_mapping(self):
        xs = [zone.x for zone in self.map_data.zones.values()]
        ys = [zone.y for zone in self.map_data.zones.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        grid_width = max_x - min_x
        grid_height = max_y - min_y
        
        avail_width = self.WIDTH - 400  
        avail_height = self.HEIGHT - 300 
        scale_x = avail_width / grid_width if grid_width > 0 else avail_width
        scale_y = avail_height / grid_height if grid_height > 0 else avail_height
        scale = min(scale_x, scale_y)
        
        offset_x = (self.WIDTH - (grid_width * scale)) / 2
        offset_y = (self.HEIGHT - (grid_height * scale)) / 2
        
        self.pixel_coords = {}
        for name, zone in self.map_data.zones.items():
            px = (zone.x - min_x) * scale + offset_x
            py = (zone.y - min_y) * scale + offset_y
            self.pixel_coords[name] = (int(px), int(py))

    def _draw_map(self):
        # 1. Rssem T-triqat (Connections)
        for conn in self.map_data.connections:
            # 🌟 N-foutou L-Coordinates 3la L-Camera bach y-t-zomaw!
            pos1 = self.camera.apply(self.pixel_coords[conn.zone1.name])
            pos2 = self.camera.apply(self.pixel_coords[conn.zone2.name])
            line_thickness = max(1, int(4 * self.camera.zoom))
            pygame.draw.line(self.screen, (150, 150, 150), pos1, pos2, line_thickness)
            
        # 2. Rssem L-Hubs (Circles)
        for name, base_pos in self.pixel_coords.items():
                cam_pos = self.camera.apply(base_pos)
                radius = max(5, int(20 * self.camera.zoom)) # L-Circle kay-kber w y-sgher
                    
                pygame.draw.circle(self.screen, (50, 150, 255), cam_pos, radius)
                pygame.draw.circle(self.screen, (255, 255, 255), cam_pos, radius, max(1, int(2 * self.camera.zoom)))

    def _draw_drones(self):
        # Dba khawya, hta n-bniw L-Animation
        pass

    def _draw_ui(self):
            self.screen.blit(self.legend_surface, (20, 20))
            self.screen.blit(self.bottom_surface, (50, self.HEIGHT - 100)) 
            
            pygame.draw.rect(self.screen, (100, 150, 255), pygame.Rect(20, 20, 250, 500), width=2, border_radius=10)
            pygame.draw.rect(self.screen, (150, 150, 5), pygame.Rect(50, self.HEIGHT - 100, self.WIDTH - 150, 80), width=2, border_radius=20)
            
            # 🌟 ZEDNA L-CONTROLS L-TE7T
            title_text = self.main_font.render(f"Map: {sys.argv[1].split('/')[-1]}", True, (255, 255, 255))
            turn_text = self.main_font.render(f"Turn: {self.current_turn} / {self.max_turns}", True, (100, 200, 255))
            
            # Ktebhoum f L-issr w L-wst
            self.screen.blit(title_text, (70, self.HEIGHT - 75))
            self.screen.blit(turn_text, (450, self.HEIGHT - 75))

            # Controls f L-imin
            controls = "[SPACE]: Pause  |  [->]: Next  |  [<-]: Prev  |  [Scroll]: Zoom  |  [Drag]: Pan"
            controls_surf = self.small_font.render(controls, True, (200, 200, 200))
            self.screen.blit(controls_surf, (700, self.HEIGHT - 77))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # 1. Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    running = False
                self.camera.handle_event(event)
            # 2. Painter's Algorithm: L-BG -> L-Map -> D-Drones -> UI
            self.screen.blit(self.bg_image, (0, 0)) # Fix 2
            self._draw_ui()
            self._draw_map()
            self._draw_drones()
            
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()