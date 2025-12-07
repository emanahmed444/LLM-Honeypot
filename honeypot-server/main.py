import os
import sys

# Ensure we can find local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ssh_server import start_ssh_server
from llm import LLM

def load_env():
    """Manually load .env file to ensure API keys are set."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        print(f"[*] Loading configuration from {env_path}")
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes and whitespace
                    os.environ[key.strip()] = value.strip().strip("'").strip('"')
    else:
        print("[!] Warning: .env file not found.")

def main():
    # 1. Load environment variables
    load_env()

    # 2. Check for API Key
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        print("[-] Error: GEMINI_API_KEY not found. Please check your .env file.")
        return
    
    print(f"[*] API Key found: {api_key[:5]}... (hidden)")

    # 3. Start Server
    try:
        # Initialize LLM (it will read the key from env if not passed, but we pass it to be safe)
        llm = LLM(api_key=api_key, max_examples=None)
        start_ssh_server(llm, port=2222)
    except Exception as e:
        print(f"[-] Critical Error: {e}")

if __name__ == "__main__":
    main()