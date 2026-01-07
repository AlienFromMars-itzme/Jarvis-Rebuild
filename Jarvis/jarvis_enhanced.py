"""
Jarvis AI Assistant - Enhanced Version
A comprehensive AI voice assistant with 15+ advanced features.
"""

import os
import sys
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import random
import pyautogui
import pyjokes
import re

# Import new modules
try:
    from config import config
    from voice_manager import voice_manager
    from ai_engine import ai_engine
    from system_control import system_control
    from whatsapp_handler import whatsapp_handler
    from news_handler import news_handler
    from reminder_manager import init_reminder_manager
    from utils import (
        get_greeting, format_time, format_date,
        extract_number, extract_percentage,
        ColorText, sanitize_filename
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all modules are in the Jarvis directory.")
    sys.exit(1)


class JarvisAssistant:
    """Main Jarvis AI Assistant class."""
    
    def __init__(self):
        """Initialize Jarvis assistant."""
        self.recognizer = sr.Recognizer()
        self.assistant_name = config.get('assistant_name', 'Jarvis')
        self.running = True
        
        # Initialize reminder manager with voice callback
        self.reminder_manager = init_reminder_manager(voice_callback=self.speak)
        
        ColorText.info(f"Initializing {self.assistant_name}...")
        self.wishme()
    
    def speak(self, text: str) -> None:
        """Speak the given text."""
        print(f"🤖 {self.assistant_name}: {text}")
        voice_manager.speak(text)
    
    def wishme(self) -> None:
        """Greet the user based on time of day."""
        greeting = get_greeting()
        self.speak(f"Welcome back, sir! {greeting}!")
        self.speak(f"{self.assistant_name} at your service. How may I assist you today?")
    
    def take_command(self) -> str:
        """Take microphone input and return as text."""
        with sr.Microphone() as source:
            ColorText.info("Listening...")
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                ColorText.info("Recognizing...")
                
                query = self.recognizer.recognize_google(audio, language="en-in")
                ColorText.print_colored(f"👤 You: {query}", ColorText.CYAN)
                return query.lower()
            
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                ColorText.error("Speech recognition service unavailable")
                return ""
            except Exception as e:
                ColorText.error(f"Error: {e}")
                return ""
    
    def get_ai_response(self, query: str) -> bool:
        """Get AI-powered response if available."""
        if ai_engine.is_available():
            response = ai_engine.get_ai_response(query)
            if response:
                self.speak(response)
                return True
        return False
    
    def handle_time(self):
        """Tell current time."""
        current_time = format_time(config.get('preferences.time_format', '12h'))
        self.speak(f"The current time is {current_time}")
    
    def handle_date(self):
        """Tell current date."""
        current_date = format_date()
        self.speak(f"The current date is {current_date}")
    
    def handle_wikipedia(self, query: str):
        """Search Wikipedia."""
        search_query = query.replace("wikipedia", "").replace("search", "").strip()
        if not search_query:
            self.speak("What would you like to search on Wikipedia?")
            search_query = self.take_command()
        
        if search_query:
            try:
                self.speak("Searching Wikipedia...")
                result = wikipedia.summary(search_query, sentences=2)
                self.speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                self.speak("Multiple results found. Please be more specific.")
            except Exception:
                self.speak("I couldn't find anything on Wikipedia.")
    
    def handle_web_search(self, query: str):
        """Perform web search."""
        search_query = query.replace("google", "").replace("search", "").strip()
        if search_query:
            wb.open(f"https://www.google.com/search?q={search_query}")
            self.speak(f"Here are the results for {search_query}")
        else:
            self.speak("What would you like to search?")
    
    def handle_music(self, query: str):
        """Play music."""
        song_name = query.replace("play", "").replace("music", "").replace("song", "").strip()
        
        if "youtube" in query or not song_name:
            if song_name:
                import pywhatkit
                try:
                    self.speak(f"Playing {song_name} on YouTube")
                    pywhatkit.playonyt(song_name)
                except Exception as e:
                    ColorText.error(f"Error playing on YouTube: {e}")
        else:
            # Play local music
            song_dir = os.path.expanduser("~\\Music")
            if os.path.exists(song_dir):
                songs = os.listdir(song_dir)
                if song_name:
                    songs = [s for s in songs if song_name.lower() in s.lower()]
                if songs:
                    song = random.choice(songs)
                    os.startfile(os.path.join(song_dir, song))
                    self.speak(f"Playing {song}")
                else:
                    self.speak("No song found")
            else:
                self.speak("Music directory not found")
    
    def handle_screenshot(self, query: str):
        """Take a screenshot."""
        # Extract filename if provided
        filename = "screenshot.png"
        if "as" in query or "name" in query:
            parts = query.split("as" if "as" in query else "name")
            if len(parts) > 1:
                filename = sanitize_filename(parts[1].strip()) + ".png"
        
        try:
            img = pyautogui.screenshot()
            img_path = os.path.expanduser(f"~\\Pictures\\{filename}")
            img.save(img_path)
            self.speak(f"Screenshot saved as {filename}")
            ColorText.success(f"Screenshot saved: {img_path}")
        except Exception as e:
            ColorText.error(f"Error taking screenshot: {e}")
            self.speak("Failed to take screenshot")
    
    def handle_joke(self):
        """Tell a joke."""
        joke = pyjokes.get_joke()
        self.speak(joke)
    
    def handle_battery(self):
        """Check battery status."""
        battery = system_control.get_battery_status()
        if battery:
            percentage = battery['percentage']
            charging = "charging" if battery['charging'] else "not charging"
            self.speak(f"Battery is at {percentage}% and {charging}")
            
            if battery['time_remaining']:
                hours = battery['time_remaining'] // 3600
                minutes = (battery['time_remaining'] % 3600) // 60
                if hours > 0:
                    self.speak(f"Approximately {hours} hours and {minutes} minutes remaining")
                else:
                    self.speak(f"Approximately {minutes} minutes remaining")
        else:
            self.speak("Unable to get battery information")
    
    def handle_cpu(self):
        """Check CPU usage."""
        cpu = system_control.get_cpu_usage()
        if cpu:
            self.speak(f"CPU usage is at {cpu['total']}%")
            self.speak(f"Your system has {cpu['cores']} cores and {cpu['threads']} threads")
    
    def handle_memory(self):
        """Check RAM usage."""
        memory = system_control.get_memory_usage()
        if memory:
            self.speak(f"RAM usage is at {memory['percentage']}%")
            self.speak(f"{memory['used']} used out of {memory['total']} total memory")
    
    def handle_internet(self):
        """Check internet connection."""
        if system_control.check_internet_connection():
            self.speak("Internet connection is active")
        else:
            self.speak("No internet connection detected")
    
    def handle_volume(self, query: str):
        """Control system volume."""
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            
            if "mute" in query:
                volume.SetMute(1, None)
                self.speak("Volume muted")
            elif "unmute" in query:
                volume.SetMute(0, None)
                self.speak("Volume unmuted")
            elif "set" in query or "to" in query:
                level = extract_percentage(query)
                if level is not None:
                    volume.SetMasterVolumeLevelScalar(level / 100, None)
                    self.speak(f"Volume set to {level}%")
            elif "increase" in query or "up" in query:
                current = volume.GetMasterVolumeLevelScalar() * 100
                new_level = min(100, current + 10)
                volume.SetMasterVolumeLevelScalar(new_level / 100, None)
                self.speak(f"Volume increased to {int(new_level)}%")
            elif "decrease" in query or "down" in query:
                current = volume.GetMasterVolumeLevelScalar() * 100
                new_level = max(0, current - 10)
                volume.SetMasterVolumeLevelScalar(new_level / 100, None)
                self.speak(f"Volume decreased to {int(new_level)}%")
            else:
                current = int(volume.GetMasterVolumeLevelScalar() * 100)
                self.speak(f"Current volume is {current}%")
        except Exception as e:
            ColorText.error(f"Error controlling volume: {e}")
            self.speak("Unable to control volume")
    
    def handle_brightness(self, query: str):
        """Control screen brightness."""
        try:
            import screen_brightness_control as sbc
            
            if "set" in query or "to" in query:
                level = extract_percentage(query)
                if level is not None:
                    sbc.set_brightness(level)
                    self.speak(f"Brightness set to {level}%")
            elif "increase" in query or "up" in query:
                current = sbc.get_brightness()[0]
                new_level = min(100, current + 10)
                sbc.set_brightness(new_level)
                self.speak(f"Brightness increased to {int(new_level)}%")
            elif "decrease" in query or "down" in query:
                current = sbc.get_brightness()[0]
                new_level = max(0, current - 10)
                sbc.set_brightness(new_level)
                self.speak(f"Brightness decreased to {int(new_level)}%")
            else:
                current = int(sbc.get_brightness()[0])
                self.speak(f"Current brightness is {current}%")
        except Exception as e:
            ColorText.error(f"Error controlling brightness: {e}")
            self.speak("Unable to control brightness")
    
    def handle_open_app(self, query: str):
        """Open an application."""
        app_name = query.replace("open", "").replace("launch", "").replace("start", "").strip()
        if app_name:
            if system_control.open_application(app_name):
                self.speak(f"Opening {app_name}")
            else:
                self.speak(f"Unable to open {app_name}")
    
    def handle_close_app(self, query: str):
        """Close an application."""
        app_name = query.replace("close", "").replace("exit", "").replace("quit", "").strip()
        if app_name:
            if system_control.close_application(app_name):
                self.speak(f"Closing {app_name}")
            else:
                self.speak(f"Unable to close {app_name}")
    
    def handle_news(self, query: str):
        """Get news updates."""
        if not news_handler.is_available():
            self.speak("News API key not configured. Please add your NewsAPI key to the .env file")
            return
        
        category = None
        if "technology" in query:
            category = "technology"
        elif "sports" in query:
            category = "sports"
        elif "business" in query:
            category = "business"
        elif "health" in query:
            category = "health"
        elif "science" in query:
            category = "science"
        elif "entertainment" in query:
            category = "entertainment"
        
        self.speak("Fetching latest news...")
        articles = news_handler.get_top_headlines(category=category, max_results=5)
        
        if articles:
            news_text = news_handler.format_news(articles, max_articles=3)
            self.speak("Here are the top headlines:")
            self.speak(news_text)
        else:
            self.speak("Unable to fetch news at the moment")
    
    def handle_reminder(self, query: str):
        """Set a reminder."""
        # Extract reminder message and time
        if "to" in query:
            parts = query.split("to", 1)
            if len(parts) > 1:
                remainder = parts[1].strip()
                
                # Try to split by time indicators
                time_indicators = ["at", "in", "tomorrow"]
                message = remainder
                time_str = ""
                
                for indicator in time_indicators:
                    if indicator in remainder:
                        parts = remainder.split(indicator, 1)
                        message = parts[0].strip()
                        time_str = indicator + " " + parts[1].strip()
                        break
                
                if not time_str:
                    # Default to 1 hour if no time specified
                    time_str = "in 1 hour"
                
                reminder_time = self.reminder_manager.parse_reminder_time(time_str)
                if reminder_time:
                    reminder_id = self.reminder_manager.add_reminder(message, reminder_time)
                    if reminder_id:
                        time_desc = reminder_time.strftime("%I:%M %p on %B %d")
                        self.speak(f"Reminder set: {message} at {time_desc}")
                        ColorText.success(f"Reminder created: {reminder_id}")
                    else:
                        self.speak("Failed to set reminder")
                else:
                    self.speak("I couldn't understand the time. Please try again")
        else:
            self.speak("Please tell me what you want to be reminded about and when")
    
    def handle_list_reminders(self):
        """List all active reminders."""
        reminders = self.reminder_manager.list_reminders(active_only=True)
        if reminders:
            self.speak(f"You have {len(reminders)} active reminders:")
            for i, reminder in enumerate(reminders[:5], 1):
                time = datetime.datetime.fromisoformat(reminder['time'])
                self.speak(f"{i}. {reminder['message']} at {time.strftime('%I:%M %p')}")
        else:
            self.speak("You have no active reminders")
    
    def handle_voice_change(self, query: str):
        """Change voice settings."""
        if "male" in query:
            voice_manager.set_voice_by_gender("male")
            self.speak("Voice changed to male")
        elif "female" in query:
            voice_manager.set_voice_by_gender("female")
            self.speak("Voice changed to female")
        elif "next" in query or "change" in query:
            voice_id = voice_manager.cycle_voice()
            voice_info = voice_manager.get_current_voice_info()
            self.speak(f"Voice changed to {voice_info.get('name', 'new voice')}")
        else:
            voices = voice_manager.get_available_voices()
            self.speak(f"There are {len(voices)} voices available. Say 'male voice' or 'female voice' to change")
    
    def handle_shutdown(self, query: str):
        """Shutdown the system."""
        delay = extract_number(query)
        if delay:
            self.speak(f"Shutting down in {delay} minutes")
            system_control.shutdown(delay * 60)
        else:
            self.speak("Shutting down now. Goodbye!")
            system_control.shutdown(5)
        self.running = False
    
    def handle_restart(self, query: str):
        """Restart the system."""
        delay = extract_number(query)
        if delay:
            self.speak(f"Restarting in {delay} minutes")
            system_control.restart(delay * 60)
        else:
            self.speak("Restarting now. See you soon!")
            system_control.restart(5)
        self.running = False
    
    def handle_sleep(self):
        """Put system to sleep."""
        self.speak("Putting system to sleep. Goodbye!")
        system_control.sleep()
        self.running = False
    
    def handle_lock(self):
        """Lock the screen."""
        self.speak("Locking screen")
        system_control.lock_screen()
    
    def handle_website(self, query: str):
        """Open a website."""
        sites = {
            "youtube": "youtube.com",
            "google": "google.com",
            "github": "github.com",
            "stackoverflow": "stackoverflow.com",
            "twitter": "twitter.com",
            "facebook": "facebook.com",
            "instagram": "instagram.com",
            "linkedin": "linkedin.com",
            "reddit": "reddit.com",
            "amazon": "amazon.com"
        }
        
        for site, url in sites.items():
            if site in query:
                wb.open(f"https://{url}")
                self.speak(f"Opening {site}")
                return
        
        self.speak("Which website would you like to open?")
    
    def process_command(self, query: str):
        """Process voice command."""
        if not query:
            return
        
        # Time and date
        if "time" in query:
            self.handle_time()
        
        elif "date" in query:
            self.handle_date()
        
        # Web and search
        elif "wikipedia" in query:
            self.handle_wikipedia(query)
        
        elif "google" in query or "search" in query:
            self.handle_web_search(query)
        
        elif "open youtube" in query or "open google" in query or "open" in query and any(site in query for site in ["youtube", "google", "github", "facebook", "twitter"]):
            self.handle_website(query)
        
        # Music and entertainment
        elif "play" in query and ("music" in query or "song" in query or "youtube" in query):
            self.handle_music(query)
        
        elif "joke" in query:
            self.handle_joke()
        
        # System monitoring
        elif "battery" in query:
            self.handle_battery()
        
        elif "cpu" in query:
            self.handle_cpu()
        
        elif "memory" in query or "ram" in query:
            self.handle_memory()
        
        elif "internet" in query:
            self.handle_internet()
        
        # System control
        elif "volume" in query:
            self.handle_volume(query)
        
        elif "brightness" in query:
            self.handle_brightness(query)
        
        elif ("open" in query or "launch" in query or "start" in query) and not any(x in query for x in ["youtube", "google", "website"]):
            self.handle_open_app(query)
        
        elif "close" in query or "exit" in query:
            self.handle_close_app(query)
        
        # News
        elif "news" in query:
            self.handle_news(query)
        
        # Reminders
        elif "remind me" in query or "reminder" in query or "set reminder" in query:
            self.handle_reminder(query)
        
        elif "list reminder" in query or "my reminders" in query:
            self.handle_list_reminders()
        
        # Voice control
        elif "change voice" in query or "change your voice" in query:
            self.handle_voice_change(query)
        
        # Screenshots
        elif "screenshot" in query or "screen shot" in query:
            self.handle_screenshot(query)
        
        # Power control
        elif "shutdown" in query:
            self.handle_shutdown(query)
        
        elif "restart" in query:
            self.handle_restart(query)
        
        elif "sleep" in query and ("system" in query or "computer" in query):
            self.handle_sleep()
        
        elif "lock" in query:
            self.handle_lock()
        
        # Exit commands
        elif any(word in query for word in ["offline", "exit", "quit", "goodbye", "bye"]):
            self.speak("Going offline. Have a great day!")
            self.running = False
        
        # Try AI response for unmatched queries
        else:
            if not self.get_ai_response(query):
                self.speak("I'm not sure how to help with that. Please try rephrasing your request.")
    
    def run(self):
        """Main run loop."""
        try:
            while self.running:
                query = self.take_command()
                if query:
                    self.process_command(query)
        
        except KeyboardInterrupt:
            ColorText.warning("\nKeyboard interrupt received")
            self.speak("Shutting down")
        
        finally:
            # Cleanup
            if self.reminder_manager:
                self.reminder_manager.shutdown()
            ColorText.success("Goodbye!")


def main():
    """Main entry point."""
    try:
        # Print banner
        print("\n" + "=" * 60)
        ColorText.print_colored("    🤖 JARVIS AI ASSISTANT - Enhanced Version 2.0", ColorText.BOLD + ColorText.CYAN)
        print("=" * 60 + "\n")
        
        # Initialize and run assistant
        assistant = JarvisAssistant()
        assistant.run()
    
    except Exception as e:
        ColorText.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
