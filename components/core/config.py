"""
Configuration file for Snake Game
Contains all game settings, colors, and constants
"""

import json
import os

# Default game settings
DEFAULT_CONFIG = {
    "screen": {
        "width": 1000,
        "height": 700,
        "fps": 15
    },
    "game": {
        "block_size": 20,
        "initial_speed": 10
    },
    "colors": {
        "background": [0, 0, 0],
        "snake": [0, 255, 0],
        "snake_head": [0, 200, 0],
        "food_normal": [255, 0, 0],
        "food_special": [255, 255, 0],
        "food_bad": [128, 0, 128],
        "obstacle": [100, 100, 100],
        "powerup_slow": [255, 165, 0],
        "powerup_wall": [128, 128, 128],
        "text": [255, 255, 255],
        "text_highlight": [255, 255, 0]
    },
    "food": {
        "normal_score": 10,
        "special_score": 50,
        "bad_penalty": 20,
        "special_spawn_chance": 0.1,
        "special_spawn_interval_min": 15000,  # 15 seconds
        "special_spawn_interval_max": 25000,  # 25 seconds
        "special_lifetime": 12000,            # 12 seconds
        "special_warning_time": 3000,         # 3 seconds warning
        "bad_spawn_interval_min": 20000,      # 20 seconds
        "bad_spawn_interval_max": 35000,      # 35 seconds
        "bad_lifetime": 10000,                # 10 seconds
        "bad_warning_time": 3000              # 3 seconds warning
    },
    "powerups": {
        "slow_duration": 5000,   # 5 seconds
        "wall_duration": 5000,   # 5 seconds
        "spawn_interval_min": 20000,  # 20 seconds min
        "spawn_interval_max": 35000,  # 35 seconds max
        "spawn_chance": 0.02,         # 2% chance
        "lifetime": 18000,            # 18 seconds lifetime
        "warning_time": 5000,         # 5 seconds warning
        "fade_time": 2000,            # 2 seconds fade
        "cooldown_after_pickup": 15000  # 15 seconds cooldown
    },
    "levels": {
        "max_level": 5,  # Maximum level available
        "obstacle_count": [1, 2, 4, 6, 8],
        "speed_multiplier": [1.0, 1.2, 1.5, 1.8, 2.0],
        "special_food_chance": [0.1, 0.15, 0.2, 0.25, 0.3],
        "level_names": ["Easy", "Normal", "Hard", "Expert", "Master"]
    }
}

class Config:
    """Configuration manager for the game"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        # Validate config_file path to prevent path traversal
        if not self._is_safe_path(self.config_file):
            return DEFAULT_CONFIG.copy()
            
        if not os.path.exists(self.config_file):
            return DEFAULT_CONFIG.copy()
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate loaded config structure
            if not isinstance(config, dict):
                return DEFAULT_CONFIG.copy()
                
            # Merge with default config to ensure all keys exist
            try:
                return self._merge_configs(DEFAULT_CONFIG, config)
            except (TypeError, AttributeError, RecursionError):
                return DEFAULT_CONFIG.copy()
                
        except (json.JSONDecodeError, IOError, OSError, UnicodeDecodeError):
            return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        # Validate config_file path to prevent path traversal
        if not self._is_safe_path(self.config_file):
            return
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError:
            pass
    
    def _merge_configs(self, default, user):
        """Merge user config with default config"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key_path, default=None):
        """Get configuration value using dot notation (e.g., 'screen.width')"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """Set configuration value using dot notation"""
        try:
            keys = key_path.split('.')
            config = self.config
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            config[keys[-1]] = value
        except (AttributeError, TypeError, KeyError):
            pass  # Silently fail if config structure is invalid
    
    def get_color(self, color_name):
        """Get color tuple from config"""
        try:
            color = self.get(f"colors.{color_name}")
            if color and isinstance(color, (list, tuple)) and len(color) >= 3:
                return tuple(color[:3])  # Ensure RGB format
            return (255, 255, 255)  # Default white
        except (TypeError, ValueError):
            return (255, 255, 255)
    
    def get_screen_size(self):
        """Get fixed optimal screen dimensions"""
        return (1000, 700)
    
    def get_fps(self):
        """Get FPS setting"""
        return self.get("screen.fps")
    
    def get_block_size(self):
        """Get block size"""
        return self.get("game.block_size", 20)
    
    def _is_safe_path(self, path):
        """Check if path is safe (no path traversal)"""
        try:
            # Resolve path and check if it's within current directory
            resolved_path = os.path.abspath(path)
            current_dir = os.path.abspath('.')
            return resolved_path.startswith(current_dir)
        except Exception:
            return False

# Global config instance
config = Config()