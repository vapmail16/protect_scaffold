"""
Minimal diagnostics script: Only checks for the OPENAI_API_KEY environment variable.
"""

import os
import sys

def check_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY is set.")
        return True
    else:
        print("❌ OPENAI_API_KEY is NOT set.")
        return False

def main():
    print("🔍 Running minimal diagnostics...")
    print("=" * 50)
    success = check_openai_api_key()
    print("=" * 50)
    if not success:
        sys.exit(1)
    print("All checks passed!")

if __name__ == "__main__":
    main() 