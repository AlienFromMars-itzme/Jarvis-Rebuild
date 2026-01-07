"""News fetching for Jarvis AI Assistant."""

import requests
from typing import List, Dict, Optional
from .config import config


class NewsHandler:
    """Handles news fetching from NewsAPI."""
    
    def __init__(self):
        """Initialize news handler."""
        self.api_key = config.get_api_key('news')
        self.base_url = "https://newsapi.org/v2"
    
    def get_top_headlines(self, category: Optional[str] = None, country: str = "us", max_results: int = 5) -> List[Dict]:
        """Get top headlines."""
        if not self.api_key:
            return []
        
        try:
            endpoint = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.api_key,
                'country': country,
                'pageSize': max_results
            }
            
            if category:
                params['category'] = category
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'ok':
                return data.get('articles', [])
            return []
        except Exception as e:
            print(f"Error fetching top headlines: {e}")
            return []
    
    def get_news_by_query(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for news by query."""
        if not self.api_key:
            return []
        
        try:
            endpoint = f"{self.base_url}/everything"
            params = {
                'apiKey': self.api_key,
                'q': query,
                'pageSize': max_results,
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'ok':
                return data.get('articles', [])
            return []
        except Exception as e:
            print(f"Error searching news: {e}")
            return []
    
    def get_news_by_source(self, source: str, max_results: int = 5) -> List[Dict]:
        """Get news from a specific source."""
        if not self.api_key:
            return []
        
        try:
            endpoint = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.api_key,
                'sources': source,
                'pageSize': max_results
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'ok':
                return data.get('articles', [])
            return []
        except Exception as e:
            print(f"Error fetching news from source: {e}")
            return []
    
    def format_news(self, articles: List[Dict], max_articles: int = 5) -> str:
        """Format news articles for speech."""
        if not articles:
            return "No news articles found."
        
        result = ""
        for i, article in enumerate(articles[:max_articles], 1):
            title = article.get('title', 'No title')
            description = article.get('description', '')
            result += f"{i}. {title}. "
            if description and len(description) < 200:
                result += f"{description} "
        
        return result.strip()
    
    def get_categories(self) -> List[str]:
        """Get available news categories."""
        return ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    
    def is_available(self) -> bool:
        """Check if news API is available."""
        return bool(self.api_key)


# Global news handler instance
news_handler = NewsHandler()
