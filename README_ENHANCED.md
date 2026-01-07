# Jarvis AI Assistant - Enhanced Version 🤖✨

<img src="https://giffiles.alphacoders.com/212/212508.gif" alt="Jarvis AI">

## 🌟 Overview

**Jarvis AI Assistant** is an advanced, feature-rich desktop voice assistant powered by AI that can automate your daily tasks, monitor your system, manage communications, and provide intelligent conversations. With 15+ powerful features and AI integration, Jarvis transforms your computer into a smart, voice-controlled companion.

**🔥 New in Version 2.0:**
- 🧠 AI-powered conversations (OpenAI GPT / Google Gemini)
- 🎤 8 different voice options (4 male + 4 female)
- 💻 Full system automation and monitoring
- 📱 WhatsApp automation
- 📰 Real-time news updates
- ⏰ Smart reminders and scheduling
- 🎵 YouTube and local music playback
- 🔊 Volume and brightness control
- And much more!

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Voice Commands](#-voice-commands)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🧠 AI Voice Reply System
- **Intelligent Conversations**: Powered by OpenAI GPT or Google Gemini
- **Contextual Responses**: Maintains conversation history for natural dialogue
- **Personalized**: Adapts to user preferences
- **Fallback Mode**: Works offline with basic responses

### 🎤 Enhanced Voice System
- **8 Voice Options**: 4 male and 4 female voices with different tones
- **Voice Switching**: Change voices on command
- **Persistent Settings**: Saves your voice preference
- **Natural Speech**: Clear and human-like voice output

### 💻 Full System Automation
- **Application Management**:
  - Open applications by name (Chrome, VS Code, Notepad, etc.)
  - Close running applications
  - List all running applications
  
- **File & Folder Operations**:
  - Create, delete, and manage files
  - Create and delete folders
  - Open folders in file explorer

### 📊 System Status Monitoring
- **Battery Status**: Check percentage, charging status, and time remaining
- **CPU Monitoring**: View CPU usage and core information
- **RAM Usage**: Monitor memory usage and availability
- **Internet Status**: Check connection status

### 🪟 Windows & Power Control
- **Power Management**:
  - Shutdown (immediate or scheduled)
  - Restart (immediate or scheduled)
  - Sleep mode
  - Hibernate
  - Lock screen
  - Cancel scheduled operations

### 🔊 Volume & Brightness Control
- **Volume Control**:
  - Increase/decrease volume
  - Set specific volume level
  - Mute/unmute
  - Show current volume
  
- **Brightness Management**:
  - Increase/decrease brightness
  - Set specific brightness level
  - Show current brightness

### 📱 WhatsApp Automation
- Send text messages to contacts
- Send messages to groups
- Schedule WhatsApp messages
- Open specific chats

### 🎵 Music Playback
- **YouTube Integration**: Play any song on YouTube
- **Local Music**: Play music from your Music folder
- **Smart Search**: Find and play songs by name

### 📰 News Updates
- Fetch real-time news from NewsAPI
- Get news by category (technology, sports, business, health, etc.)
- Get trending news
- Hear news headlines read aloud

### ⏰ Smart Reminders & Scheduling
- Set reminders with natural language ("remind me to call mom at 3 PM")
- Set recurring reminders
- List all active reminders
- Snooze reminders
- Smart time parsing ("in 30 minutes", "tomorrow at 9 AM", etc.)

### 🎮 Entertainment & More
- Tell jokes (powered by pyjokes)
- Wikipedia search
- Google search
- Take screenshots
- Open websites
- Weather updates (with API key)
- And much more!

## 📌 Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows (primary), Linux/Mac (partial support)
- **Microphone**: For voice input
- **Internet Connection**: For AI features, news, and online services
- **API Keys** (optional but recommended):
  - OpenAI API key or Google Gemini API key (for AI conversations)
  - NewsAPI key (for news updates)
  - Spotify credentials (for Spotify integration)

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AlienFromMars-itzme/Jarvis-Rebuild.git
cd Jarvis-Rebuild
```

### 2. Create and Activate Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install PyAudio (Windows)

PyAudio can be tricky on Windows. Follow these steps:

1. Download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Install it: `pip install path/to/PyAudio‑0.2.11‑cp3x‑cp3xm‑win_amd64.whl`

Or follow the guide [here](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14)

### 5. Configure API Keys (Optional but Recommended)

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
# AI Integration
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# News API
NEWS_API_KEY=your_news_api_key_here

# Spotify (optional)
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Google Gemini: https://makersuite.google.com/app/apikey
- NewsAPI: https://newsapi.org/
- Spotify: https://developer.spotify.com/dashboard/

## ⚙️ Configuration

The assistant uses a configuration file located at `Jarvis/data/config.json`. This file is automatically created on first run with default settings.

You can customize:
- Assistant name
- Voice settings (voice ID, rate, volume)
- Enabled features
- Preferences (news category, music service, etc.)

## 🚀 Usage

### Running the Assistant

Navigate to the Jarvis directory and run:

```bash
cd Jarvis
python jarvis_enhanced.py
```

Or for the original (basic) version:
```bash
python jarvis.py
```

### First Run

On first run, Jarvis will:
1. Create necessary configuration files
2. Greet you based on the time of day
3. Wait for your voice commands

### Interacting with Jarvis

Simply speak your commands after Jarvis says "Listening...". The assistant will process your command and respond accordingly.

## 🎯 Voice Commands

Here are some example commands you can use:

### Basic Information
- "What's the time?"
- "What's the date?"
- "Tell me a joke"

### Web & Search
- "Search Wikipedia for artificial intelligence"
- "Google Python programming"
- "Open YouTube"
- "Open Google"

### Music & Entertainment
- "Play Shape of You on YouTube"
- "Play music"
- "Play some song"

### System Monitoring
- "What's my battery status?"
- "Check CPU usage"
- "How much RAM am I using?"
- "Check internet connection"

### System Control
- "Open Chrome"
- "Close Firefox"
- "Take a screenshot"
- "Increase volume"
- "Decrease brightness"
- "Set volume to 50%"
- "Set brightness to 75%"

### News
- "Get me the latest news"
- "What's the news in technology?"
- "Tell me sports news"

### Reminders
- "Remind me to call mom at 3 PM"
- "Set a reminder for my meeting in 30 minutes"
- "Remind me to take medicine tomorrow at 9 AM"
- "List my reminders"

### Voice Settings
- "Change your voice"
- "Switch to male voice"
- "Switch to female voice"

### Power Control
- "Shutdown the computer"
- "Shutdown in 10 minutes"
- "Restart the computer"
- "Put the computer to sleep"
- "Lock screen"

### AI Conversations
Ask anything! If Jarvis doesn't have a specific command for it, the AI will respond:
- "What's the weather like today?"
- "Tell me about quantum computing"
- "How do I make pasta?"
- "What's the capital of France?"

### Exit
- "Goodbye"
- "Exit"
- "Offline"

## 📁 Project Structure

```
Jarvis-Rebuild/
├── Jarvis/
│   ├── jarvis.py                    # Original version
│   ├── jarvis_enhanced.py           # Enhanced version (use this)
│   ├── config.py                    # Configuration management
│   ├── ai_engine.py                 # AI integration (OpenAI/Gemini)
│   ├── voice_manager.py             # Voice control system
│   ├── system_control.py            # System operations
│   ├── whatsapp_handler.py          # WhatsApp automation
│   ├── news_handler.py              # News fetching
│   ├── reminder_manager.py          # Reminders & scheduling
│   ├── utils.py                     # Utility functions
│   └── data/
│       ├── config.json              # User configuration
│       ├── reminders.json           # Active reminders
│       └── conversation_history.json # AI conversation history
├── requirements.txt                 # Python dependencies
├── .env.example                     # API keys template
├── .env                            # Your API keys (not in git)
├── .gitignore                      # Git ignore file
├── README.md                       # This file
└── LICENSE                         # MIT License
```

## 🔧 Troubleshooting

### Common Issues

**1. "Speech recognition service unavailable"**
- Check your internet connection
- Ensure your microphone is working
- Try speaking more clearly

**2. "PyAudio installation failed"**
- On Windows, download the appropriate `.whl` file
- On Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`
- On Mac: `brew install portaudio`

**3. "AI features not working"**
- Make sure you've added your API keys to the `.env` file
- Check that the API keys are valid
- Ensure you have internet connection
- Install required libraries: `pip install openai google-generativeai`

**4. "News not working"**
- Add your NewsAPI key to `.env`
- Free tier has limitations (500 requests/day)
- Check your internet connection

**5. "Volume/Brightness control not working"**
- Windows: Install `pip install pycaw comtypes`
- Linux: May require additional system packages
- Some features may be Windows-only

**6. Module import errors**
- Ensure you're in the Jarvis directory when running
- Check all dependencies are installed
- Try: `pip install -r requirements.txt --upgrade`

### Debug Mode

To see detailed error messages, check the console output. Errors are printed in red with details.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/AmazingFeature`
3. **Commit Your Changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the Branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Test your changes thoroughly
- Update documentation as needed

## 🐛 Known Limitations

- Some features are Windows-specific (volume control, certain power functions)
- WhatsApp automation requires WhatsApp Web to be accessible
- AI features require internet connection and valid API keys
- Free tier API limits apply (NewsAPI: 500 requests/day)
- Voice recognition works best in quiet environments

## 🔐 Security & Privacy

- API keys are stored in `.env` file (not committed to git)
- Conversation history is stored locally
- No data is sent to third parties except API providers
- You can disable AI features in config for offline use

## 🎯 Future Enhancements

- [ ] Spotify integration
- [ ] Weather updates with OpenWeatherMap
- [ ] Email management (Gmail)
- [ ] Wake word detection ("Hey Jarvis")
- [ ] GUI interface
- [ ] Mobile app integration
- [ ] Smart home integration
- [ ] Multi-language support
- [ ] Custom command creation
- [ ] Plugin system

## 📜 License

This project is [MIT](LICENSE) licensed.

## 👨‍💻 Original Author

**Kishan Kumar Rai**
- Twitter: [@kishan_rajput23](https://twitter.com/kishan_rajput23)
- GitHub: [@kishanrajput23](https://github.com/kishanrajput23)
- LinkedIn: [@kishan-kumar-rai](https://linkedin.com/in/kishan-kumar-rai-23112000)

## 🌟 Enhanced Version Contributors

Enhanced with advanced AI features, system automation, and 15+ new capabilities.

## ⭐ Show Your Support

Please ⭐️ this repository if this project helped you!

## 📞 Support

Having issues? Please open an issue on GitHub with:
- Detailed description of the problem
- Error messages (if any)
- Your OS and Python version
- Steps to reproduce

---

**Made with ❤️ and powered by AI**

*Transform your computer into an intelligent assistant today!* 🚀
