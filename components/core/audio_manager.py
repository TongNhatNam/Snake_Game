"""
Audio management system for Snake Game
Handles background music, sound effects, and volume control
"""

import pygame
import os
from .config import config

class AudioManager:
    """Manages all game audio including music and sound effects"""
    
    def __init__(self):
        """Initialize audio manager"""
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return
        
        self.enabled = True
        self.sounds = {}
        self.music_enabled = config.get("audio.music_enabled", True)
        self.sfx_enabled = config.get("audio.sfx_enabled", True)
        self.master_volume = config.get("audio.master_volume", 1.0)
        self.music_volume = config.get("audio.music_volume", 0.7)
        self.sfx_volume = config.get("audio.sfx_volume", 0.8)
        
        self.current_music = None
        self.music_playing = False
        
        # Load all sounds
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound files from assets/sounds directory"""
        sounds_dir = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sounds")
        
        # Sound file mapping - supports both WAV and MP3
        sound_files = {
            "eat": "eat_sound.wav",
            "powerup": "powerup_sound.wav",
            "death": "death_sound.wav",
            "level_complete": "level_complete.wav",
            "menu_select": "menu_select.wav",
            "menu_back": "menu_back.wav",
            "lose": "lose.mp3"  # Game over/lose sound
        }
        
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(sounds_dir, filename)
            try:
                if os.path.exists(filepath):
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    # Set initial volume
                    self.sounds[sound_name].set_volume(self.sfx_volume * self.master_volume)
            except pygame.error:
                # Silently fail if sound file can't be loaded
                pass
    
    def play_music(self, music_name, loops=-1):
        """
        Play background music
        
        Args:
            music_name: Name of music file (without extension) in assets/sounds
            loops: Number of loops (-1 for infinite)
        """
        if not self.enabled or not self.music_enabled:
            return
        
        sounds_dir = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sounds")
        
        # Try both .mp3 and .wav formats
        for extension in [".mp3", ".wav"]:
            music_path = os.path.join(sounds_dir, f"{music_name}{extension}")
            
            try:
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                    pygame.mixer.music.play(loops)
                    self.current_music = music_name
                    self.music_playing = True
                    return
            except pygame.error:
                pass
    
    def stop_music(self):
        """Stop background music"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except pygame.error:
            pass
    
    def pause_music(self):
        """Pause background music"""
        if not self.enabled or not self.music_playing:
            return
        
        try:
            pygame.mixer.music.pause()
        except pygame.error:
            pass
    
    def unpause_music(self):
        """Resume background music"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.music.unpause()
            self.music_playing = True
        except pygame.error:
            pass
    
    def play_sound(self, sound_name):
        """
        Play a sound effect
        
        Args:
            sound_name: Name of sound to play (must be pre-loaded)
        """
        if not self.enabled or not self.sfx_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error:
                pass
    
    def set_master_volume(self, volume):
        """
        Set master volume (0.0 to 1.0)
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        if not self.enabled:
            return
        
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
        config.set("audio.master_volume", self.master_volume)
    
    def set_music_volume(self, volume):
        """
        Set music volume (0.0 to 1.0)
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        if not self.enabled:
            return
        
        self.music_volume = max(0.0, min(1.0, volume))
        self._update_music_volume()
        config.set("audio.music_volume", self.music_volume)
    
    def set_sfx_volume(self, volume):
        """
        Set sound effects volume (0.0 to 1.0)
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        if not self.enabled:
            return
        
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_sfx_volumes()
        config.set("audio.sfx_volume", self.sfx_volume)
    
    def set_music_enabled(self, enabled):
        """Enable or disable music"""
        self.music_enabled = enabled
        if not enabled:
            self.stop_music()
        config.set("audio.music_enabled", enabled)
    
    def set_sfx_enabled(self, enabled):
        """Enable or disable sound effects"""
        self.sfx_enabled = enabled
        config.set("audio.sfx_enabled", enabled)
    
    def _update_all_volumes(self):
        """Update all sound volumes"""
        self._update_music_volume()
        self._update_sfx_volumes()
    
    def _update_music_volume(self):
        """Update music volume based on master and music volume"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        except pygame.error:
            pass
    
    def _update_sfx_volumes(self):
        """Update all sound effects volumes"""
        if not self.enabled:
            return
        
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.sfx_volume * self.master_volume)
            except (pygame.error, AttributeError):
                pass
    
    def get_master_volume(self):
        """Get current master volume"""
        return self.master_volume
    
    def get_music_volume(self):
        """Get current music volume"""
        return self.music_volume
    
    def get_sfx_volume(self):
        """Get current sound effects volume"""
        return self.sfx_volume
    
    def is_music_enabled(self):
        """Check if music is enabled"""
        return self.music_enabled
    
    def is_sfx_enabled(self):
        """Check if sound effects are enabled"""
        return self.sfx_enabled

# Global audio manager instance
audio_manager = AudioManager()
