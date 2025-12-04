"""
Game-specific menu classes
"""

import pygame
import math
import random
from .base_menu import Menu
from ..core import config

class MainMenu(Menu):
    """Main menu screen"""
    
    def __init__(self, screen):
        super().__init__(screen)
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "High Scores", "Achievements"]
        self.buttons = []
        self.button_hover_scale = [1.0] * len(self.options)

    def handle_event(self, event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.spawn_particles(500, 300 + self.selected_option * 70, count=3)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.spawn_particles(500, 300 + self.selected_option * 70, count=3)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                selected_action = self.options[self.selected_option]
                if selected_action == "Start Game":
                    return "Select Level"
                return selected_action
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(self.buttons):
                if button_rect.collidepoint(mouse_pos):
                    self.selected_option = i
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for i, button_rect in enumerate(self.buttons):
                    if button_rect.collidepoint(mouse_pos):
                        selected_action = self.options[i]
                        if selected_action == "Start Game":
                            return "Select Level"
                        return selected_action
        return None

    def draw(self):
        """Draw main menu with modern web-friendly design"""

        gradient_offset = int(20 * math.sin(self.animation_timer * 0.02))
        color1 = (15, 25, 50)
        color2 = (35, 55, 100)
        self.draw_gradient_background(color1, color2)

        grid_color = (30, 40, 80)
        for x in range(0, self.screen_width, 50):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.screen_height), 1)
        for y in range(0, self.screen_height, 50):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.screen_width, y), 1)

        title_y = 80 + int(8 * math.sin(self.animation_timer * 0.03))
        
        for layer in range(4, 0, -1):
            glow_alpha = int(60 / layer)
            glow_color = (100 - glow_alpha, 180 - glow_alpha, 100)
            offset = layer * 1
            self.draw_text("SNAKE GAME", self.font_large, glow_color,
                          self.screen_width // 2 + offset, title_y + offset)
        
        title_color = (100, 255, 120)
        self.draw_text("SNAKE GAME", self.font_large, title_color,
                      self.screen_width // 2, title_y, shadow=True)

        subtitle_color = (180, 200, 220)
        self.draw_text("Classic Game | Modern Experience", self.font_small, subtitle_color,
                      self.screen_width // 2, title_y + 60)

        start_y = 280
        button_width = 280
        button_height = 50
        button_spacing = 75

        self.buttons = []
        for i, option in enumerate(self.options):
            y = start_y + i * button_spacing
            is_selected = (i == self.selected_option)

            target_scale = 1.08 if is_selected else 1.0
            self.button_hover_scale[i] += (target_scale - self.button_hover_scale[i]) * 0.15

            scaled_width = int(button_width * self.button_hover_scale[i])
            scaled_height = int(button_height * self.button_hover_scale[i])
            centered_x = self.screen_width // 2 - scaled_width // 2
            centered_y = y - (scaled_height - button_height) // 2

            if is_selected:
                base_color = (50, 100, 200)
                hover_color = (80, 140, 255)
            else:
                base_color = (40, 70, 150)
                hover_color = (60, 110, 200)
            
            button_rect = self.draw_button(
                option,
                centered_x,
                centered_y,
                scaled_width,
                scaled_height,
                base_color,
                hover_color,
                is_selected
            )
            
            if is_selected and self.animation_timer % 15 == 0:
                self.spawn_particles(centered_x + scaled_width // 2, 
                                   centered_y + scaled_height // 2, 
                                   count=3, color=(100, 255, 150))
            
            self.buttons.append(button_rect)

        self.draw_animated_particles()

        footer_y = self.screen_height - 50
        instr_color = (140, 160, 200)
        self.draw_text("ARROW KEYS or MOUSE TO NAVIGATE",
                      self.font_small, instr_color,
                      self.screen_width // 2, footer_y)
        self.draw_text("ENTER or CLICK TO SELECT",
                      self.font_small, instr_color,
                      self.screen_width // 2, footer_y + 35)

        self.update_animation()

class LevelSelectMenu(Menu):
    """Level selection menu screen"""

    def __init__(self, screen):
        super().__init__(screen)
        self.selected_level = 0
        self.max_level = config.get("levels.max_level")
        self.level_names = config.get("levels.level_names")
        self.obstacle_counts = config.get("levels.obstacle_count")
        self.speed_multipliers = config.get("levels.speed_multiplier")
        self.level_scales = [1.0] * self.max_level

    def handle_event(self, event):
        """Handle level selection events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % self.max_level
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % self.max_level
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return f"start_level_{self.selected_level + 1}"
            elif event.key == pygame.K_ESCAPE:
                return "back"
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            start_y = 140
            level_height = 80
            card_width = 700
            card_x = (self.screen_width - card_width) // 2
            
            for i in range(self.max_level):
                y = start_y + i * level_height
                card_height = 65
                card_y = y - (card_height - 65) // 2
                level_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                if level_rect.collidepoint(mouse_pos):
                    self.selected_level = i
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                start_y = 140
                level_height = 80
                card_width = 700
                card_x = (self.screen_width - card_width) // 2
                
                for i in range(self.max_level):
                    y = start_y + i * level_height
                    card_height = 65
                    card_y = y - (card_height - 65) // 2
                    level_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                    if level_rect.collidepoint(mouse_pos):
                        return f"start_level_{i + 1}"
        return None

    def draw(self):
        """Draw level selection with improved card layout design"""

        color1 = (15, 30, 55)
        color2 = (35, 50, 100)
        self.draw_gradient_background(color1, color2)

        grid_color = (25, 35, 70)
        for x in range(0, self.screen_width, 60):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.screen_height), 1)
        for y in range(0, self.screen_height, 60):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.screen_width, y), 1)

        title_y = 50
        title_color = (100, 255, 120)
        self.draw_text("SELECT DIFFICULTY", self.font_large, title_color,
                      self.screen_width // 2, title_y, shadow=True)
        subtitle_color = (150, 180, 220)
        self.draw_text("Choose your challenge", self.font_small, subtitle_color,
                      self.screen_width // 2, title_y + 50)

        start_y = 140
        level_height = 80
        card_width = 700
        card_x = (self.screen_width - card_width) // 2

        for i in range(self.max_level):
            y = start_y + i * level_height
            is_selected = (i == self.selected_level)

            target_scale = 1.06 if is_selected else 1.0
            self.level_scales[i] += (target_scale - self.level_scales[i]) * 0.12

            card_height = int(65 * self.level_scales[i])
            card_y = y - (card_height - 65) // 2

            if is_selected:
                grad_start = (70, 110, 200)
                grad_end = (100, 140, 230)
                
                for draw_y in range(card_height):
                    progress = draw_y / card_height
                    line_color = tuple(
                        int(grad_start[j] + (grad_end[j] - grad_start[j]) * progress)
                        for j in range(3)
                    )
                    pygame.draw.line(self.screen, line_color, 
                                   (card_x, card_y + draw_y), (card_x + card_width, card_y + draw_y))
                
                for offset in [6, 4, 2]:
                    glow_surface = pygame.Surface((card_width + offset * 2, card_height + offset * 2))
                    glow_surface.set_alpha(15)
                    glow_surface.fill((100, 180, 255))
                    self.screen.blit(glow_surface, (card_x - offset, card_y - offset))
                
                border_color = (100, 200, 255)
                border_width = 3
            else:
                card_color = (35, 60, 130)
                pygame.draw.rect(self.screen, card_color, (card_x, card_y, card_width, card_height))
                border_color = (80, 120, 180)
                border_width = 2
            
            pygame.draw.rect(self.screen, border_color, (card_x, card_y, card_width, card_height), border_width)
            
            level_name = self.level_names[i] if i < len(self.level_names) else f"Level {i + 1}"
            
            level_num_color = (255, 255, 100) if is_selected else (200, 200, 200)
            self.draw_text(f"LEVEL {i + 1}", self.font_small, level_num_color,
                          card_x + 30, card_y + card_height // 2, center=False)
            
            level_name_color = (255, 255, 255) if is_selected else (220, 220, 220)
            self.draw_text(level_name, self.font_medium, level_name_color,
                          card_x + 120, card_y + card_height // 2, center=False)
            
            obstacles = self.obstacle_counts[i] if i < len(self.obstacle_counts) else 0
            speed = self.speed_multipliers[i] if i < len(self.speed_multipliers) else 1.0
            
            speed_badge_x = card_x + card_width - 320
            speed_badge_y = card_y + card_height // 2 - 12
            speed_badge_width = 120
            speed_badge_height = 24
            
            speed_badge_color = (100, 180, 100) if is_selected else (80, 140, 80)
            pygame.draw.rect(self.screen, speed_badge_color, 
                           (speed_badge_x, speed_badge_y, speed_badge_width, speed_badge_height))
            pygame.draw.rect(self.screen, (150, 220, 150) if is_selected else (120, 180, 120),
                           (speed_badge_x, speed_badge_y, speed_badge_width, speed_badge_height), 1)
            
            badge_text_color = (255, 255, 255) if is_selected else (220, 220, 220)
            self.draw_text(f"Speed: {speed}x", self.font_small, badge_text_color,
                          speed_badge_x + speed_badge_width // 2, speed_badge_y + speed_badge_height // 2)
            
            obs_badge_x = card_x + card_width - 160
            obs_badge_y = card_y + card_height // 2 - 12
            obs_badge_width = 130
            obs_badge_height = 24
            
            obs_badge_color = (200, 100, 100) if is_selected else (160, 80, 80)
            pygame.draw.rect(self.screen, obs_badge_color,
                           (obs_badge_x, obs_badge_y, obs_badge_width, obs_badge_height))
            pygame.draw.rect(self.screen, (220, 150, 150) if is_selected else (180, 120, 120),
                           (obs_badge_x, obs_badge_y, obs_badge_width, obs_badge_height), 1)
            
            self.draw_text(f"Obstacles: {obstacles}", self.font_small, badge_text_color,
                          obs_badge_x + obs_badge_width // 2, obs_badge_y + obs_badge_height // 2)
            
            if is_selected and self.animation_timer % 20 == 0:
                self.spawn_particles(card_x + card_width // 2,
                                   card_y + card_height // 2,
                                   count=2, color=(100, 200, 255))

        self.draw_animated_particles()

        instr_color = (140, 160, 200)
        self.draw_text("Use UP/DOWN arrow keys or mouse to select | ENTER to start | ESC to back",
                      self.font_small, instr_color,
                      self.screen_width // 2, self.screen_height - 40)

        self.update_animation()

class GameOverMenu(Menu):
    """Game over screen"""

    def __init__(self, screen, final_score, level):
        super().__init__(screen)
        self.final_score = final_score
        self.level = level
        from .score_menu import HighScoreMenu
        self.high_score_menu = HighScoreMenu(screen)
        self.show_high_score = False
        
        # Add score to high scores
        self.high_score_menu.add_score(final_score, level)

    def handle_event(self, event):
        """Handle game over events"""
        if self.show_high_score:
            return self._handle_high_score_event(event)
        
        if event.type == pygame.KEYDOWN:
            return self._handle_keyboard_event(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_event(event)
        
        return None
    
    def _handle_high_score_event(self, event):
        """Handle events when high score screen is shown"""
        result = self.high_score_menu.handle_event(event)
        if result == "back":
            self.show_high_score = False
        return result
    
    def _handle_keyboard_event(self, event):
        """Handle keyboard events"""
        key_actions = {
            pygame.K_r: "restart",
            pygame.K_m: "menu",
            pygame.K_h: None
        }
        
        if event.key in key_actions:
            if event.key == pygame.K_h:
                self.show_high_score = True
                return None
            return key_actions[event.key]
        
        return None
    
    def _handle_mouse_event(self, event):
        """Handle mouse click events"""
        if event.button != 1:
            return None
        
        mouse_pos = pygame.mouse.get_pos()
        
        actions = ["restart", "menu", None]
        start_y = 400
        for i in range(3):
            y = start_y + i * 40
            text_rect = pygame.Rect(self.screen_width // 2 - 100, y - 15, 200, 30)
            if text_rect.collidepoint(mouse_pos):
                if i == 2:  # High Scores
                    self.show_high_score = True
                    return None
                return actions[i]
        
        return None

    def draw(self):
        """Draw game over screen with modern web-friendly design"""
        if self.show_high_score:
            self.high_score_menu.draw()
            return

        color1 = (20, 15, 35)
        color2 = (40, 25, 60)
        self.draw_gradient_background(color1, color2)

        grid_color = (30, 25, 45)
        for x in range(0, self.screen_width, 50):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.screen_height), 1)
        for y in range(0, self.screen_height, 50):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.screen_width, y), 1)

        game_over_y = 90
        
        for layer in range(5, 0, -1):
            glow_alpha = int(40 / layer)
            glow_color = (255 - glow_alpha, 30, 30)
            offset = layer * 1
            self.draw_text("GAME OVER", self.font_large, glow_color,
                          self.screen_width // 2 + offset, game_over_y + offset)
        
        game_over_color = (255, 80, 80)
        self.draw_text("GAME OVER", self.font_large, game_over_color,
                      self.screen_width // 2, game_over_y, shadow=True)

        card_y = 200
        card_width = 500
        card_height = 100
        card_x = (self.screen_width - card_width) // 2
        
        for draw_y in range(card_height):
            progress = draw_y / card_height
            line_color = (
                int(50 + (80 - 50) * progress),
                int(60 + (90 - 60) * progress),
                int(120 + (150 - 120) * progress)
            )
            pygame.draw.line(self.screen, line_color,
                           (card_x, card_y + draw_y), (card_x + card_width, card_y + draw_y))
        
        pygame.draw.rect(self.screen, (100, 150, 200), (card_x, card_y, card_width, card_height), 3)
        
        pulse_intensity = int(50 * math.sin(self.animation_timer * 0.05))
        score_color = (200 + pulse_intensity, 255, 150 + pulse_intensity)
        self.draw_text(f"Final Score: {self.final_score:06d}", self.font_large, score_color,
                      self.screen_width // 2, card_y + 35, shadow=True)
        
        level_color = (150, 220, 255)
        self.draw_text(f"Level: {self.level}", self.font_medium, level_color,
                      self.screen_width // 2, card_y + 75, shadow=False)

        options = [
            ("Play Again", "R", (0, 200, 100)),
            ("Main Menu", "M", (200, 150, 50)),
            ("High Scores", "H", (100, 150, 255))
        ]

        button_y = 350
        button_spacing = 65
        
        for i, (text, key, base_color) in enumerate(options):
            y = button_y + i * button_spacing
            
            button_width = 300
            button_height = 45
            button_x = self.screen_width // 2 - button_width // 2
            
            hover_color = tuple(min(255, c + 40) for c in base_color)
            pygame.draw.rect(self.screen, base_color, (button_x, y, button_width, button_height))
            
            pygame.draw.rect(self.screen, hover_color, (button_x, y, button_width, button_height), 2)
            
            button_text = f"[{key}] {text}"
            text_color = (255, 255, 255)
            self.draw_text(button_text, self.font_medium, text_color,
                          button_x + button_width // 2, y + button_height // 2, shadow=False)
        
        self.draw_animated_particles()

        footer_color = (150, 170, 200)
        self.draw_text("Press R, M, or H to select | ESC to go back",
                      self.font_small, footer_color,
                      self.screen_width // 2, self.screen_height - 50)

        self.update_animation()

