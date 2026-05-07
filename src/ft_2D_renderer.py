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
        self.COLORS = {
            "red": (255, 50, 50),
            "green": (50, 200, 50),
            "blue": (50, 150, 255),
            "yellow": (255, 215, 0),
            "purple": (150, 50, 200),
            "orange": (255, 150, 50),
            "gray": (150, 150, 150),
            "black": (40, 40, 40),
            "white": (240, 240, 240),
            "default": (150, 100, 250) 
        }
    # Fix 1: Indentation m-regla
    def _load_assets(self):
        try:
            # Kan-3tiwh L-Path dyal L-Fichier NICHAN
            self.main_font = pygame.font.Font("assets/GODOFWAR.TTF", 32)
            self.small_font = pygame.font.Font("assets/GODOFWAR.TTF", 18)
        except Exception as e:
            print(f"Warning: Custom font not found. Using default. Error: {e}")
            self.main_font = pygame.font.SysFont(None, 28)
            self.small_font = pygame.font.SysFont(None, 24)
        
        self.legend_surface = pygame.Surface((250, 400), pygame.SRCALPHA)
        self.legend_surface.fill((20, 20, 30, 150))
        
        self.bottom_surface = pygame.Surface((self.WIDTH - 100, 80), pygame.SRCALPHA)
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
            pos1 = self.camera.apply(self.pixel_coords[conn.zone1.name])
            pos2 = self.camera.apply(self.pixel_coords[conn.zone2.name])
            line_thickness = max(1, int(4 * self.camera.zoom))
            # Loun L-Connection (Zreq bhal t-tswira)
            pygame.draw.line(self.screen, (100, 150, 255), pos1, pos2, line_thickness)
            
        # 2. Rssem L-Hubs w L-Icons
        for name, base_pos in self.pixel_coords.items():
            cam_pos = self.camera.apply(base_pos)
            radius = max(5, int(20 * self.camera.zoom))
            zone = self.map_data.zones[name]
            
            # --- COLOR MAPPING ---
            # (Mola7ada: T2kked kifach m-ssmiha f parser dyalk. Ghaliban getattr(zone, 'color'))
            z_color_str = str(getattr(zone, 'color', 'default')).lower()
            hub_color = self.COLORS.get(z_color_str, self.COLORS["default"])
            
            # --- ZONE IDENTIFICATION ---
            is_start = (name == self.map_data.start_hub.name)
            is_goal = (name == self.map_data.end_hub.name)
            z_type = str(getattr(zone, 'zone_type', '')).lower()
            
            # 1. Base Circle
            pygame.draw.circle(self.screen, hub_color, cam_pos, radius)
            
            # 2. Outer Border (Ila kan Start/Goal, n-ghldouh w n-lownouh)
            border_color = (255, 255, 255) # Default white border
            border_thick = max(1, int(2 * self.camera.zoom))
            
            if is_start:
                border_color = self.COLORS["green"]
                border_thick = max(2, int(4 * self.camera.zoom))
            elif is_goal:
                border_color = self.COLORS["red"]
                border_thick = max(2, int(4 * self.camera.zoom))
                
            pygame.draw.circle(self.screen, border_color, cam_pos, radius, border_thick)

            # 3. DRAW ICONS (Geometry / Math)
            if "blocked" in z_type:
                # Icon Blocked: Kht 7mer dayz f L-wst (Slash /)
                pygame.draw.line(self.screen, (255, 50, 50), 
                                (cam_pos[0] - radius*0.7, cam_pos[1] + radius*0.7), 
                                (cam_pos[0] + radius*0.7, cam_pos[1] - radius*0.7), 
                                max(2, int(4 * self.camera.zoom)))
                pygame.draw.circle(self.screen, (255, 50, 50), cam_pos, radius, max(1, int(2 * self.camera.zoom))) # Red inner ring
                
            elif "restricted" in z_type:
                # Icon Restricted: Dwaera 7mra sghira l-dakhl
                inner_r = max(2, int(radius * 0.4))
                pygame.draw.circle(self.screen, (255, 50, 50), cam_pos, inner_r, max(2, int(3 * self.camera.zoom)))
                
            elif "priority" in z_type:
                # Icon Priority: Dwaera Sfra wla Nqta m-dweya
                inner_r = max(2, int(radius * 0.4))
                pygame.draw.circle(self.screen, self.COLORS["yellow"], cam_pos, inner_r)
            
        # 2. Rssem L-Hubs (Circles)
        for name, base_pos in self.pixel_coords.items():
                cam_pos = self.camera.apply(base_pos)
                radius = max(5, int(20 * self.camera.zoom)) # L-Circle kay-kber w y-sgher
                    
                pygame.draw.circle(self.screen, (255, 255, 255), cam_pos, radius, max(1, int(2 * self.camera.zoom)))

    def _draw_drones(self):
        # Dba khawya, hta n-bniw L-Animation
        pass

    def _draw_ui(self):
        self.screen.blit(self.legend_surface, (20, 20))
        self.screen.blit(self.bottom_surface, (50, self.HEIGHT - 100)) 
        
        pygame.draw.rect(self.screen, (100, 150, 255), pygame.Rect(20, 20, 250, 400), width=2, border_radius=10)
        pygame.draw.rect(self.screen, (150, 150, 5), pygame.Rect(50, self.HEIGHT - 100, self.WIDTH - 100, 80), width=2, border_radius=20)
        
        # 🌟 ZEDNA L-CONTROLS L-TE7T
        title_text = self.main_font.render(f"Map: {sys.argv[1].split('/')[-1]}", True, (255, 255, 255))
        turn_text = self.small_font.render(f"Turn: {self.current_turn} / {self.max_turns}", True, (100, 200, 255))
        
        # Ktebhoum f L-issr w L-wst
        self.screen.blit(title_text, (60, self.HEIGHT - 85))
        self.screen.blit(turn_text, (570, self.HEIGHT - 75))

        # Controls f L-imin
        controls = "<SPACE>: Pause | < -> >: Next |  < <- >: Prev | <Scroll>: Zoom"
        controls_surf = self.small_font.render(controls, True, (200, 200, 200))
        self.screen.blit(controls_surf, (700, self.HEIGHT - 75))
        leg_x = 35  # X Offset wst L-Panel
        leg_y = 40  # Y Offset
        
        # Smiya d L-Legend
        title_surf = self.main_font.render("Legend", True, (100, 200, 255))
        my_login = self.small_font.render("made by skoulal", True, (150, 100, 220))
        self.screen.blit(title_surf, (leg_x, leg_y))
        self.screen.blit(my_login, (100, 375))
        
        legend_items = [
            ("Start Hub", self.COLORS["green"], "circle"),
            ("Goal Hub", self.COLORS["red"], "circle"),
            ("Hub (Map color)", self.COLORS["default"], "circle"),
            ("Connection Line", (100, 150, 255), "line"),
            ("Priority zone", self.COLORS["yellow"], "priority"),
            ("Blocked zone", (255, 50, 50), "blocked"),
            ("Restricted zone", (255, 50, 50), "restricted")
        ]
        
        y_offset = leg_y + 40
        for text, color, icon_type in legend_items:
            icon_center = (leg_x + 15, y_offset + 10)
            
            if icon_type == "circle":
                pygame.draw.circle(self.screen, color, icon_center, 10)
            elif icon_type == "line":
                pygame.draw.line(self.screen, color, (leg_x, y_offset + 10), (leg_x + 30, y_offset + 10), 4)
            elif icon_type in ["priority", "blocked", "restricted"]:
                # N-rsmou L-Icon dyal L-Type bhal L-Map b-dabt (Black background with icon)
                pygame.draw.circle(self.screen, self.COLORS["black"], icon_center, 10)
                pygame.draw.circle(self.screen, (255,255,255), icon_center, 10, 1) # White border
                if icon_type == "blocked":
                    pygame.draw.line(self.screen, color, (icon_center[0]-7, icon_center[1]+7), (icon_center[0]+7, icon_center[1]-7), 2)
                    pygame.draw.circle(self.screen, color, icon_center, 10, 1)
                elif icon_type == "restricted":
                    pygame.draw.circle(self.screen, color, icon_center, 4, 2)
                elif icon_type == "priority":
                    pygame.draw.circle(self.screen, color, icon_center, 4)

            # 2. Rsem L-Kteba
            text_surf = self.small_font.render(text, True, (220, 220, 220))
            self.screen.blit(text_surf, (leg_x + 40, y_offset))
            
            y_offset += 35 # Hbet l-ster L-jay
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