#!/usr/bin/env python3
"""
Build script for creating Windows executable for Faker GUI.
Run this script to build the application.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """Main build process."""
    print("=" * 60)
    print("Faker GUI - Windows Executable Builder")
    print("=" * 60)
    print()
    
    # Get project root directory
    project_dir = Path(__file__).parent.absolute()
    os.chdir(project_dir)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found!")
        print("  Please install it using:")
        print("  pip install -r requirements-build.txt")
        sys.exit(1)
    
    # Check if faker is installed
    try:
        import faker
        print(f"✓ Faker library found")
    except ImportError:
        print("✗ Faker library not found!")
        print("  Please install it using:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("Building Windows executable...")
    print("-" * 60)
    
    # Clean previous builds
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            print(f"Cleaning {dir_name}/ directory...")
            shutil.rmtree(dir_path)
    
    # Build command using PyInstaller
    build_cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=FakerGUI",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "faker_gui.py"
    ]
    
    print(f"Running: {' '.join(build_cmd)}")
    print()
    
    # Run PyInstaller
    result = subprocess.run(build_cmd, cwd=project_dir)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        print()
        print(f"Executable location: {project_dir / 'dist' / 'FakerGUI.exe'}")
        print()
        print("You can now distribute the FakerGUI.exe file.")
        print("It can run on Windows without Python installed.")
        print()
    else:
        print()
        print("=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print()
        print("Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
