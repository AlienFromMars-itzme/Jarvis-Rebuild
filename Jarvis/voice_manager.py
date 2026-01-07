"""Voice management for Jarvis AI Assistant."""

import pyttsx3
from typing import List, Dict, Optional
from .config import config


class VoiceManager:
    """Manages text-to-speech voices for Jarvis."""
    
    def __init__(self):
        """Initialize voice engine."""
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self._load_voice_config()
    
    def _load_voice_config(self):
        """Load voice configuration."""
        voice_id = config.get('voice.voice_id', 1)
        rate = config.get('voice.rate', 150)
        volume = config.get('voice.volume', 1.0)
        
        # Set voice
        if 0 <= voice_id < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_id].id)
        
        # Set rate and volume
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
    
    def speak(self, text: str) -> None:
        """Speak the given text."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error speaking: {e}")
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voices."""
        voice_list = []
        for i, voice in enumerate(self.voices):
            voice_info = {
                'id': i,
                'name': voice.name,
                'languages': voice.languages,
                'gender': 'male' if 'male' in voice.name.lower() else 'female'
            }
            voice_list.append(voice_info)
        return voice_list
    
    def list_voices(self) -> str:
        """List all available voices."""
        voices = self.get_available_voices()
        result = "Available voices:\n"
        for voice in voices:
            result += f"{voice['id']}: {voice['name']} ({voice['gender']})\n"
        return result
    
    def set_voice(self, voice_id: int) -> bool:
        """Set voice by ID."""
        try:
            if 0 <= voice_id < len(self.voices):
                self.engine.setProperty('voice', self.voices[voice_id].id)
                config.set('voice.voice_id', voice_id)
                return True
            return False
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False
    
    def set_voice_by_gender(self, gender: str) -> bool:
        """Set voice by gender (male/female)."""
        gender = gender.lower()
        for i, voice in enumerate(self.voices):
            voice_gender = 'male' if 'male' in voice.name.lower() else 'female'
            if voice_gender == gender:
                return self.set_voice(i)
        return False
    
    def cycle_voice(self, gender: Optional[str] = None) -> int:
        """Cycle to next voice, optionally filtering by gender."""
        current_voice_id = config.get('voice.voice_id', 0)
        voices = self.get_available_voices()
        
        if gender:
            gender = gender.lower()
            # Filter voices by gender
            filtered_voices = [v for v in voices if v['gender'] == gender]
            if not filtered_voices:
                return current_voice_id
            
            # Find current index in filtered list
            current_idx = 0
            for i, v in enumerate(filtered_voices):
                if v['id'] == current_voice_id:
                    current_idx = i
                    break
            
            # Get next voice
            next_idx = (current_idx + 1) % len(filtered_voices)
            next_voice_id = filtered_voices[next_idx]['id']
        else:
            # Cycle through all voices
            next_voice_id = (current_voice_id + 1) % len(voices)
        
        self.set_voice(next_voice_id)
        return next_voice_id
    
    def set_rate(self, rate: int) -> bool:
        """Set speech rate."""
        try:
            self.engine.setProperty('rate', rate)
            config.set('voice.rate', rate)
            return True
        except Exception as e:
            print(f"Error setting rate: {e}")
            return False
    
    def adjust_rate(self, adjustment: int) -> int:
        """Adjust speech rate by given amount."""
        current_rate = config.get('voice.rate', 150)
        new_rate = max(50, min(300, current_rate + adjustment))
        self.set_rate(new_rate)
        return new_rate
    
    def set_volume(self, volume: float) -> bool:
        """Set volume (0.0 to 1.0)."""
        try:
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
            config.set('voice.volume', volume)
            return True
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False
    
    def adjust_volume(self, adjustment: float) -> float:
        """Adjust volume by given amount."""
        current_volume = config.get('voice.volume', 1.0)
        new_volume = max(0.0, min(1.0, current_volume + adjustment))
        self.set_volume(new_volume)
        return new_volume
    
    def get_current_voice_info(self) -> Dict[str, any]:
        """Get information about current voice."""
        voice_id = config.get('voice.voice_id', 0)
        if 0 <= voice_id < len(self.voices):
            voice = self.voices[voice_id]
            return {
                'id': voice_id,
                'name': voice.name,
                'languages': voice.languages,
                'rate': config.get('voice.rate', 150),
                'volume': config.get('voice.volume', 1.0)
            }
        return {}


# Global voice manager instance
voice_manager = VoiceManager()
