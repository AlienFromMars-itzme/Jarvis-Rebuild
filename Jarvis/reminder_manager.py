"""Reminder and scheduling manager for Jarvis AI Assistant."""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from .utils import load_json, save_json


class ReminderManager:
    """Manages reminders and scheduled tasks."""
    
    REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "data", "reminders.json")
    
    def __init__(self, voice_callback=None):
        """Initialize reminder manager."""
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.voice_callback = voice_callback
        self.reminders = self._load_reminders()
        self._restore_reminders()
    
    def _load_reminders(self) -> List[Dict]:
        """Load reminders from file."""
        return load_json(self.REMINDERS_FILE, [])
    
    def _save_reminders(self):
        """Save reminders to file."""
        save_json(self.REMINDERS_FILE, self.reminders)
    
    def _restore_reminders(self):
        """Restore active reminders to scheduler."""
        for reminder in self.reminders:
            if reminder.get('active', True):
                try:
                    self._schedule_reminder(reminder)
                except Exception as e:
                    print(f"Error restoring reminder: {e}")
    
    def _schedule_reminder(self, reminder: Dict):
        """Schedule a reminder in the scheduler."""
        reminder_id = reminder['id']
        reminder_time = datetime.fromisoformat(reminder['time'])
        
        # Only schedule future reminders
        if reminder_time > datetime.now():
            if reminder.get('recurring'):
                # For recurring reminders, use cron trigger
                trigger = CronTrigger(
                    hour=reminder_time.hour,
                    minute=reminder_time.minute
                )
            else:
                # For one-time reminders, use date trigger
                trigger = DateTrigger(run_date=reminder_time)
            
            self.scheduler.add_job(
                self._trigger_reminder,
                trigger=trigger,
                args=[reminder_id],
                id=str(reminder_id),
                replace_existing=True
            )
    
    def _trigger_reminder(self, reminder_id: str):
        """Trigger a reminder."""
        reminder = self.get_reminder(reminder_id)
        if reminder:
            message = f"Reminder: {reminder['message']}"
            print(f"\n🔔 {message}")
            
            # Call voice callback if available
            if self.voice_callback:
                self.voice_callback(message)
            
            # Deactivate non-recurring reminders
            if not reminder.get('recurring', False):
                self.deactivate_reminder(reminder_id)
    
    def add_reminder(self, message: str, reminder_time: datetime, recurring: bool = False) -> Optional[str]:
        """Add a new reminder."""
        try:
            reminder_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            reminder = {
                'id': reminder_id,
                'message': message,
                'time': reminder_time.isoformat(),
                'recurring': recurring,
                'active': True,
                'created_at': datetime.now().isoformat()
            }
            
            self.reminders.append(reminder)
            self._save_reminders()
            self._schedule_reminder(reminder)
            
            return reminder_id
        except Exception as e:
            print(f"Error adding reminder: {e}")
            return None
    
    def get_reminder(self, reminder_id: str) -> Optional[Dict]:
        """Get a reminder by ID."""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                return reminder
        return None
    
    def list_reminders(self, active_only: bool = True) -> List[Dict]:
        """List all reminders."""
        if active_only:
            return [r for r in self.reminders if r.get('active', True)]
        return self.reminders
    
    def delete_reminder(self, reminder_id: str) -> bool:
        """Delete a reminder."""
        try:
            # Remove from scheduler
            try:
                self.scheduler.remove_job(str(reminder_id))
            except:
                pass
            
            # Remove from list
            self.reminders = [r for r in self.reminders if r['id'] != reminder_id]
            self._save_reminders()
            return True
        except Exception as e:
            print(f"Error deleting reminder: {e}")
            return False
    
    def deactivate_reminder(self, reminder_id: str) -> bool:
        """Deactivate a reminder."""
        try:
            for reminder in self.reminders:
                if reminder['id'] == reminder_id:
                    reminder['active'] = False
                    
                    # Remove from scheduler
                    try:
                        self.scheduler.remove_job(str(reminder_id))
                    except:
                        pass
                    
                    self._save_reminders()
                    return True
            return False
        except Exception as e:
            print(f"Error deactivating reminder: {e}")
            return False
    
    def snooze_reminder(self, reminder_id: str, minutes: int = 10) -> bool:
        """Snooze a reminder for specified minutes."""
        try:
            reminder = self.get_reminder(reminder_id)
            if reminder:
                new_time = datetime.now() + timedelta(minutes=minutes)
                reminder['time'] = new_time.isoformat()
                self._save_reminders()
                self._schedule_reminder(reminder)
                return True
            return False
        except Exception as e:
            print(f"Error snoozing reminder: {e}")
            return False
    
    def parse_reminder_time(self, time_str: str) -> Optional[datetime]:
        """Parse reminder time from natural language."""
        try:
            time_str = time_str.lower().strip()
            now = datetime.now()
            
            # Handle "in X minutes/hours"
            if "in" in time_str:
                if "minute" in time_str:
                    minutes = int(''.join(filter(str.isdigit, time_str)))
                    return now + timedelta(minutes=minutes)
                elif "hour" in time_str:
                    hours = int(''.join(filter(str.isdigit, time_str)))
                    return now + timedelta(hours=hours)
            
            # Handle "at HH:MM"
            if "at" in time_str:
                time_parts = time_str.split("at")[1].strip()
                # Try to parse time
                for fmt in ["%I:%M %p", "%H:%M", "%I %p"]:
                    try:
                        parsed_time = datetime.strptime(time_parts, fmt)
                        reminder_time = now.replace(
                            hour=parsed_time.hour,
                            minute=parsed_time.minute,
                            second=0,
                            microsecond=0
                        )
                        # If time has passed today, schedule for tomorrow
                        if reminder_time < now:
                            reminder_time += timedelta(days=1)
                        return reminder_time
                    except ValueError:
                        continue
            
            # Handle "tomorrow at HH:MM"
            if "tomorrow" in time_str:
                time_parts = time_str.split("at")[1].strip() if "at" in time_str else "09:00"
                for fmt in ["%I:%M %p", "%H:%M"]:
                    try:
                        parsed_time = datetime.strptime(time_parts, fmt)
                        reminder_time = (now + timedelta(days=1)).replace(
                            hour=parsed_time.hour,
                            minute=parsed_time.minute,
                            second=0,
                            microsecond=0
                        )
                        return reminder_time
                    except ValueError:
                        continue
            
            return None
        except Exception as e:
            print(f"Error parsing reminder time: {e}")
            return None
    
    def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()


# Global reminder manager instance (will be initialized with voice callback)
reminder_manager = None


def init_reminder_manager(voice_callback=None):
    """Initialize the global reminder manager."""
    global reminder_manager
    reminder_manager = ReminderManager(voice_callback)
    return reminder_manager
