"""AI engine for intelligent conversations using OpenAI GPT or Google Gemini."""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from .config import config
from .utils import load_json, save_json


class AIEngine:
    """Manages AI-powered conversations."""
    
    HISTORY_FILE = os.path.join(os.path.dirname(__file__), "data", "conversation_history.json")
    MAX_HISTORY = 10  # Keep last 10 exchanges for context
    
    def __init__(self):
        """Initialize AI engine."""
        self.conversation_history = self._load_history()
        self.ai_client = None
        self.ai_type = None
        self._initialize_ai()
    
    def _initialize_ai(self):
        """Initialize AI client based on available API keys."""
        # Try OpenAI first
        if config.has_api_key('openai'):
            try:
                import openai
                openai.api_key = config.get_api_key('openai')
                self.ai_client = openai
                self.ai_type = 'openai'
                return
            except ImportError:
                print("OpenAI library not installed. Install with: pip install openai")
        
        # Try Google Gemini
        if config.has_api_key('gemini'):
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.get_api_key('gemini'))
                self.ai_client = genai.GenerativeModel('gemini-pro')
                self.ai_type = 'gemini'
                return
            except ImportError:
                print("Google Generative AI library not installed. Install with: pip install google-generativeai")
        
        print("No AI API keys configured. AI features will be limited.")
    
    def _load_history(self) -> List[Dict[str, str]]:
        """Load conversation history."""
        history = load_json(self.HISTORY_FILE, [])
        return history[-self.MAX_HISTORY:] if history else []
    
    def _save_history(self):
        """Save conversation history."""
        save_json(self.HISTORY_FILE, self.conversation_history)
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        # Keep only last MAX_HISTORY exchanges
        if len(self.conversation_history) > self.MAX_HISTORY * 2:
            self.conversation_history = self.conversation_history[-self.MAX_HISTORY * 2:]
        self._save_history()
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self._save_history()
    
    def get_ai_response(self, user_input: str, use_history: bool = True) -> Optional[str]:
        """Get AI-generated response."""
        if not self.ai_client or not config.get('features.ai_enabled', True):
            return None
        
        try:
            if self.ai_type == 'openai':
                return self._get_openai_response(user_input, use_history)
            elif self.ai_type == 'gemini':
                return self._get_gemini_response(user_input, use_history)
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return None
    
    def _get_openai_response(self, user_input: str, use_history: bool) -> Optional[str]:
        """Get response from OpenAI GPT."""
        try:
            messages = []
            
            # Add system message
            messages.append({
                'role': 'system',
                'content': 'You are Jarvis, a helpful and friendly AI voice assistant. Provide concise, natural responses suitable for voice interaction. Keep responses brief (2-3 sentences) unless more detail is requested.'
            })
            
            # Add conversation history if enabled
            if use_history:
                for msg in self.conversation_history:
                    if msg['role'] in ['user', 'assistant']:
                        messages.append({
                            'role': msg['role'],
                            'content': msg['content']
                        })
            
            # Add current user input
            messages.append({
                'role': 'user',
                'content': user_input
            })
            
            # Get response from OpenAI
            response = self.ai_client.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Add to history
            self.add_to_history('user', user_input)
            self.add_to_history('assistant', ai_response)
            
            return ai_response
        except Exception as e:
            print(f"OpenAI error: {e}")
            return None
    
    def _get_gemini_response(self, user_input: str, use_history: bool) -> Optional[str]:
        """Get response from Google Gemini."""
        try:
            # Build prompt with context
            prompt = "You are Jarvis, a helpful and friendly AI voice assistant. Provide concise, natural responses suitable for voice interaction. Keep responses brief (2-3 sentences) unless more detail is requested.\n\n"
            
            # Add conversation history if enabled
            if use_history:
                for msg in self.conversation_history:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    prompt += f"{role}: {msg['content']}\n"
            
            # Add current user input
            prompt += f"User: {user_input}\nAssistant:"
            
            # Get response from Gemini
            response = self.ai_client.generate_content(prompt)
            ai_response = response.text.strip()
            
            # Add to history
            self.add_to_history('user', user_input)
            self.add_to_history('assistant', ai_response)
            
            return ai_response
        except Exception as e:
            print(f"Gemini error: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if AI is available."""
        return self.ai_client is not None and config.get('features.ai_enabled', True)


# Global AI engine instance
ai_engine = AIEngine()
