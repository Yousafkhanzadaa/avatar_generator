import requests
from config.settings import Settings
from utils.logger import logger
import time

class TMDBService:
    def __init__(self):
        self.headers = {
            # 'Authorization': f'Bearer {Settings.TMDB_API_KEY}',
            'Content-Type': 'application/json'
        }

    def fetch_popular_celebrities(self, num_pages=15):
        all_celebrities = []
        #** Commented
        for page in range(1, 2):
            try:
                response = requests.get(
                    f'{Settings.TMDB_BASE_URL}/person/popular',
                    headers=self.headers,
                    params={'page': page, 'api_key': Settings.TMDB_API_KEY}
                )
                response.raise_for_status()
                celebrities = response.json()['results']
                all_celebrities.extend(celebrities)
                logger.info(f"Fetched page {page} of celebrities")
                time.sleep(Settings.RATE_LIMIT_DELAY)
            except Exception as e:
                logger.error(f"Error fetching celebrities page {page}: {str(e)}")
                continue
        return all_celebrities

    def fetch_celebrity_details(self, celebrity_id):
        try:
            response = requests.get(
                f'{Settings.TMDB_BASE_URL}/person/{celebrity_id}',
                headers=self.headers,
                params={ 'api_key': Settings.TMDB_API_KEY}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching details for celebrity {celebrity_id}: {str(e)}")
            return None

    def get_profile_image_url(self, profile_path):
        return f'{Settings.TMDB_IMAGE_BASE_URL}{profile_path}'