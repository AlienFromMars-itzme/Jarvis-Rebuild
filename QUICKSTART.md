# 🚀 Quick Start Guide - Jarvis AI Assistant

Get up and running with Jarvis in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- Microphone (for voice input)
- Windows OS (recommended) - partial support for Linux/Mac

## Installation Steps

### 1. Clone and Navigate

```bash
git clone https://github.com/AlienFromMars-itzme/Jarvis-Rebuild.git
cd Jarvis-Rebuild
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues with PyAudio on Windows:
- Download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Install it: `pip install PyAudio-0.2.11-cp3x-cp3xm-win_amd64.whl`

### 4. Run Setup Wizard (Optional)

```bash
cd Jarvis
python setup.py
```

This will help you:
- Configure API keys
- Set assistant name
- Test microphone
- Verify installation

### 5. Start Jarvis!

```bash
python jarvis_enhanced.py
```

## Quick Configuration (Optional)

To enable AI features and advanced capabilities:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   ```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys (Free trial available)
- NewsAPI: https://newsapi.org/ (Free tier: 500 requests/day)
- Google Gemini: https://makersuite.google.com/app/apikey (Free)

## First Commands to Try

Once Jarvis says "Listening...", try these:

### Basic Commands
```
"What's the time?"
"What's the date?"
"Tell me a joke"
```

### Information
```
"Search Wikipedia for artificial intelligence"
"What's my battery status?"
"Check CPU usage"
```

### Entertainment
```
"Play music"
"Open YouTube"
```

### System Control
```
"Take a screenshot"
"Increase volume"
"Lock screen"
```

### With API Keys
```
"What's the weather?"
"Get me the latest news"
"Calculate 25 times 4"
"Tell me about quantum computing" (AI response)
```

### Exit
```
"Goodbye"
"Exit"
"Offline"
```

## Troubleshooting

### "Speech recognition service unavailable"
- Check internet connection
- Verify microphone is working
- Try speaking more clearly

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "No module named 'pyttsx3'"
```bash
pip install -r requirements.txt
```

### PyAudio Issues (Windows)
Download and install from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### Microphone Not Working
- Check Windows Sound Settings
- Ensure microphone is set as default recording device
- Grant microphone permissions to Python

### AI Features Not Working
- Add API keys to `.env` file
- Verify API keys are valid
- Check internet connection

## Feature Checklist

Without API keys, you can use:
- ✅ Voice commands
- ✅ Time and date
- ✅ System monitoring (battery, CPU, RAM)
- ✅ Application control
- ✅ Volume and brightness control
- ✅ Music playback
- ✅ Screenshots
- ✅ Jokes
- ✅ Wikipedia search
- ✅ Web browsing
- ✅ Calculator

With API keys, you also get:
- 🔑 AI conversations (OpenAI/Gemini)
- 🔑 News updates (NewsAPI)
- 🔑 Weather updates (OpenWeatherMap)
- 🔑 Advanced features

## What's Next?

1. **Customize**: Edit `Jarvis/data/config.json` to personalize settings
2. **Explore**: Try different voice commands (see README_ENHANCED.md)
3. **Extend**: Add your own features by modifying the modules
4. **Share**: Star the repo if you find it useful! ⭐

## Need Help?

- 📖 Full documentation: [README_ENHANCED.md](README_ENHANCED.md)
- 🐛 Issues: Open an issue on GitHub
- 💬 Questions: Check the troubleshooting section

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│               JARVIS VOICE COMMANDS                     │
├─────────────────────────────────────────────────────────┤
│ Information                                             │
│  • "What's the time?"                                   │
│  • "What's my battery status?"                          │
│  • "Check internet connection"                          │
├─────────────────────────────────────────────────────────┤
│ System Control                                          │
│  • "Open Chrome"                                        │
│  • "Close Firefox"                                      │
│  • "Increase volume"                                    │
│  • "Take a screenshot"                                  │
├─────────────────────────────────────────────────────────┤
│ Entertainment                                           │
│  • "Play Shape of You on YouTube"                       │
│  • "Tell me a joke"                                     │
│  • "Open YouTube"                                       │
├─────────────────────────────────────────────────────────┤
│ Advanced (with API keys)                                │
│  • "What's the weather?"                                │
│  • "Get latest tech news"                               │
│  • "Calculate 45 plus 37"                               │
│  • "Tell me about space exploration" (AI)               │
├─────────────────────────────────────────────────────────┤
│ Power                                                   │
│  • "Shutdown the computer"                              │
│  • "Lock screen"                                        │
│  • "Put computer to sleep"                              │
└─────────────────────────────────────────────────────────┘
```

---

**Ready to explore? Start with "What's the time?" and go from there!** 🚀
