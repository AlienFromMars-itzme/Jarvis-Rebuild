"""
Jarvis AI Assistant - Enhanced Version
A comprehensive AI voice assistant with advanced features.
"""

__version__ = "2.0.0"
__author__ = "Kishan Kumar Rai (Enhanced)"
__description__ = "Advanced AI Voice Assistant with 15+ features"

# Import main components for easy access
try:
    from .config import config
    from .voice_manager import voice_manager
    from .ai_engine import ai_engine
    from .system_control import system_control
    from .whatsapp_handler import whatsapp_handler
    from .news_handler import news_handler
    from .reminder_manager import reminder_manager, init_reminder_manager
    from .utils import ColorText, get_greeting, format_time, format_date
except ImportError:
    # Allow imports to fail during setup
    pass

__all__ = [
    'config',
    'voice_manager',
    'ai_engine',
    'system_control',
    'whatsapp_handler',
    'news_handler',
    'reminder_manager',
    'init_reminder_manager',
    'ColorText',
    'get_greeting',
    'format_time',
    'format_date'
]
