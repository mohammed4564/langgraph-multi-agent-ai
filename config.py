import os
MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:3b')
BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
