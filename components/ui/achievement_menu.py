"""
Achievement Menu for displaying unlocked achievements and progress
"""

import pygame
import math
from .base_menu import Menu
from ..core.achievement_manager import achievement_manager

class AchievementMenu(Menu):
    """Achievement display menu"""
    
    def __init__(self, screen):
        super().__init__(screen)
        self.scroll_offset = 0
        self.max_scroll = 0
        self.selected_achievement = None
        
    def handle_event(self, event):
        """Handle achievement menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 40)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 40)
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 40))
        elif event.type == pygame.MOUSEMOTION:
            # Update selected achievement based on mouse position
            self._update_selection_from_mouse(pygame.mouse.get_pos())
        
        return None
    
    def _update_selection_from_mouse(self, mouse_pos):
        """Update selected achievement based on mouse position"""
        achievements = achievement_manager.get_achievements_by_type()
        session_achievements = achievements["session"]["unlocked"] + achievements["session"]["locked"]
        persistent_achievements = achievements["persistent"]["unlocked"] + achievements["persistent"]["locked"]
        
        current_y = 120
        
        # Check session achievements
        if session_achievements:
            current_y += 40  # Section header
            for achievement in session_achievements:
                y = current_y - self.scroll_offset
                if 50 <= y <= self.screen_height - 50:
                    rect = pygame.Rect(50, y, self.screen_width - 100, 70)
                    if rect.collidepoint(mouse_pos):
                        self.selected_achievement = achievement
                        return
                current_y += 80
        
        # Check persistent achievements
        if persistent_achievements:
            current_y += 60  # Extra spacing + section header
            for achievement in persistent_achievements:
                y = current_y - self.scroll_offset
                if 50 <= y <= self.screen_height - 50:
                    rect = pygame.Rect(50, y, self.screen_width - 100, 70)
                    if rect.collidepoint(mouse_pos):
                        self.selected_achievement = achievement
                        return
                current_y += 80
        
        self.selected_achievement = None
    
    def draw(self):
        """Draw achievement menu with modern styling"""
        # Animated gradient background
        gradient_offset = int(50 * math.sin(self.animation_timer * 0.02))
        color1 = (20, 40, 60)
        color2 = (40, 60 + gradient_offset // 2, 120)
        self.draw_gradient_background(color1, color2)
        
        # Title
        title_y = 50 + int(8 * math.sin(self.animation_timer * 0.04))
        title_color = (100 + int(100 * math.sin(self.animation_timer * 0.05)),
                      200 + int(50 * math.sin(self.animation_timer * 0.06)),
                      100 + int(50 * math.sin(self.animation_timer * 0.07)))
        self.draw_text("ACHIEVEMENTS", self.font_large, title_color,
                      self.screen_width // 2, title_y, shadow=True)
        
        # Achievement list organized by type
        achievements = achievement_manager.get_achievements_by_type()
        
        # Progress summary
        session_count = len(achievements["session"]["unlocked"])
        persistent_count = len(achievements["persistent"]["unlocked"])
        session_total = len(achievements["session"]["unlocked"]) + len(achievements["session"]["locked"])
        persistent_total = len(achievements["persistent"]["unlocked"]) + len(achievements["persistent"]["locked"])
        
        progress_text = f"Session: {session_count}/{session_total} | Persistent: {persistent_count}/{persistent_total}"
        progress_color = (150, 200, 255)
        self.draw_text(progress_text, self.font_medium, progress_color,
                      self.screen_width // 2, 110, shadow=True)
        
        # Combine all achievements for display
        session_achievements = achievements["session"]["unlocked"] + achievements["session"]["locked"]
        persistent_achievements = achievements["persistent"]["unlocked"] + achievements["persistent"]["locked"]
        
        # Draw achievements
        start_y = 120 - self.scroll_offset
        current_y = start_y
        
        # Draw session achievements section
        if session_achievements:
            section_y = current_y - self.scroll_offset
            if section_y > 50 and section_y < self.screen_height - 50:
                section_color = (150, 200, 100)
                self.draw_text("SESSION ACHIEVEMENTS", self.font_medium, section_color,
                              70, section_y, center=False)
            current_y += 40
            
            for achievement in session_achievements:
                y = current_y - self.scroll_offset
                if y > 50 and y < self.screen_height - 50:
                    self._draw_achievement(achievement, 50, y, self.screen_width - 100, 70)
                current_y += 80
        
        # Draw persistent achievements section
        if persistent_achievements:
            current_y += 20  # Extra spacing
            section_y = current_y - self.scroll_offset
            if section_y > 50 and section_y < self.screen_height - 50:
                section_color = (100, 200, 100)
                self.draw_text("PERSISTENT ACHIEVEMENTS", self.font_medium, section_color,
                              70, section_y, center=False)
            current_y += 40
            
            for achievement in persistent_achievements:
                y = current_y - self.scroll_offset
                if y > 50 and y < self.screen_height - 50:
                    self._draw_achievement(achievement, 50, y, self.screen_width - 100, 70)
                current_y += 80
        
        # Update max scroll based on total content height
        total_content_height = current_y - start_y
        visible_height = self.screen_height - 200
        self.max_scroll = max(0, total_content_height - visible_height)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            self._draw_scrollbar()
        
        # Draw particles
        self.draw_animated_particles()
        
        # Instructions
        instr_color = (180, 180, 200)
        self.draw_text("ESC to go back | Mouse wheel or UP/DOWN to scroll",
                      self.font_small, instr_color,
                      self.screen_width // 2, self.screen_height - 30)
        
        self.update_animation()
    
    def _draw_achievement(self, achievement, x, y, width, height):
        """Draw individual achievement"""
        is_unlocked = achievement.unlocked
        is_selected = (achievement == self.selected_achievement)
        
        # Background with gradient
        if is_selected:
            bg_color = (80, 80, 120)
            border_color = (255, 255, 100)
            border_width = 2
        else:
            bg_color = (60, 60, 100) if is_unlocked else (40, 40, 60)
            border_color = (100, 100, 120)
            border_width = 1
        
        # Draw gradient background
        for draw_y in range(height):
            progress = draw_y / height
            if is_selected:
                line_color = (int(80 + 40 * progress), int(80 + 40 * progress), 
                            int(120 + 30 * progress))
            else:
                line_color = bg_color
            pygame.draw.line(self.screen, line_color, (x, y + draw_y), (x + width, y + draw_y))
        
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=8)
        
        # Icon
        icon_size = 40
        icon_x = x + 15
        icon_y = y + (height - icon_size) // 2
        
        # Different colors for session vs persistent
        if achievement.persistent:
            unlock_color = (100, 200, 100)  # Green for persistent
            lock_color = (60, 60, 60)
        else:
            unlock_color = (255, 200, 100)  # Orange for session
            lock_color = (80, 60, 40)
        
        if is_unlocked:
            # Draw icon (colored circle with achievement text)
            pygame.draw.circle(self.screen, unlock_color, 
                             (icon_x + icon_size//2, icon_y + icon_size//2), icon_size//2 - 2)
            pygame.draw.circle(self.screen, (255, 255, 255), 
                             (icon_x + icon_size//2, icon_y + icon_size//2), icon_size//2 - 2, 2)
            
            # Draw achievement icon text
            self.draw_text(achievement.icon, self.font_small, (255, 255, 255),
                          icon_x + icon_size//2, icon_y + icon_size//2)
        else:
            # Grayed out icon
            pygame.draw.circle(self.screen, lock_color, 
                             (icon_x + icon_size//2, icon_y + icon_size//2), icon_size//2 - 2)
            pygame.draw.circle(self.screen, (100, 100, 100), 
                             (icon_x + icon_size//2, icon_y + icon_size//2), icon_size//2 - 2, 2)
            
            self.draw_text("?", self.font_small, (100, 100, 100),
                          icon_x + icon_size//2, icon_y + icon_size//2)
        
        # Text
        text_x = icon_x + icon_size + 15
        text_color = (255, 255, 100) if is_unlocked else (150, 150, 150)
        
        # Achievement name with animation
        name_scale = 1.05 if is_selected else 1.0
        self.draw_text(achievement.name, self.font_medium, text_color,
                      text_x, y + 20, center=False)
        
        # Achievement description with type indicator
        desc_color = self.text_color if is_unlocked else (100, 100, 100)
        type_text = " [SESSION]" if not achievement.persistent else " [PERSISTENT]"
        full_description = achievement.description + type_text
        self.draw_text(full_description, self.font_small, desc_color,
                      text_x, y + 45, center=False)
        
        # Unlock time for unlocked achievements
        if is_unlocked and achievement.unlock_time:
            try:
                from datetime import datetime
                unlock_dt = datetime.fromisoformat(achievement.unlock_time)
                
                # Smart date formatting
                now = datetime.now()
                days_ago = (now - unlock_dt).days
                
                if days_ago == 0:
                    time_text = "Today"
                elif days_ago == 1:
                    time_text = "Yesterday"
                elif days_ago < 7:
                    time_text = f"{days_ago}d ago"
                elif days_ago < 30:
                    weeks_ago = days_ago // 7
                    time_text = f"{weeks_ago}w ago"
                else:
                    time_text = unlock_dt.strftime("%d/%m/%y")
                
                self.draw_text(time_text, self.font_small, (150, 150, 150),
                              x + width - 70, y + 20, center=False)
            except Exception:
                # Fallback if datetime parsing fails
                self.draw_text("Unlocked", self.font_small, (150, 150, 150),
                              x + width - 60, y + 20, center=False)
    
    def _draw_scrollbar(self):
        """Draw scrollbar for achievement list"""
        if self.max_scroll <= 0:
            return
        
        # Scrollbar dimensions
        bar_width = 8
        bar_x = self.screen_width - 20
        bar_y = 120
        bar_height = self.screen_height - 200
        
        # Background
        pygame.draw.rect(self.screen, (60, 60, 60), 
                        (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        
        # Thumb
        thumb_height = max(20, int(bar_height * (bar_height / (bar_height + self.max_scroll))))
        thumb_y = bar_y + int((self.scroll_offset / self.max_scroll) * (bar_height - thumb_height))
        
        pygame.draw.rect(self.screen, (200, 150, 100),
                        (bar_x, thumb_y, bar_width, thumb_height), border_radius=4)

class AchievementNotification:
    """Achievement unlock notification overlay"""
    
    def __init__(self, achievement):
        self.achievement = achievement
        self.timer = 3000  # 3 seconds
        self.slide_progress = 0
        self.max_slide = 1.0
    
    def update(self, delta_time):
        """Update notification animation"""
        self.timer -= delta_time
        
        # Slide in/out animation
        if self.timer > 2500:  # Slide in
            self.slide_progress = min(1.0, self.slide_progress + delta_time / 500)
        elif self.timer < 500:  # Slide out
            self.slide_progress = max(0.0, self.slide_progress - delta_time / 500)
        
        return self.timer > 0
    
    def draw(self, screen, font_medium, font_small):
        """Draw notification"""
        if self.slide_progress <= 0:
            return
        
        # Notification dimensions
        width = 350
        height = 80
        x = screen.get_width() - width * self.slide_progress
        y = 20
        
        # Background with glow
        bg_color = (40, 80, 40)
        border_color = (100, 255, 100)
        
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
        
        # Achievement unlocked text
        text_surface = font_small.render("ACHIEVEMENT UNLOCKED!", True, (255, 255, 100))
        screen.blit(text_surface, (x + 15, y + 10))
        
        # Icon (achievement icon in circle)
        pygame.draw.circle(screen, (100, 200, 100), (x + 30, y + 45), 15)
        pygame.draw.circle(screen, (255, 255, 255), (x + 30, y + 45), 15, 2)
        icon_surface = font_small.render(self.achievement.icon, True, (255, 255, 255))
        icon_rect = icon_surface.get_rect(center=(x + 30, y + 45))
        screen.blit(icon_surface, icon_rect)
        
        # Achievement name
        name_surface = font_medium.render(self.achievement.name, True, (255, 255, 255))
        screen.blit(name_surface, (x + 60, y + 30))
        
        # Description
        desc_surface = font_small.render(self.achievement.description, True, (200, 200, 200))
        screen.blit(desc_surface, (x + 15, y + 55))