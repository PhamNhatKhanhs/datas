import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base configuration
BASE_URL = os.getenv('BASE_URL', 'https://vnexpress.net')
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'json')
CONCURRENT_REQUESTS = int(os.getenv('CONCURRENT_REQUESTS', 5))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 1))
USER_AGENT = os.getenv('USER_AGENT')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///output/articles.db')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
