"""WhatsApp automation for Jarvis AI Assistant."""

import pywhatkit
from datetime import datetime, timedelta
from typing import Optional
from .utils import extract_number


class WhatsAppHandler:
    """Handles WhatsApp automation."""
    
    def __init__(self):
        """Initialize WhatsApp handler."""
        pass
    
    def send_message(self, phone_number: str, message: str, hour: Optional[int] = None, minute: Optional[int] = None) -> bool:
        """Send a WhatsApp message."""
        try:
            if hour is None or minute is None:
                # Send immediately (after 2 minutes)
                now = datetime.now() + timedelta(minutes=2)
                hour = now.hour
                minute = now.minute
            
            # Ensure phone number has country code
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            pywhatkit.sendwhatmsg(phone_number, message, hour, minute, wait_time=15, tab_close=True)
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
    
    def send_message_instantly(self, phone_number: str, message: str) -> bool:
        """Send a WhatsApp message instantly."""
        try:
            # Ensure phone number has country code
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True)
            return True
        except Exception as e:
            print(f"Error sending instant WhatsApp message: {e}")
            return False
    
    def send_to_group(self, group_id: str, message: str, hour: Optional[int] = None, minute: Optional[int] = None) -> bool:
        """Send a message to a WhatsApp group."""
        try:
            if hour is None or minute is None:
                # Send immediately (after 2 minutes)
                now = datetime.now() + timedelta(minutes=2)
                hour = now.hour
                minute = now.minute
            
            pywhatkit.sendwhatmsg_to_group(group_id, message, hour, minute, wait_time=15, tab_close=True)
            return True
        except Exception as e:
            print(f"Error sending WhatsApp group message: {e}")
            return False
    
    def open_chat(self, phone_number: str) -> bool:
        """Open WhatsApp chat with a contact."""
        try:
            # Ensure phone number has country code
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            import webbrowser
            webbrowser.open(f"https://web.whatsapp.com/send?phone={phone_number}")
            return True
        except Exception as e:
            print(f"Error opening WhatsApp chat: {e}")
            return False


# Global WhatsApp handler instance
whatsapp_handler = WhatsAppHandler()
