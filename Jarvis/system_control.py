"""System control and automation for Jarvis AI Assistant."""

import os
import subprocess
import psutil
import platform
from typing import List, Dict, Optional, Tuple
from .utils import format_bytes, is_windows


class SystemControl:
    """Manages system operations and monitoring."""
    
    def __init__(self):
        """Initialize system control."""
        self.platform = platform.system()
    
    # ========== Application Management ==========
    
    def open_application(self, app_name: str) -> bool:
        """Open an application by name."""
        try:
            app_name = app_name.lower()
            
            # Common application mappings
            app_mappings = {
                'chrome': 'chrome.exe' if is_windows() else 'google-chrome',
                'firefox': 'firefox.exe' if is_windows() else 'firefox',
                'edge': 'msedge.exe' if is_windows() else 'microsoft-edge',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe' if is_windows() else 'gnome-calculator',
                'vs code': 'code',
                'vscode': 'code',
                'spotify': 'spotify.exe' if is_windows() else 'spotify',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'outlook': 'outlook.exe',
                'discord': 'discord.exe' if is_windows() else 'discord',
                'teams': 'teams.exe' if is_windows() else 'teams',
                'zoom': 'zoom.exe' if is_windows() else 'zoom'
            }
            
            executable = app_mappings.get(app_name, app_name)
            
            if is_windows():
                os.startfile(executable) if '.exe' in executable else subprocess.Popen(executable, shell=True)
            else:
                subprocess.Popen([executable])
            
            return True
        except Exception as e:
            print(f"Error opening application: {e}")
            return False
    
    def close_application(self, app_name: str) -> bool:
        """Close an application by name."""
        try:
            app_name = app_name.lower()
            closed = False
            
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name in proc.info['name'].lower():
                        proc.terminate()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return closed
        except Exception as e:
            print(f"Error closing application: {e}")
            return False
    
    def list_running_applications(self) -> List[str]:
        """List all running applications."""
        try:
            apps = set()
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name']:
                        apps.add(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return sorted(list(apps))
        except Exception as e:
            print(f"Error listing applications: {e}")
            return []
    
    # ========== System Monitoring ==========
    
    def get_battery_status(self) -> Optional[Dict[str, any]]:
        """Get battery status information."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percentage': battery.percent,
                    'charging': battery.power_plugged,
                    'time_remaining': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
            return None
        except Exception as e:
            print(f"Error getting battery status: {e}")
            return None
    
    def get_cpu_usage(self) -> Dict[str, any]:
        """Get CPU usage information."""
        try:
            return {
                'total': psutil.cpu_percent(interval=1),
                'per_core': psutil.cpu_percent(interval=1, percpu=True),
                'cores': psutil.cpu_count(logical=False),
                'threads': psutil.cpu_count(logical=True)
            }
        except Exception as e:
            print(f"Error getting CPU usage: {e}")
            return {}
    
    def get_memory_usage(self) -> Dict[str, any]:
        """Get RAM usage information."""
        try:
            mem = psutil.virtual_memory()
            return {
                'total': format_bytes(mem.total),
                'available': format_bytes(mem.available),
                'used': format_bytes(mem.used),
                'percentage': mem.percent,
                'total_bytes': mem.total,
                'available_bytes': mem.available
            }
        except Exception as e:
            print(f"Error getting memory usage: {e}")
            return {}
    
    def get_disk_usage(self) -> Dict[str, any]:
        """Get disk usage information."""
        try:
            disk = psutil.disk_usage('/')
            return {
                'total': format_bytes(disk.total),
                'used': format_bytes(disk.used),
                'free': format_bytes(disk.free),
                'percentage': disk.percent
            }
        except Exception as e:
            print(f"Error getting disk usage: {e}")
            return {}
    
    def check_internet_connection(self) -> bool:
        """Check if internet connection is available."""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    # ========== Power Control ==========
    
    def shutdown(self, delay: int = 0) -> bool:
        """Shutdown the system."""
        try:
            if is_windows():
                os.system(f"shutdown /s /f /t {delay}")
            else:
                os.system(f"shutdown -h +{delay//60}")
            return True
        except Exception as e:
            print(f"Error shutting down: {e}")
            return False
    
    def restart(self, delay: int = 0) -> bool:
        """Restart the system."""
        try:
            if is_windows():
                os.system(f"shutdown /r /f /t {delay}")
            else:
                os.system(f"shutdown -r +{delay//60}")
            return True
        except Exception as e:
            print(f"Error restarting: {e}")
            return False
    
    def sleep(self) -> bool:
        """Put system to sleep."""
        try:
            if is_windows():
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif self.platform == "Darwin":  # macOS
                os.system("pmset sleepnow")
            else:  # Linux
                os.system("systemctl suspend")
            return True
        except Exception as e:
            print(f"Error putting system to sleep: {e}")
            return False
    
    def hibernate(self) -> bool:
        """Hibernate the system."""
        try:
            if is_windows():
                os.system("shutdown /h")
            else:
                os.system("systemctl hibernate")
            return True
        except Exception as e:
            print(f"Error hibernating: {e}")
            return False
    
    def lock_screen(self) -> bool:
        """Lock the screen."""
        try:
            if is_windows():
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif self.platform == "Darwin":  # macOS
                os.system("pmset displaysleepnow")
            else:  # Linux
                os.system("xdg-screensaver lock")
            return True
        except Exception as e:
            print(f"Error locking screen: {e}")
            return False
    
    def cancel_shutdown(self) -> bool:
        """Cancel scheduled shutdown/restart."""
        try:
            if is_windows():
                os.system("shutdown /a")
            else:
                os.system("shutdown -c")
            return True
        except Exception as e:
            print(f"Error cancelling shutdown: {e}")
            return False
    
    # ========== File Operations ==========
    
    def create_file(self, filepath: str, content: str = "") -> bool:
        """Create a new file."""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def create_folder(self, folderpath: str) -> bool:
        """Create a new folder."""
        try:
            os.makedirs(folderpath, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False
    
    def delete_folder(self, folderpath: str) -> bool:
        """Delete a folder."""
        try:
            import shutil
            if os.path.exists(folderpath):
                shutil.rmtree(folderpath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting folder: {e}")
            return False
    
    def open_folder(self, folderpath: str) -> bool:
        """Open a folder in file explorer."""
        try:
            if is_windows():
                os.startfile(folderpath)
            elif self.platform == "Darwin":  # macOS
                subprocess.Popen(["open", folderpath])
            else:  # Linux
                subprocess.Popen(["xdg-open", folderpath])
            return True
        except Exception as e:
            print(f"Error opening folder: {e}")
            return False


# Global system control instance
system_control = SystemControl()
