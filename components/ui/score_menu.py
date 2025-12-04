"""
High score menu and management
"""

import json
import os
import pygame
import math
from .base_menu import Menu

class HighScoreMenu(Menu):
    """High scores menu screen"""

    def __init__(self, screen):
        super().__init__(screen)
        self.high_scores_file = "high_scores.json"
        self.high_scores = self.load_high_scores()
        self.selected_score = None

    def load_high_scores(self):
        """Load high scores from file"""

        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def save_high_scores(self):
        """Save high scores to file"""

        try:
            with open(self.high_scores_file, 'w', encoding='utf-8') as f:
                json.dump(self.high_scores, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def add_score(self, score, level):
        """Add new score to high scores"""

        self.high_scores.append({"score": score, "level": level})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        self.save_high_scores()

    def handle_event(self, event):
        """Handle high scores events"""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                # Scroll up
                pass
            elif event.key == pygame.K_DOWN:
                # Scroll down
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                return "back"
        return None

    def draw(self):
        """Draw high scores menu with modern styling"""

        gradient_offset = int(40 * math.sin(self.animation_timer * 0.02))
        color1 = (20, 50, 40)
        color2 = (50, 80 + gradient_offset // 2, 100)
        self.draw_gradient_background(color1, color2)

        title_y = 80 + int(10 * math.sin(self.animation_timer * 0.04))
        
        for layer in range(3, 0, -1):
            glow_alpha = int(100 / (layer * 1.5))
            glow_color = (100 - glow_alpha, 200 - glow_alpha, 100)
            offset = layer * 2
            self.draw_text("HIGH SCORES", self.font_large, glow_color,
                          self.screen_width // 2 + offset, title_y + offset)
        
        title_color = (100 + int(100 * math.sin(self.animation_timer * 0.05)),
                      200 + int(50 * math.sin(self.animation_timer * 0.06)),
                      100 + int(50 * math.sin(self.animation_timer * 0.07)))
        self.draw_text("HIGH SCORES", self.font_large, title_color,
                      self.screen_width // 2, title_y, shadow=True)

        if not self.high_scores:
            no_scores_color = (180, 180, 200)
            self.draw_text("No scores yet! Be the first!", self.font_medium, no_scores_color,
                          self.screen_width // 2, 300)
        else:
            start_y = 200
            for i, score_data in enumerate(self.high_scores):
                y = start_y + i * 45
                rank = i + 1
                score = score_data["score"]
                level = score_data["level"]

                try:
                    score_bg = pygame.Rect(150, y - 18, 700, 36)
                    
                    if rank <= 3:
                        if rank == 1:
                            bg_color = (255, 200, 0)  # Gold
                            pulse = int(30 * math.sin(self.animation_timer * 0.1))
                        elif rank == 2:
                            bg_color = (200, 200, 200)  # Silver
                            pulse = int(20 * math.sin(self.animation_timer * 0.08))
                        else:
                            bg_color = (200, 120, 60)  # Bronze
                            pulse = int(20 * math.sin(self.animation_timer * 0.06))
                        
                        for draw_y in range(36):
                            progress = draw_y / 36
                            line_color = tuple(int(c * (0.3 + 0.2 * progress)) for c in bg_color)
                            pygame.draw.line(self.screen, line_color,
                                           (150, y - 18 + draw_y), (850, y - 18 + draw_y))
                    else:
                        bg_color = (50, 50, 80) if i % 2 == 0 else (60, 60, 90)
                        pygame.draw.rect(self.screen, bg_color, score_bg)
                    
                    pygame.draw.rect(self.screen, (150, 150, 150), score_bg, 2)
                except Exception:
                    pass
                
                try:
                    top_colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
                    rank_color = top_colors[i] if i < len(top_colors) else (200, 200, 255)
                except (IndexError, TypeError):
                    rank_color = (200, 200, 255)
                
                rank_text = f"#{rank}" if i < 3 else f"{rank}."
                self.draw_text(rank_text, self.font_medium, rank_color, 200, y, shadow=True)

                if i < 3:
                    score_color = (255, 255, 100)
                    score_font = self.font_large
                else:
                    score_color = (200, 200, 255)
                    score_font = self.font_medium
                
                self.draw_text(f"{score:06d}", score_font, score_color, 450, y, shadow=True)
                
                level_color = (150, 200, 255)
                self.draw_text(f"Level {level}", self.font_medium, level_color, 700, y, shadow=True)

        self.draw_animated_particles()

        instr_color = (180, 180, 200)
        self.draw_text("Press ESC or CLICK anywhere to go back",
                      self.font_small, instr_color,
                      self.screen_width // 2, self.screen_height - 50)

        self.update_animation()