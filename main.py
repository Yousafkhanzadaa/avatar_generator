from config.settings import Settings
from database.mongodb import MongoDB
from services.tmdb_service import TMDBService
from services.avatar_service import AvatarService
from models.celebrity import Celebrity
from utils.logger import logger
from utils.image_utils import download_image
from datetime import datetime, timedelta
import time

class CelebrityAvatarGenerator:
    def __init__(self):
        self.db = MongoDB()
        self.tmdb_service = TMDBService()
        self.avatar_service = AvatarService()

    def should_update_celebrity(self, celebrity):
        existing_celeb = self.db.get_celebrity(celebrity['id'])
        if not existing_celeb:
            return True
        last_updated = existing_celeb['last_updated']
        return (datetime.now() - last_updated) > timedelta(days=Settings.UPDATE_INTERVAL_DAYS)

    def process_celebrity(self, celeb_basic):
        try:
            # Check if we should update this celebrity
            if not self.should_update_celebrity(celeb_basic):
                logger.info(f"Skipping {celeb_basic['name']} - recently updated")
                return

            # Fetch detailed information
            details = self.tmdb_service.fetch_celebrity_details(celeb_basic['id'])
            if not details or not details.get('profile_path'):
                logger.info(f"Skipping {celeb_basic['name']} - no profile image")
                return

            # Download profile image
            image_url = self.tmdb_service.get_profile_image_url(details['profile_path'])
            image_data = download_image(image_url)
            if not image_data:
                return

            # Generate avatar
            avatar_data = self.avatar_service.generate_avatar(image_data)
            if not avatar_data:
                return

            # Create celebrity object and save to database
            celebrity = Celebrity(details, avatar_data)
            self.db.save_celebrity(celebrity.to_dict())
            
            logger.info(f"Successfully processed {celebrity.name}")
            time.sleep(Settings.RATE_LIMIT_DELAY)

        except Exception as e:
            logger.error(f"Error processing celebrity {celeb_basic.get('name', 'Unknown')}: {str(e)}")

    def run(self):
        try:
            celebrities = self.tmdb_service.fetch_popular_celebrities()
            for celeb in celebrities:
                self.process_celebrity(celeb)
        finally:
            self.db.close()

def main():
    generator = CelebrityAvatarGenerator()
    generator.run()

if __name__ == "__main__":
    main()