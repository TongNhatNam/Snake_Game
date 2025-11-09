"""
Achievement System for Snake Game
Tracks player progress and unlocks achievements
"""

import json
import os
import time
from datetime import datetime

class Achievement:
    """Individual achievement class"""
    
    def __init__(self, id, name, description, icon, condition_func, persistent=True, hidden=False):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.condition_func = condition_func
        self.persistent = persistent  # True = saves between sessions, False = resets
        self.hidden = hidden
        self.unlocked = False
        self.unlock_time = None
    
    def check_condition(self, game_stats):
        """Check if achievement condition is met"""
        if not self.unlocked and self.condition_func(game_stats):
            self.unlock()
            return True
        return False
    
    def unlock(self):
        """Unlock this achievement"""
        self.unlocked = True
        self.unlock_time = datetime.now().isoformat()

class GameStats:
    """Track game statistics for achievements"""
    
    def __init__(self):
        self.reset_session()
        # Persistent stats
        self.total_games = 0
        self.total_score = 0
        self.total_food_eaten = 0
        self.total_powerups_collected = 0
        self.highest_score = 0
        self.highest_level = 0
        self.total_playtime = 0
        
    def reset_session(self):
        """Reset session-specific stats"""
        self.session_start_time = time.time()
        self.current_score = 0
        self.current_level = 1
        self.food_eaten_this_game = 0
        self.powerups_collected_this_game = 0
        self.consecutive_food = 0
        self.max_consecutive_food = 0
        self.survival_time = 0
        self.deaths_this_game = 0
        self.perfect_level = True  # No deaths in current level

class AchievementManager:
    """Manages all achievements and notifications"""
    
    def __init__(self, save_file="achievements.json"):
        self.save_file = save_file
        self.achievements = {}
        self.game_stats = GameStats()
        self.pending_notifications = []
        self.notification_timer = 0
        
        self._define_achievements()
        self.load_progress()
        self.reset_session_achievements()  # Reset session achievements on startup
    
    def _define_achievements(self):
        """Define all available achievements"""
        achievements_data = [
            # SESSION ACHIEVEMENTS (Reset each game session)
            ("speed_demon", "Speed Demon", "Eat 5 food items in 10 seconds", ">>>", 
             lambda stats: stats.consecutive_food >= 5 and stats.survival_time <= 10, False),
            
            ("survivor", "Survivor", "Survive for 60 seconds", "60s", 
             lambda stats: stats.survival_time >= 60, False),
            
            ("perfectionist", "Perfectionist", "Complete a level without dying", "0x", 
             lambda stats: stats.perfect_level and stats.current_level > 1, False),
            
            ("collector", "Collector", "Collect 10 power-ups in one game", "10+", 
             lambda stats: stats.powerups_collected_this_game >= 10, False),
            
            ("session_master", "Session Master", "Reach score 300 in one game", "300", 
             lambda stats: stats.current_score >= 300, False),
            
            ("food_chain", "Food Chain", "Eat 20 food items in one game", "20", 
             lambda stats: stats.food_eaten_this_game >= 20, False),
            
            # PERSISTENT ACHIEVEMENTS (Saved between sessions)
            ("first_blood", "First Blood", "Complete your first game", "1st", 
             lambda stats: stats.total_games >= 1, True),
            
            ("baby_steps", "Baby Steps", "Eat 50 food items total", "50", 
             lambda stats: stats.total_food_eaten >= 50, True),
            
            ("getting_started", "Getting Started", "Reach score 500 total", "500", 
             lambda stats: stats.highest_score >= 500, True),
            
            ("power_hungry", "Power Hungry", "Collect 100 power-ups total", "100", 
             lambda stats: stats.total_powerups_collected >= 100, True),
            
            ("high_roller", "High Roller", "Reach score 1000", "1K", 
             lambda stats: stats.highest_score >= 1000, True),
            
            ("score_master", "Score Master", "Reach score 2000", "2K", 
             lambda stats: stats.highest_score >= 2000, True),
            
            ("level_up", "Level Up", "Reach level 3", "L3", 
             lambda stats: stats.highest_level >= 3, True),
            
            ("master_level", "Master Level", "Reach level 5", "L5", 
             lambda stats: stats.highest_level >= 5, True),
            
            ("glutton", "Glutton", "Eat 200 food items total", "200", 
             lambda stats: stats.total_food_eaten >= 200, True),
            
            ("veteran", "Veteran", "Play 25 games", "25G", 
             lambda stats: stats.total_games >= 25, True),
            
            ("dedication", "Dedication", "Play for 30 minutes total", "30m", 
             lambda stats: stats.total_playtime >= 1800, True),  # 30 minutes
        ]
        
        for achievement_data in achievements_data:
            achievement = Achievement(*achievement_data)
            self.achievements[achievement.id] = achievement
    
    def update_stats(self, event_type, **kwargs):
        """Update game statistics based on events"""
        if event_type == "game_start":
            self.game_stats.reset_session()
            
        elif event_type == "game_end":
            self.game_stats.total_games += 1
            self.game_stats.total_score += self.game_stats.current_score
            self.game_stats.highest_score = max(self.game_stats.highest_score, self.game_stats.current_score)
            self.game_stats.highest_level = max(self.game_stats.highest_level, self.game_stats.current_level)
            session_time = time.time() - self.game_stats.session_start_time
            self.game_stats.total_playtime += session_time
            
        elif event_type == "food_eaten":
            food_type = kwargs.get("food_type", "normal")
            if food_type in ["normal", "special"]:  # Don't count bad food
                self.game_stats.food_eaten_this_game += 1
                self.game_stats.total_food_eaten += 1
                self.game_stats.consecutive_food += 1
                self.game_stats.max_consecutive_food = max(
                    self.game_stats.max_consecutive_food, 
                    self.game_stats.consecutive_food
                )
            else:
                self.game_stats.consecutive_food = 0
                
        elif event_type == "powerup_collected":
            self.game_stats.powerups_collected_this_game += 1
            self.game_stats.total_powerups_collected += 1
            
        elif event_type == "score_update":
            self.game_stats.current_score = kwargs.get("score", 0)
            
        elif event_type == "level_update":
            self.game_stats.current_level = kwargs.get("level", 1)
            
        elif event_type == "death":
            self.game_stats.deaths_this_game += 1
            self.game_stats.perfect_level = False
            self.game_stats.consecutive_food = 0
            
        elif event_type == "survival_time":
            self.game_stats.survival_time = kwargs.get("time", 0)
    
    def check_achievements(self):
        """Check all achievements and return newly unlocked ones"""
        newly_unlocked = []
        for achievement in self.achievements.values():
            if achievement.check_condition(self.game_stats):
                newly_unlocked.append(achievement)
                self.pending_notifications.append(achievement)
        
        if newly_unlocked:
            self.save_progress()
        
        return newly_unlocked
    
    def get_notification(self):
        """Get next pending notification"""
        if self.pending_notifications and self.notification_timer <= 0:
            self.notification_timer = 3000  # 3 seconds
            return self.pending_notifications.pop(0)
        return None
    
    def update_notification_timer(self, delta_time):
        """Update notification display timer"""
        if self.notification_timer > 0:
            self.notification_timer -= delta_time
    
    def get_progress_summary(self):
        """Get achievement progress summary"""
        total = len(self.achievements)
        unlocked = sum(1 for a in self.achievements.values() if a.unlocked)
        return {
            "total": total,
            "unlocked": unlocked,
            "percentage": int((unlocked / total) * 100) if total > 0 else 0
        }
    
    def get_achievements_by_category(self):
        """Get achievements organized by unlock status"""
        unlocked = [a for a in self.achievements.values() if a.unlocked]
        locked = [a for a in self.achievements.values() if not a.unlocked and not a.hidden]
        
        # Sort by unlock time (newest first) and name
        unlocked.sort(key=lambda a: a.unlock_time or "", reverse=True)
        locked.sort(key=lambda a: a.name)
        
        return {"unlocked": unlocked, "locked": locked}
    
    def reset_session_achievements(self):
        """Reset all session-based achievements"""
        for achievement in self.achievements.values():
            if not achievement.persistent:
                achievement.unlocked = False
                achievement.unlock_time = None
    
    def get_achievements_by_type(self):
        """Get achievements organized by type (session vs persistent)"""
        session_unlocked = [a for a in self.achievements.values() if not a.persistent and a.unlocked]
        session_locked = [a for a in self.achievements.values() if not a.persistent and not a.unlocked]
        persistent_unlocked = [a for a in self.achievements.values() if a.persistent and a.unlocked]
        persistent_locked = [a for a in self.achievements.values() if a.persistent and not a.unlocked]
        
        return {
            "session": {"unlocked": session_unlocked, "locked": session_locked},
            "persistent": {"unlocked": persistent_unlocked, "locked": persistent_locked}
        }
    
    def save_progress(self):
        """Save only persistent achievement progress to file"""
        try:
            # Only save persistent achievements
            persistent_achievements = {
                aid: {
                    "unlocked": a.unlocked,
                    "unlock_time": a.unlock_time
                } for aid, a in self.achievements.items() if a.persistent
            }
            
            data = {
                "achievements": persistent_achievements,
                "stats": {
                    "total_games": self.game_stats.total_games,
                    "total_score": self.game_stats.total_score,
                    "total_food_eaten": self.game_stats.total_food_eaten,
                    "total_powerups_collected": self.game_stats.total_powerups_collected,
                    "highest_score": self.game_stats.highest_score,
                    "highest_level": self.game_stats.highest_level,
                    "total_playtime": self.game_stats.total_playtime
                }
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Silently fail if can't save
    
    def load_progress(self):
        """Load only persistent achievement progress from file"""
        if not os.path.exists(self.save_file):
            return
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load only persistent achievement progress
            achievements_data = data.get("achievements", {})
            for aid, progress in achievements_data.items():
                if aid in self.achievements and self.achievements[aid].persistent:
                    achievement = self.achievements[aid]
                    achievement.unlocked = progress.get("unlocked", False)
                    achievement.unlock_time = progress.get("unlock_time")
            
            # Load persistent stats
            stats_data = data.get("stats", {})
            for key, value in stats_data.items():
                if hasattr(self.game_stats, key):
                    setattr(self.game_stats, key, value)
                    
        except Exception:
            pass  # Silently fail if can't load

# Global achievement manager instance
achievement_manager = AchievementManager()