import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame  # noqa: E402


class Camera:
    """Handles camera movement and zooming for the 2D renderer."""

    def __init__(self):
        """Initializes the camera with default offset and zoom."""
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.is_dragging = False
        self.last_mouse_pos = (0, 0)

    def apply(self, pos):
        """Converts world coordinates to screen coordinates."""
        screen_x = (pos[0] + self.offset_x) * self.zoom
        screen_y = (pos[1] + self.offset_y) * self.zoom
        return (int(screen_x), int(screen_y))

    def handle_event(self, event):
        """Handles mouse events for panning and zooming."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                self.offset_x += dx / self.zoom
                self.offset_y += dy / self.zoom
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEWHEEL:
            self.zoom += event.y * 0.1
            self.zoom = max(0.2, min(self.zoom, 3.0))


class Renderer2D:
    """Renders the drone simulation using pygame."""

    def __init__(self, map_data, engine_history):
        """Initializes the 2D renderer with map data and simulation history."""
        self.map_data = map_data
        self.history = engine_history

        self.current_turn = 0
        self.max_turns = len(engine_history)
        self.is_paused = True

        self.camera = Camera()

        pygame.init()
        self.WIDTH, self.HEIGHT = 1400, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("SKOULAL | Fly-In Simulator")

        self._load_assets()
        self._calculate_coord_mapping()

        self._build_timeline()

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
            "gold": (239, 191, 4),
            "magenta": (255, 0, 255),
            "cyan": (0, 255, 255),
            "default": (150, 100, 250),
        }

    def _load_assets(self):
        """Loads fonts, images, and visual assets required for rendering."""
        try:
            self.main_font = pygame.font.Font("assets/GODOFWAR.TTF", 28)
            self.small_font = pygame.font.Font("assets/GODOFWAR.TTF", 18)
        except Exception as e:
            print(f"Warning: Custom font not found. Using default. Error: {e}")
            self.main_font = pygame.font.SysFont(None, 28)
            self.small_font = pygame.font.SysFont(None, 24)

        self.legend_surface = pygame.Surface((250, 400), pygame.SRCALPHA)
        self.legend_surface.fill((20, 20, 30, 150))

        self.bottom_surface = pygame.Surface(
            (self.WIDTH - 100, 80), pygame.SRCALPHA
        )
        self.bottom_surface.fill((20, 20, 30, 150))

        try:
            self.bg_image = pygame.image.load("assets/fly-in_bg.jpg")
            self.drone_image = pygame.image.load("assets/drone.png")
            self.bg_image = pygame.transform.scale(
                self.bg_image, (self.WIDTH, self.HEIGHT)
            )
        except Exception:
            print("Error loading background, using default color.")
            self.bg_image = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg_image.fill((30, 35, 45))

    def _calculate_coord_mapping(self):
        """Calculates scaling and offset to map world coordinates to screen pixels."""
        xs = [zone.x for zone in self.map_data.zones.values()]
        ys = [zone.y for zone in self.map_data.zones.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        grid_width = max_x - min_x
        grid_height = max_y - min_y

        avail_width = self.WIDTH - 350
        avail_height = self.HEIGHT - 200
        scale_x = (
            avail_width / grid_width if grid_width > 0 else avail_width
        )
        scale_y = (
            avail_height / grid_height if grid_height > 0 else avail_height
        )
        scale = min(scale_x, scale_y)

        offset_x = 300 + (avail_width - (grid_width * scale)) / 2
        offset_y = 50 + (avail_height - (grid_height * scale)) / 2

        self.pixel_coords = {}
        for name, zone in self.map_data.zones.items():
            px = (zone.x - min_x) * scale + offset_x
            py = (zone.y - min_y) * scale + offset_y
            self.pixel_coords[name] = (int(px), int(py))

    def _build_timeline(self):
        """Translates simulation history into states for all
        drones per turn."""
        self.timeline = []

        current_state = {}
        for i in range(1, self.map_data.nb_drones + 1):
            current_state[str(i)] = self.map_data.start_hub.name
        self.timeline.append(current_state.copy())

        for turn_moves in self.history:
            new_state = current_state.copy()
            for move in turn_moves:
                parts = move.split("-")
                drone_id = parts[0][1:]
                dest_zone = parts[1]
                new_state[drone_id] = dest_zone
            self.timeline.append(new_state)
            current_state = new_state

    def _draw_map(self):
        """Draws the map connections and hubs on the screen."""
        for conn in self.map_data.connections:
            pos1 = self.camera.apply(self.pixel_coords[conn.zone1.name])
            pos2 = self.camera.apply(self.pixel_coords[conn.zone2.name])
            line_thickness = max(1, int(4 * self.camera.zoom))
            pygame.draw.line(
                self.screen, (100, 200, 155), pos1, pos2, line_thickness
            )

        for name, base_pos in self.pixel_coords.items():
            cam_pos = self.camera.apply(base_pos)
            radius = max(5, int(12 * self.camera.zoom))
            zone = self.map_data.zones[name]

            z_color_str = str(getattr(zone, "color", "default")).lower()
            hub_color = self.COLORS.get(z_color_str, self.COLORS["default"])

            is_start = name == self.map_data.start_hub.name
            z_type = str(getattr(zone, "zone_type", "")).lower()

            pygame.draw.circle(self.screen, hub_color, cam_pos, radius)

            border_color = (255, 255, 255)
            border_thick = max(1, int(2 * self.camera.zoom))

            if is_start:
                border_color = self.COLORS["green"]
                border_thick = max(2, int(4 * self.camera.zoom))

            pygame.draw.circle(
                self.screen, border_color, cam_pos, radius, border_thick
            )

            if "blocked" in z_type:
                pygame.draw.line(
                    self.screen,
                    (255, 50, 50),
                    (cam_pos[0] - radius * 0.7, cam_pos[1] + radius * 0.7),
                    (cam_pos[0] + radius * 0.7, cam_pos[1] - radius * 0.7),
                    max(2, int(4 * self.camera.zoom)),
                )
                pygame.draw.circle(
                    self.screen,
                    (255, 50, 50),
                    cam_pos,
                    radius,
                    max(1, int(2 * self.camera.zoom)),
                )  # Red inner ring

            elif "restricted" in z_type:
                inner_r = max(2, int(radius * 0.4))
                pygame.draw.circle(
                    self.screen,
                    (255, 50, 50),
                    cam_pos,
                    inner_r,
                    max(2, int(3 * self.camera.zoom)),
                )

            elif "priority" in z_type:
                inner_r = max(2, int(radius * 0.4))
                pygame.draw.circle(
                    self.screen, self.COLORS["yellow"], cam_pos, inner_r
                )

        for name, base_pos in self.pixel_coords.items():
            cam_pos = self.camera.apply(base_pos)
            radius = max(5, int(12 * self.camera.zoom))

            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                cam_pos,
                radius,
                max(1, int(2 * self.camera.zoom)),
            )

    def _draw_drones(self):
        """Draws the drones at their interpolated positions between turns."""
        t = self.anim_progress

        start_state = self.timeline[self.current_turn]
        next_turn = min(self.current_turn + 1, self.max_turns)
        end_state = self.timeline[next_turn]

        for d_id in start_state:
            start_zone = start_state[d_id]
            end_zone = end_state[d_id]

            start_px = self.pixel_coords[start_zone]
            end_px = self.pixel_coords[end_zone]

            # THE LERP MATH
            # Current = Start + (End - Start) * t
            cur_x = start_px[0] + (end_px[0] - start_px[0]) * t
            cur_y = start_px[1] + (end_px[1] - start_px[1]) * t

            cam_pos = self.camera.apply((cur_x, cur_y))

            if hasattr(self, "drone_image"):
                size = max(10, int(20 * self.camera.zoom))
                scaled_drone = pygame.transform.scale(
                    self.drone_image, (size, size)
                )
                drone_rect = scaled_drone.get_rect(center=cam_pos)
                self.screen.blit(scaled_drone, drone_rect)
            else:
                pygame.draw.circle(
                    self.screen,
                    (255, 200, 0),
                    cam_pos,
                    max(5, int(10 * self.camera.zoom)),
                )

    def _draw_ui(self):
        """Draws the user interface elements, including the
        legend and turn info."""
        self.screen.blit(self.legend_surface, (20, 20))
        self.screen.blit(self.bottom_surface, (50, self.HEIGHT - 100))

        pygame.draw.rect(
            self.screen,
            (52, 173, 97),
            pygame.Rect(20, 20, 250, 400),
            width=2,
            border_radius=10,
        )
        pygame.draw.rect(
            self.screen,
            (52, 173, 97),
            pygame.Rect(50, self.HEIGHT - 100, self.WIDTH - 100, 80),
            width=2,
            border_radius=20,
        )
        map_name = sys.argv[1].split("/")[-1]
        map_name = map_name.replace(".txt", "")

        title_text = self.main_font.render(
            f"Map: {map_name}", True, (255, 255, 255)
        )
        turn_text = self.small_font.render(
            f"Turn: {self.current_turn} / {self.max_turns}",
            True,
            (61, 184, 127),
        )

        self.screen.blit(title_text, (60, self.HEIGHT - 85))
        self.screen.blit(turn_text, (570, self.HEIGHT - 75))

        controls = " SPACE : Pause | ->: Next |  <- : Prev | Scroll: Zoom"
        controls_surf = self.small_font.render(controls, True, (200, 200, 200))
        self.screen.blit(controls_surf, (700, self.HEIGHT - 75))
        leg_x = 35  # X Offset inside the legend panel
        leg_y = 40  # Y Offset

        title_surf = self.main_font.render("Legend", True, (61, 184, 127))
        my_login = self.small_font.render(
            "made by skoulal", True, (61, 184, 127)
        )
        self.screen.blit(title_surf, (leg_x, leg_y))
        self.screen.blit(my_login, (100, 375))

        legend_items = [
            ("Start Hub", self.COLORS["green"], "circle"),
            ("Hub (Map color)", self.COLORS["default"], "circle"),
            ("Connection Line", (100, 150, 255), "line"),
            ("Priority zone", self.COLORS["yellow"], "priority"),
            ("Blocked zone", (255, 50, 50), "blocked"),
            ("Restricted zone", (255, 50, 50), "restricted"),
        ]

        y_offset = leg_y + 40
        for text, color, icon_type in legend_items:
            icon_center = (leg_x + 15, y_offset + 10)

            if icon_type == "circle":
                pygame.draw.circle(self.screen, color, icon_center, 10)
            elif icon_type == "line":
                pygame.draw.line(
                    self.screen,
                    color,
                    (leg_x, y_offset + 10),
                    (leg_x + 30, y_offset + 10),
                    4,
                )
            elif icon_type in ["priority", "blocked", "restricted"]:
                # Draw type icons with black background similar to the map
                pygame.draw.circle(
                    self.screen, self.COLORS["black"], icon_center, 10
                )
                pygame.draw.circle(
                    self.screen, (255, 255, 255), icon_center, 10, 1
                )  # White border
                if icon_type == "blocked":
                    pygame.draw.line(
                        self.screen,
                        color,
                        (icon_center[0] - 7, icon_center[1] + 7),
                        (icon_center[0] + 7, icon_center[1] - 7),
                        2,
                    )
                    pygame.draw.circle(self.screen, color, icon_center, 10, 1)
                elif icon_type == "restricted":
                    pygame.draw.circle(self.screen, color, icon_center, 4, 2)
                elif icon_type == "priority":
                    pygame.draw.circle(self.screen, color, icon_center, 4)

            # 2. Draw Text
            text_surf = self.small_font.render(text, True, (220, 220, 220))
            self.screen.blit(text_surf, (leg_x + 40, y_offset))

            y_offset += 35

    def run(self):
        """Main rendering loop that handles events, animation
        updates, and drawing."""
        clock = pygame.time.Clock()
        running = True
        self.anim_progress = 0.0
        self.anim_speed = 0.02
        self.is_paused = True
        self.hub_pause_frames = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    running = False
                self.camera.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused
                    if self.is_paused:
                        if event.key == pygame.K_RIGHT:
                            if self.current_turn < self.max_turns:
                                self.current_turn += 1
                                self.anim_progress = 0.0
                                self.hub_pause_frames = 0
                        elif event.key == pygame.K_LEFT:
                            if self.current_turn > 0:
                                self.current_turn -= 1
                                self.anim_progress = 0.01
                                self.hub_pause_frames = 0

            if not self.is_paused and self.current_turn < self.max_turns:
                if self.hub_pause_frames > 0:
                    self.hub_pause_frames -= 1
                    if self.hub_pause_frames <= 0:
                        self.anim_progress = 0.0
                        self.current_turn += 1
                        if self.current_turn >= self.max_turns:
                            self.is_paused = True
                else:
                    self.anim_progress += self.anim_speed
                    if self.anim_progress >= 1.0:
                        self.anim_progress = 1.0
                        self.hub_pause_frames = 60

            self.screen.blit(self.bg_image, (0, 0))
            self._draw_map()
            self._draw_drones()
            self._draw_ui()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
