"""Configuration management for Jarvis AI Assistant."""

import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Manages configuration settings for Jarvis."""
    
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "data", "config.json")
    
    DEFAULT_CONFIG = {
        "assistant_name": "Jarvis",
        "voice": {
            "voice_id": 1,
            "rate": 150,
            "volume": 1.0,
            "language": "en"
        },
        "features": {
            "ai_enabled": True,
            "wake_word_enabled": False,
            "conversation_mode": False,
            "offline_mode": False
        },
        "ai_settings": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 150,
            "temperature": 0.7
        },
        "preferences": {
            "news_category": "technology",
            "music_service": "youtube",
            "temperature_unit": "celsius",
            "time_format": "12h"
        },
        "api_keys": {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
            "news_api_key": os.getenv("NEWS_API_KEY", ""),
            "openweather_api_key": os.getenv("OPENWEATHER_API_KEY", ""),
            "spotify_client_id": os.getenv("SPOTIFY_CLIENT_ID", ""),
            "spotify_client_secret": os.getenv("SPOTIFY_CLIENT_SECRET", "")
        }
    }
    
    def __init__(self):
        """Initialize configuration."""
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                # Merge with default config to ensure all keys exist
                return self._merge_configs(self.DEFAULT_CONFIG.copy(), config)
            else:
                # Create data directory if it doesn't exist
                os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
                # Save default config
                self.save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Merge user config with default config."""
        for key, value in default.items():
            if key in user:
                if isinstance(value, dict) and isinstance(user[key], dict):
                    default[key] = self._merge_configs(value, user[key])
                else:
                    default[key] = user[key]
        return default
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """Save configuration to file."""
        try:
            if config is None:
                config = self.config
            
            # Don't save API keys to config file (use .env instead)
            config_to_save = config.copy()
            if "api_keys" in config_to_save:
                config_to_save["api_keys"] = {key: "" for key in config_to_save["api_keys"]}
            
            os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_to_save, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default=None) -> Any:
        """Get a configuration value."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Set a configuration value."""
        try:
            keys = key.split('.')
            config = self.config
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            config[keys[-1]] = value
            return self.save_config()
        except Exception as e:
            print(f"Error setting config: {e}")
            return False
    
    def get_api_key(self, service: str) -> str:
        """Get API key for a service."""
        # Try environment variable first
        env_key = f"{service.upper()}_API_KEY"
        api_key = os.getenv(env_key)
        if api_key:
            return api_key
        # Fall back to config
        return self.config.get("api_keys", {}).get(f"{service}_api_key", "")
    
    def has_api_key(self, service: str) -> bool:
        """Check if API key exists for a service."""
        return bool(self.get_api_key(service))


# Global configuration instance
config = Config()
