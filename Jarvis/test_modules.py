"""
Test script for Jarvis modules - validates basic functionality
"""

import sys
import os

# Add Jarvis directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    try:
        from config import config
        print("✓ config")
    except Exception as e:
        print(f"✗ config: {e}")
        return False
    
    try:
        from utils import ColorText, get_greeting
        print("✓ utils")
    except Exception as e:
        print(f"✗ utils: {e}")
        return False
    
    try:
        from voice_manager import voice_manager
        print("✓ voice_manager")
    except Exception as e:
        print(f"✗ voice_manager: {e}")
        return False
    
    try:
        from ai_engine import ai_engine
        print("✓ ai_engine")
    except Exception as e:
        print(f"✗ ai_engine: {e}")
        return False
    
    try:
        from system_control import system_control
        print("✓ system_control")
    except Exception as e:
        print(f"✗ system_control: {e}")
        return False
    
    try:
        from calculator import calculator
        print("✓ calculator")
    except Exception as e:
        print(f"✗ calculator: {e}")
        return False
    
    try:
        from weather_handler import weather_handler
        print("✓ weather_handler")
    except Exception as e:
        print(f"✗ weather_handler: {e}")
        return False
    
    try:
        from news_handler import news_handler
        print("✓ news_handler")
    except Exception as e:
        print(f"✗ news_handler: {e}")
        return False
    
    try:
        from whatsapp_handler import whatsapp_handler
        print("✓ whatsapp_handler")
    except Exception as e:
        print(f"✗ whatsapp_handler: {e}")
        return False
    
    return True


def test_config():
    """Test configuration system."""
    print("\nTesting configuration...")
    
    try:
        from config import config
        
        # Test get
        name = config.get('assistant_name', 'Jarvis')
        print(f"✓ Assistant name: {name}")
        
        # Test set
        config.set('test_key', 'test_value')
        value = config.get('test_key')
        assert value == 'test_value', "Config set/get failed"
        print("✓ Config set/get works")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_utils():
    """Test utility functions."""
    print("\nTesting utilities...")
    
    try:
        from utils import get_greeting, format_time, extract_number, ColorText
        
        greeting = get_greeting()
        print(f"✓ Greeting: {greeting}")
        
        time_str = format_time('12h')
        print(f"✓ Time: {time_str}")
        
        number = extract_number("shutdown in 10 minutes")
        assert number == 10, "Extract number failed"
        print(f"✓ Extract number: {number}")
        
        ColorText.success("Color text works")
        
        return True
    except Exception as e:
        print(f"✗ Utils test failed: {e}")
        return False


def test_calculator():
    """Test calculator functionality."""
    print("\nTesting calculator...")
    
    try:
        from calculator import calculator
        
        # Test basic arithmetic
        result = calculator.evaluate_expression("5 + 3")
        assert result == 8, f"Expected 8, got {result}"
        print(f"✓ 5 + 3 = {result}")
        
        result = calculator.evaluate_expression("10 * 2")
        assert result == 20, f"Expected 20, got {result}"
        print(f"✓ 10 * 2 = {result}")
        
        # Test voice input parsing
        result = calculator.parse_calculation("what is 5 plus 3")
        assert result == "8", f"Expected '8', got {result}"
        print(f"✓ Voice calculation: {result}")
        
        return True
    except Exception as e:
        print(f"✗ Calculator test failed: {e}")
        return False


def test_system_control():
    """Test system control (read-only operations)."""
    print("\nTesting system control...")
    
    try:
        from system_control import system_control
        
        # Test battery (may not be available on all systems)
        battery = system_control.get_battery_status()
        if battery:
            print(f"✓ Battery: {battery['percentage']}%")
        else:
            print("○ Battery info not available (may be a desktop)")
        
        # Test CPU
        cpu = system_control.get_cpu_usage()
        print(f"✓ CPU usage: {cpu['total']}%")
        
        # Test memory
        memory = system_control.get_memory_usage()
        print(f"✓ RAM: {memory['percentage']}% used")
        
        # Test internet
        internet = system_control.check_internet_connection()
        print(f"✓ Internet: {'Connected' if internet else 'Disconnected'}")
        
        return True
    except Exception as e:
        print(f"✗ System control test failed: {e}")
        return False


def test_voice_manager():
    """Test voice manager (without actually speaking)."""
    print("\nTesting voice manager...")
    
    try:
        from voice_manager import voice_manager
        
        voices = voice_manager.get_available_voices()
        print(f"✓ Available voices: {len(voices)}")
        
        info = voice_manager.get_current_voice_info()
        print(f"✓ Current voice: {info.get('name', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"✗ Voice manager test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("    JARVIS AI ASSISTANT - Module Tests")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Utilities", test_utils()))
    results.append(("Calculator", test_calculator()))
    results.append(("System Control", test_system_control()))
    results.append(("Voice Manager", test_voice_manager()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
