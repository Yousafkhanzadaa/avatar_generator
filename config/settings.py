from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # API Keys and Credentials
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')

    # API URLs
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
    DEEPAI_TOONIFY_URL = 'https://api.deepai.org/api/toonify'

    # Application Settings
    BATCH_SIZE = 20
    UPDATE_INTERVAL_DAYS = 7
    RATE_LIMIT_DELAY = 1