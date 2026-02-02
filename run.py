#!/usr/bin/env python3
"""
Launcher script for Faker GUI application.
Run this script to start the application.
"""

import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import faker
        print("✓ Dependencies are installed")
        return True
    except ImportError:
        print("✗ Missing dependencies!")
        print("\nPlease install dependencies by running:")
        print("  pip install -r requirements.txt")
        return False

def main():
    """Main entry point."""
    print("=" * 60)
    print("Faker GUI - SQL Data Generator")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run the GUI
    print("Starting application...\n")
    try:
        import faker_gui
        faker_gui.main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
