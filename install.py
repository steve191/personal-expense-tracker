#!/usr/bin/env python3
"""
Installation script for Personal Expense Tracker
Run this before main.py to install all required dependencies.

Usage: python install.py
"""

import subprocess
import sys

REQUIRED_PACKAGES = [
    "ttkbootstrap",
    "python-dateutil", 
    "pandas",
    "ofxtools",
    "pillow",
]

def install_packages():
    print("=" * 50)
    print("Personal Expense Tracker - Dependency Installer")
    print("=" * 50)
    print(f"\nPython version: {sys.version}")
    print(f"\nInstalling required packages...")
    print("-" * 50)
    
    failed = []
    
    for package in REQUIRED_PACKAGES:
        print(f"\nInstalling {package}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  [OK] {package} installed successfully")
            else:
                print(f"  [ERROR] Failed to install {package}")
                print(f"  {result.stderr}")
                failed.append(package)
        except Exception as e:
            print(f"  [ERROR] Exception installing {package}: {e}")
            failed.append(package)
    
    print("\n" + "=" * 50)
    
    if failed:
        print("Installation completed with errors.")
        print(f"Failed packages: {', '.join(failed)}")
        print("\nTry installing failed packages manually:")
        for pkg in failed:
            print(f"  pip install {pkg}")
        return False
    else:
        print("All packages installed successfully!")
        print("\nYou can now run the application with:")
        print("  python main.py")
        return True

def verify_imports():
    print("\nVerifying installations...")
    print("-" * 50)
    
    checks = [
        ("ttkbootstrap", "ttkbootstrap"),
        ("python-dateutil", "dateutil"),
        ("pandas", "pandas"),
        ("ofxtools", "ofxtools"),
        ("pillow", "PIL"),
    ]
    
    all_ok = True
    for package_name, import_name in checks:
        try:
            __import__(import_name)
            print(f"  [OK] {package_name}")
        except ImportError:
            print(f"  [MISSING] {package_name}")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    success = install_packages()
    
    if success:
        verified = verify_imports()
        if verified:
            print("\n" + "=" * 50)
            print("Setup complete! Run 'python main.py' to start.")
            print("=" * 50)
        else:
            print("\nSome packages failed verification.")
            print("Try restarting your terminal and running install.py again.")
            sys.exit(1)
    else:
        sys.exit(1)
