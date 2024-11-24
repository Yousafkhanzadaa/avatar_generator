from pymongo import MongoClient
from config.settings import Settings
from utils.logger import logger

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Settings.MONGODB_URI)
        self.db = self.client.celebrity_database
        self.celebrities = self.db.celebrities

    def save_celebrity(self, celebrity_data):
        try:
            return self.celebrities.update_one(
                {'tmdb_id': celebrity_data['tmdb_id']},
                {'$set': celebrity_data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error saving celebrity to MongoDB: {str(e)}")
            return None

    def get_celebrity(self, tmdb_id):
        return self.celebrities.find_one({'tmdb_id': tmdb_id})

    def close(self):
        self.client.close()