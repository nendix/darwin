#!/usr/bin/env python3
"""
Darwin - Simple Test Script
"""

print("🧬 DARWIN EVOLUTION SIMULATOR - BASIC TEST")
print("=" * 60)

try:
    import pygame
    print("✅ Pygame imported successfully")
    
    import numpy as np
    print("✅ NumPy imported successfully")
    
    import matplotlib.pyplot as plt
    print("✅ Matplotlib imported successfully")
    
    # Test basic constants
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    print("\n🧬 Testing Darwin modules...")
    
    # Test configuration
    exec(open('src/config.py').read())
    print("✅ Configuration loaded successfully")
    
    print(f"   - Screen dimensions: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"   - World dimensions: {WORLD_WIDTH}x{WORLD_HEIGHT}")
    print(f"   - Default prey count: {DEFAULT_PREY_COUNT}")
    print(f"   - Default predator count: {DEFAULT_PREDATOR_COUNT}")
    
    print("\n🎮 Basic functionality test passed!")
    print("=" * 60)
    print("✅ ALL BASIC TESTS PASSED!")
    print("\nReady to run Darwin simulation:")
    print("  python main.py")
    print("  or")
    print("  make run")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies:")
    print("  pip install pygame numpy matplotlib")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
