"""Setup wizard for Jarvis AI Assistant."""

import os
import sys
from pathlib import Path


def print_header():
    """Print setup header."""
    print("\n" + "=" * 70)
    print("    🤖 JARVIS AI ASSISTANT - Setup Wizard")
    print("=" * 70 + "\n")


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if all dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'pyttsx3',
        'wikipedia',
        'pyautogui',
        'speech_recognition',
        'pyjokes',
        'psutil',
        'requests',
        'dotenv',
        'apscheduler'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True


def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Created: {data_dir}")
    
    return True


def setup_env_file():
    """Setup .env file."""
    print("\n🔑 Setting up API keys...")
    
    env_file = Path(__file__).parent.parent / ".env"
    env_example = Path(__file__).parent.parent / ".env.example"
    
    if env_file.exists():
        print("✅ .env file already exists")
        response = input("   Do you want to reconfigure it? (y/n): ").lower()
        if response != 'y':
            return True
    
    if not env_example.exists():
        print("⚠️  .env.example not found")
        return False
    
    # Copy example file
    with open(env_example, 'r') as f:
        content = f.read()
    
    print("\nAPI Key Setup:")
    print("-" * 70)
    print("You can add these API keys now or skip and add them later.")
    print("Press Enter to skip any key.\n")
    
    # OpenAI
    print("🤖 OpenAI GPT (for AI conversations):")
    print("   Get it from: https://platform.openai.com/api-keys")
    openai_key = input("   API Key: ").strip()
    if openai_key:
        content = content.replace('your_openai_api_key_here', openai_key)
    
    # Gemini
    print("\n🤖 Google Gemini (alternative to OpenAI):")
    print("   Get it from: https://makersuite.google.com/app/apikey")
    gemini_key = input("   API Key: ").strip()
    if gemini_key:
        content = content.replace('your_gemini_api_key_here', gemini_key)
    
    # NewsAPI
    print("\n📰 NewsAPI (for news updates):")
    print("   Get it from: https://newsapi.org/")
    news_key = input("   API Key: ").strip()
    if news_key:
        content = content.replace('your_news_api_key_here', news_key)
    
    # Save .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"\n✅ Created: {env_file}")
    print("   You can edit this file later to add or update API keys.")
    
    return True


def test_microphone():
    """Test microphone access."""
    print("\n🎤 Testing microphone...")
    
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("✅ Microphone detected")
            return True
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("   Make sure your microphone is connected and working")
        return False


def configure_assistant():
    """Configure assistant settings."""
    print("\n⚙️  Configure Assistant:")
    print("-" * 70)
    
    name = input("What would you like to name your assistant? (default: Jarvis): ").strip()
    if not name:
        name = "Jarvis"
    
    print(f"\n✅ Assistant name set to: {name}")
    
    # Save to config
    try:
        from config import config as cfg
        cfg.set('assistant_name', name)
        print("✅ Configuration saved")
    except Exception as e:
        print(f"⚠️  Could not save configuration: {e}")
    
    return True


def print_next_steps():
    """Print next steps."""
    print("\n" + "=" * 70)
    print("🎉 Setup Complete!")
    print("=" * 70)
    print("\n📝 Next Steps:")
    print("   1. Make sure all dependencies are installed:")
    print("      pip install -r requirements.txt")
    print("\n   2. (Optional) Add API keys to .env file for advanced features")
    print("\n   3. Run Jarvis:")
    print("      cd Jarvis")
    print("      python jarvis_enhanced.py")
    print("\n   4. Start speaking commands after 'Listening...' appears")
    print("\n💡 Quick Commands:")
    print("   - 'What's the time?'")
    print("   - 'Tell me a joke'")
    print("   - 'Search Wikipedia for AI'")
    print("   - 'Play music'")
    print("   - 'What's my battery status?'")
    print("   - 'Goodbye' (to exit)")
    print("\n📖 For more commands, see README_ENHANCED.md")
    print("\n" + "=" * 70 + "\n")


def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        print("\n⚠️  Please install dependencies first:")
        print("   pip install -r requirements.txt")
        print("\nThen run this setup again.")
        sys.exit(1)
    
    # Setup .env file
    setup_env_file()
    
    # Test microphone
    test_microphone()
    
    # Configure assistant
    configure_assistant()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
