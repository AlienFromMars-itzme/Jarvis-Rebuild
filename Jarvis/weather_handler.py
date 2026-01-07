"""Weather module for Jarvis AI Assistant."""

import requests
from typing import Optional, Dict
from .config import config


class WeatherHandler:
    """Handles weather information using OpenWeatherMap API."""
    
    def __init__(self):
        """Initialize weather handler."""
        self.api_key = config.get_api_key('openweather')
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """Get current weather for a city."""
        if not self.api_key:
            return None
        
        try:
            endpoint = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'temperature': data.get('main', {}).get('temp'),
                'feels_like': data.get('main', {}).get('feels_like'),
                'humidity': data.get('main', {}).get('humidity'),
                'pressure': data.get('main', {}).get('pressure'),
                'description': data.get('weather', [{}])[0].get('description'),
                'wind_speed': data.get('wind', {}).get('speed'),
                'clouds': data.get('clouds', {}).get('all')
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def get_forecast(self, city: str, days: int = 3, units: str = "metric") -> Optional[Dict]:
        """Get weather forecast for a city."""
        if not self.api_key:
            return None
        
        try:
            endpoint = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units,
                'cnt': days * 8  # API returns data every 3 hours
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            forecasts = []
            for item in data.get('list', [])[:days * 8:8]:  # Take one per day
                forecasts.append({
                    'date': item.get('dt_txt'),
                    'temperature': item.get('main', {}).get('temp'),
                    'description': item.get('weather', [{}])[0].get('description'),
                    'humidity': item.get('main', {}).get('humidity')
                })
            
            return {
                'city': data.get('city', {}).get('name'),
                'country': data.get('city', {}).get('country'),
                'forecasts': forecasts
            }
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    def format_weather(self, weather: Dict) -> str:
        """Format weather data for speech."""
        if not weather:
            return "Unable to fetch weather information."
        
        city = weather.get('city', 'Unknown')
        temp = weather.get('temperature', 0)
        description = weather.get('description', 'unknown')
        humidity = weather.get('humidity', 0)
        
        units = config.get('preferences.temperature_unit', 'celsius')
        temp_unit = '°C' if units == 'celsius' else '°F'
        
        result = f"The weather in {city} is {description}. "
        result += f"Temperature is {temp:.1f}{temp_unit} "
        result += f"with {humidity}% humidity."
        
        return result
    
    def is_available(self) -> bool:
        """Check if weather API is available."""
        return bool(self.api_key)


# Global weather handler instance
weather_handler = WeatherHandler()
