"""
Settings menu for game configuration
"""

import pygame
import math
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
        self.row_scales = [1.0] * len(self.settings)

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
        """Draw simplified settings menu with modern styling"""
        # Animated gradient background
        gradient_offset = int(40 * math.sin(self.animation_timer * 0.02))
        color1 = (20, 40, 60)
        color2 = (50, 40, 100 + gradient_offset // 2)
        self.draw_gradient_background(color1, color2)

        # Title
        title_y = 100 + int(8 * math.sin(self.animation_timer * 0.04))
        title_color = (100 + int(100 * math.sin(self.animation_timer * 0.05)),
                      200 + int(50 * math.sin(self.animation_timer * 0.06)),
                      100)
        self.draw_text("SETTINGS", self.font_large, title_color,
                      self.screen_width // 2, title_y, shadow=True)

        # Settings
        self._button_rects = []
        self._row_rects = []
        
        start_y = 250
        row_height = 90
        
        for i, (setting_name, key_path, options) in enumerate(self.settings):
            y = start_y + i * row_height
            is_selected = (i == self.selected_setting)
            current_value = options[self.current_values[i]]
            
            # Smooth scale animation
            target_scale = 1.05 if is_selected else 1.0
            self.row_scales[i] += (target_scale - self.row_scales[i]) * 0.1
            
            # Row background with scale
            row_width = int(600 * self.row_scales[i])
            row_height_scaled = int(60 * self.row_scales[i])
            row_x = self.screen_width // 2 - row_width // 2
            row_y = y - (row_height_scaled - 60) // 2
            
            # Gradient background
            for draw_y in range(row_height_scaled):
                progress = draw_y / row_height_scaled
                if is_selected:
                    line_color = (int(80 + 40 * progress), int(80 + 40 * progress), 
                                int(120 + 30 * progress))
                else:
                    line_color = (int(60 + 10 * progress), int(60 + 10 * progress), 
                                int(80 + 10 * progress))
                pygame.draw.line(self.screen, line_color, (row_x, row_y + draw_y), 
                               (row_x + row_width, row_y + draw_y))
            
            row_rect = pygame.Rect(row_x, row_y, row_width, row_height_scaled)
            
            # Border
            if is_selected:
                border_color = (255, 200 + int(55 * math.sin(self.animation_timer * 0.08)), 100)
                border_width = 3
                # Glow effect
                glow_color = (border_color[0] // 2, border_color[1] // 2, border_color[2] // 2)
                pygame.draw.rect(self.screen, glow_color, (row_x - 2, row_y - 2, 
                                row_width + 4, row_height_scaled + 4), 1)
            else:
                border_color = (150, 150, 150)
                border_width = 2
            
            pygame.draw.rect(self.screen, border_color, row_rect, border_width)
            self._row_rects.append(row_rect)
            
            # Setting name (left aligned)
            name_color = (255, 255, 100) if is_selected else (200, 200, 200)
            self.draw_text(setting_name, self.font_medium, name_color,
                          row_x + 30, row_y + 15, center=False)
            
            # Left button
            left_rect = pygame.Rect(row_x + row_width - 170, row_y + row_height_scaled // 2 - 15, 35, 30)
            btn_color = (100, 120, 180) if is_selected else (80, 100, 160)
            pygame.draw.rect(self.screen, btn_color, left_rect, 0, border_radius=5)
            pygame.draw.rect(self.screen, (255, 255, 100) if is_selected else (150, 150, 150), 
                           left_rect, 2, border_radius=5)
            left_text = self.font_medium.render("<", True, (255, 255, 255))
            left_text_rect = left_text.get_rect(center=left_rect.center)
            self.screen.blit(left_text, left_text_rect)
            
            # Value display (center)
            if isinstance(current_value, tuple):  # Color
                color_rect = pygame.Rect(row_x + row_width - 115, row_y + row_height_scaled // 2 - 10, 25, 20)
                pygame.draw.rect(self.screen, current_value, color_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 2)
            else:  # FPS
                value_surface = self.font_medium.render(str(current_value), True, name_color)
                value_rect = value_surface.get_rect(center=(row_x + row_width - 102, row_y + row_height_scaled // 2))
                self.screen.blit(value_surface, value_rect)
            
            # Right button
            right_rect = pygame.Rect(row_x + row_width - 70, row_y + row_height_scaled // 2 - 15, 35, 30)
            pygame.draw.rect(self.screen, btn_color, right_rect, 0, border_radius=5)
            pygame.draw.rect(self.screen, (255, 255, 100) if is_selected else (150, 150, 150), 
                           right_rect, 2, border_radius=5)
            right_text = self.font_medium.render(">", True, (255, 255, 255))
            right_text_rect = right_text.get_rect(center=right_rect.center)
            self.screen.blit(right_text, right_text_rect)
            
            self._button_rects.append((left_rect, right_rect))

        # Draw particles
        self.draw_animated_particles()

        # Instructions
        instr_color = (180, 180, 200)
        self.draw_text("Arrow keys or click < > to adjust | ESC to go back",
                      self.font_small, instr_color,
                      self.screen_width // 2, self.screen_height - 80)

        self.update_animation()

