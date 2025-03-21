from config.settings import Settings
from database.mongodb import MongoDB
from services.tmdb_service import TMDBService
from services.avatar_service import LightXAvatarService
from services.biography_service import BiographyService
from models.celebrity import Celebrity
from utils.logger import logger
from utils.image_utils import download_image
from datetime import datetime, timedelta
import time

class CelebrityAvatarGenerator:
    def __init__(self):
        self.db = MongoDB()
        self.tmdb_service = TMDBService()
        self.avatar_service = LightXAvatarService()
        self.biography_service = BiographyService()
        
    def write_creative_bio(self, celebrity_data):
      return self.biography_service.generate_creative_biography(celebrity_data)

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

            # Get the full image URL
            image_url = self.tmdb_service.get_profile_image_url(details['profile_path'])

            # Generate avatar using LightX
            avatar_data = self.avatar_service.generate_avatar(image_url)
            if not avatar_data:
                logger.error(f"Failed to generate avatar for {celeb_basic['name']}")
                return

            # Create celebrity object and save to database
            celebrity = Celebrity(details, avatar_data)
            self.db.save_celebrity(celebrity.to_dict())
            
            logger.info(f"Successfully processed {celebrity.name}")
            time.sleep(Settings.RATE_LIMIT_DELAY)

        except Exception as e:
            logger.error(f"Error processing celebrity {celeb_basic['name']}: {str(e)}")
    
    def process_single_celebrity(self, celebrity_id):
        """
        Process a single celebrity by their TMDB ID
        """
        try:
            # Fetch detailed information
            details = self.tmdb_service.fetch_celebrity_details(celebrity_id)
            if not details:
                logger.error(f"Could not fetch details for celebrity ID {celebrity_id}")
                return
            
            logger.info(f"Processing celebrity: {details['name']}")

            if not details.get('profile_path'):
                logger.info(f"No profile image available for {details['name']}")
                return
              
            #** checing
            check_global_popularity = self.biography_service.check_celebrity_global_popularity(details)
            print(check_global_popularity)
            if not check_global_popularity or check_global_popularity == 'no':
              return

            # Get the full image URL
            image_url = self.tmdb_service.get_profile_image_url(details['profile_path'])
            logger.info(f"Found image URL: {image_url}")
            
            #** Generate avatar using LightX
            logger.info("Starting avatar generation with LightX...")
            avatar_data = self.avatar_service.generate_avatar(image_url, details['name'])
            
            if not avatar_data:
                logger.error(f"Failed to generate avatar for {details['name']}")
                return

            logger.info("Avatar generated successfully")
          
            transformed_name = self.biography_service.transform_name(details["name"])
            if not transformed_name:
                logger.warning(f"Could not generate creative biography for {celeb_basic['name']}")
                creative_bio = None  # Fallback to None if generation fails
            
            creative_bio = self.biography_service.generate_creative_biography(details, transformed_name)
            if not creative_bio:
                logger.warning(f"Could not generate creative biography for {celeb_basic['name']}")
                creative_bio = None  # Fallback to None if generation fails
                

            #** Create celebrity object and save to database
            celebrity = Celebrity(details, avatar_data, creative_bio, transformed_name)
            # celebrity = Celebrity(details, image_url, creative_bio, transformed_name)
            self.db.save_celebrity(celebrity.to_dict())
            
            logger.info(f"Successfully processed and saved {details['name']}")
            logger.info(f"Successfully processed and saved {transformed_name}")

        except Exception as e:
            logger.error(f"Error processing celebrity ID {celebrity_id}: {str(e)}")

    def run(self):
        try:
            celebrities = self.tmdb_service.fetch_popular_celebrities()
            for celeb in celebrities:
                self.process_single_celebrity(celeb['id'])
                # self.process_celebrity(celeb)
        finally:
            self.db.close()
    
    #** Testing
    def run_test(self):
        try:
            # Test with a specific celebrity ID
            # Example: Tom Cruise's TMDB ID is 500
            test_celebrity_id = 10859  # You can change this to any celebrity ID
            logger.info(f"Starting test with celebrity ID: {test_celebrity_id}")
            self.process_single_celebrity(test_celebrity_id)
        finally:
            self.db.close()

def main():
    generator = CelebrityAvatarGenerator()
    generator.run()

if __name__ == "__main__":
    main()