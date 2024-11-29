import os
from dotenv import load_dotenv


load_dotenv(override=True)

class Settings:
    # API Keys and Credentials
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    LIGHTX_API_KEY = os.getenv('LIGHTX_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # API URLs
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
    LIGHTX_AVATAR_URL = 'https://api.lightxeditor.com/external/api/v1/avatar'
    LIGHTX_STATUS_URL = 'https://api.lightxeditor.com/external/api/v1/order-status'

    # Application Settings
    MAX_RETRIES = 5
    STATUS_CHECK_DELAY = 3
    RATE_LIMIT_DELAY = 1