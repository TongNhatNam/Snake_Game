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
            ("FPS", "screen.fps", [5, 10, 15, 20, 30, 60]),
            ("Snake Color", "colors.snake", [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 100, 255), (100, 255, 255)])
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
        for setting_name, key_path, options in self.settings:
            current_value = config.get(key_path)
            if current_value in options:
                self.current_values.append(options.index(current_value))
            else:
                # Find closest match for slider values
                if isinstance(current_value, (int, float)):
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
                setting_name, key_path, options = self.settings[self.selected_setting]
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
                        setting_name, key_path, options = self.settings[i]
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

        # Title
        title_surface = self.font_large.render("SETTINGS", True, self.highlight_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(title_surface, title_rect)

        # Settings
        self._button_rects = []
        self._row_rects = []
        
        start_y = 250
        row_height = 80
        
        for i, (setting_name, key_path, options) in enumerate(self.settings):
            y = start_y + i * row_height
            is_selected = (i == self.selected_setting)
            current_value = options[self.current_values[i]]
            
            # Row background
            row_rect = pygame.Rect(200, y - 25, 600, 50)
            if is_selected:
                pygame.draw.rect(self.screen, (60, 60, 80), row_rect, 0, border_radius=5)
                pygame.draw.rect(self.screen, (255, 255, 100), row_rect, 2, border_radius=5)
            self._row_rects.append(row_rect)
            
            # Setting name (left aligned)
            name_color = self.highlight_color if is_selected else self.text_color
            name_surface = self.font_medium.render(setting_name, True, name_color)
            self.screen.blit(name_surface, (220, y - 10))
            
            # Left button
            left_rect = pygame.Rect(500, y - 15, 30, 30)
            btn_color = (80, 80, 100) if is_selected else (60, 60, 80)
            pygame.draw.rect(self.screen, btn_color, left_rect, 0, border_radius=5)
            left_text = self.font_medium.render("<", True, (255, 255, 255))
            left_text_rect = left_text.get_rect(center=left_rect.center)
            self.screen.blit(left_text, left_text_rect)
            
            # Value display (center)
            if isinstance(current_value, tuple):  # Color
                color_rect = pygame.Rect(560, y - 10, 20, 20)
                pygame.draw.rect(self.screen, current_value, color_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 1)
            else:  # FPS
                value_surface = self.font_medium.render(str(current_value), True, name_color)
                value_rect = value_surface.get_rect(center=(570, y))
                self.screen.blit(value_surface, value_rect)
            
            # Right button
            right_rect = pygame.Rect(610, y - 15, 30, 30)
            pygame.draw.rect(self.screen, btn_color, right_rect, 0, border_radius=5)
            right_text = self.font_medium.render(">", True, (255, 255, 255))
            right_text_rect = right_text.get_rect(center=right_rect.center)
            self.screen.blit(right_text, right_text_rect)
            
            self._button_rects.append((left_rect, right_rect))

        # Instructions
        instr_surface = self.font_small.render("Arrow keys or click < > to adjust | ESC to go back", True, self.text_color)
        instr_rect = instr_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        self.screen.blit(instr_surface, instr_rect)

        self.update_animation()

