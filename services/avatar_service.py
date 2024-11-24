import requests
from config.settings import Settings
from utils.logger import logger
from utils.image_utils import encode_image_to_base64
from io import BytesIO

class AvatarService:
    def __init__(self):
        self.headers = {
            'api-key': Settings.DEEPAI_API_KEY
        }

    def generate_avatar(self, image_data):
        try:
            # Convert image data to base64
            image_base64 = encode_image_to_base64(image_data)
            if not image_base64:
                return None

            # Make request to DeepAI
            response = requests.post(
                Settings.DEEPAI_TOONIFY_URL,
                headers=self.headers,
                data={'image': image_base64}
            )
            response.raise_for_status()
            
            # Get the avatar URL from response
            avatar_url = response.json()['output_url']
            
            # Download the avatar
            avatar_response = requests.get(avatar_url)
            avatar_response.raise_for_status()
            
            return BytesIO(avatar_response.content)
        except Exception as e:
            logger.error(f"Error generating avatar: {str(e)}")
            return None