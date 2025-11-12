"""
Settings menu for game configuration
"""

import pygame
from .base_menu import Menu
from ..core import config

class SettingsMenu(Menu):
    """Simplified settings menu screen"""

    def __init__(self, screen):
        super().__init__(screen)
        self.selected_setting = 0
        self.settings = [
            ("FPS", "screen.fps", [5, 10, 15, 20, 30, 60], "value"),
            ("Snake Color", "colors.snake", [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 100, 255), (100, 255, 255)], "color"),
        
        ]
        self.current_values = []
        self.load_current_values()
        self._button_rects = []
        self._row_rects = []
        # Font caching for performance
        self._cached_fonts = {}

    def load_current_values(self):
        """Load current setting values"""
        self.current_values = []
        for setting_name, key_path, options, setting_type in self.settings:
            current_value = config.get(key_path)
            if current_value in options:
                self.current_values.append(options.index(current_value))
            else:
                # Find closest match for slider values
                if setting_type == "slider" and isinstance(current_value, (int, float)):
                    closest_idx = min(range(len(options)), key=lambda i: abs(options[i] - current_value))
                    self.current_values.append(closest_idx)
                else:
                    self.current_values.append(0)

    def handle_event(self, event):
        """Handle settings events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % len(self.settings)
            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % len(self.settings)
            elif event.key == pygame.K_LEFT:
                self.current_values[self.selected_setting] = max(0, self.current_values[self.selected_setting] - 1)
                self.update_setting()
            elif event.key == pygame.K_RIGHT:
                setting_name, key_path, options, setting_type = self.settings[self.selected_setting]
                self.current_values[self.selected_setting] = min(len(options) - 1, self.current_values[self.selected_setting] + 1)
                self.update_setting()
            elif event.key == pygame.K_ESCAPE:
                return "back"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                # Check click on any left/right button
                for i, pair in enumerate(self._button_rects):
                    if not pair:
                        continue
                    left_rect, right_rect = pair
                    if left_rect and left_rect.collidepoint(mouse_pos):
                        self.selected_setting = i
                        self.current_values[i] = max(0, self.current_values[i] - 1)
                        self.update_setting()
                        return None
                    if right_rect and right_rect.collidepoint(mouse_pos):
                        self.selected_setting = i
                        setting_name, key_path, options, setting_type = self.settings[i]
                        self.current_values[i] = min(len(options) - 1, self.current_values[i] + 1)
                        self.update_setting()
                        return None
                # Click a row selects it
                for i, row in enumerate(self._row_rects):
                    if row and row.collidepoint(mouse_pos):
                        self.selected_setting = i
                        return None
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Hovering a row updates selection for better UX
            for i, row in enumerate(self._row_rects):
                if row and row.collidepoint(mouse_pos):
                    self.selected_setting = i
                    break
        return None

    def update_setting(self):
        """Update current setting value"""
        setting_name, key_path, options = self.settings[self.selected_setting]
        new_value = options[self.current_values[self.selected_setting]]
        config.set(key_path, new_value)
        config.save_config()

    def draw(self):
        """Draw simplified settings menu"""
        self.screen.fill(self.background_color)

        # Simplified layout
        panel_width = 700
        panel_height = 100 + len(self.settings) * 55
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        # Panel background
        panel_bg = (40, 40, 60)
        panel_border = (120, 120, 160)
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, panel_bg, panel_rect, 0, border_radius=8)
        pygame.draw.rect(self.screen, panel_border, panel_rect, 2, border_radius=8)

        # Title
        self.draw_text("SETTINGS", self.font_large, self.highlight_color,
                      self.screen_width // 2, panel_y - 40)

        # Settings rows
        self._button_rects = []
        self._row_rects = []
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (setting_name, key_path, options, setting_type) in enumerate(self.settings):
            y = panel_y + 50 + i * 55
            is_selected = (i == self.selected_setting)
            
            # Row background
            row_rect = pygame.Rect(panel_x + 20, y - 20, panel_width - 40, 45)
            if is_selected:
                pygame.draw.rect(self.screen, (60, 60, 80), row_rect, 0, border_radius=5)
                pygame.draw.rect(self.screen, (255, 255, 100), row_rect, 2, border_radius=5)
            self._row_rects.append(row_rect)
            
            # Setting name
            color = self.highlight_color if is_selected else self.text_color
            self.draw_text(setting_name, self.font_medium, color, panel_x + 40, y, center=False)
            
            # Current value and controls
            current_value = options[self.current_values[i]]
            
            # Left/Right buttons
            btn_size = 30
            left_rect = pygame.Rect(panel_x + panel_width - 180, y - 15, btn_size, btn_size)
            right_rect = pygame.Rect(panel_x + panel_width - 60, y - 15, btn_size, btn_size)
            
            # Draw buttons
            btn_color = (80, 80, 100) if is_selected else (60, 60, 80)
            pygame.draw.rect(self.screen, btn_color, left_rect, 0, border_radius=5)
            pygame.draw.rect(self.screen, btn_color, right_rect, 0, border_radius=5)
            
            # Button text
            self.draw_text("<", self.font_medium, (255, 255, 255), left_rect.centerx, left_rect.centery)
            self.draw_text(">", self.font_medium, (255, 255, 255), right_rect.centerx, right_rect.centery)
            
            # Value display in the middle
            center_x = (left_rect.right + right_rect.left) // 2
            if setting_type == "color":  # Color
                color_rect = pygame.Rect(center_x - 10, y - 10, 20, 20)
                pygame.draw.rect(self.screen, current_value, color_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 1)
            elif setting_type == "slider":  # Volume slider
                # Display percentage
                volume_pct = int(current_value * 100)
                self.draw_text(f"{volume_pct}%", self.font_medium, color, center_x, y)
            else:  # FPS or other values
                self.draw_text(str(current_value), self.font_medium, color, center_x, y)
            
            self._button_rects.append((left_rect, right_rect))

        # Instructions
        instr_y = panel_y + panel_height + 20
        self.draw_text("Arrow keys or click < > to adjust | ESC to go back",
                      self.font_small, self.text_color,
                      self.screen_width // 2, instr_y)

        self.update_animation()

