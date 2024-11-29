# services/avatar_service.py
import requests
import json
import time
from config.settings import Settings
from utils.logger import logger
from utils.image_utils import encode_image_to_base64
from io import BytesIO
import base64

class LightXAvatarService:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': Settings.LIGHTX_API_KEY
        }
        
    def _convert_to_base64(self, image_data):
        """Convert BytesIO image data to base64 string"""
        try:
            # Convert BytesIO to base64
            base64_data = base64.b64encode(image_data.getvalue())
            # Convert bytes to string
            return base64_data.decode('utf-8')
        except Exception as e:
            logger.error(f"Error converting image to base64: {str(e)}")
            return None

    def _check_order_status(self, order_id):
        """Check the status of an avatar generation order"""
        payload = {"orderId": order_id}
        
        for attempt in range(Settings.MAX_RETRIES):
            try:
                response = requests.post(
                    Settings.LIGHTX_STATUS_URL,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                logger.info(f"Status check attempt {attempt + 1}: {data}")
                
                # Check if the response is successful
                if data.get('statusCode') == 2000:
                    body = data.get('body', {})
                    status = body.get('status')
                    
                    if status == 'active' and body.get('output'):
                        logger.info("Avatar generation completed")
                        return body['output']
                    elif status == 'failed':
                        logger.error("Avatar generation failed")
                        return None
                    else:
                        logger.info(f"Status: {status}. Waiting...")
                        time.sleep(Settings.STATUS_CHECK_DELAY)
                else:
                    logger.error(f"Unexpected status code: {data.get('statusCode')}")
                    return None
                
            except Exception as e:
                logger.error(f"Error checking order status: {str(e)}")
                time.sleep(Settings.STATUS_CHECK_DELAY)
        
        logger.error("Max retries reached while checking order status")
        return None

    def generate_avatar(self, image_url):
        """Generate avatar using LightX API"""
        try:
            # Prepare the payload for avatar generation
            payload = {
                "imageUrl": image_url,
                "styleImageUrl": "",
                "textPrompt": "Photorealistic high-resolution portrait of Daniel Radcliffe, professional studio headshot with precise facial details, accurate skin texture, and true-to-life facial features, soft diffused studio lighting minimizing harsh shadows, neutral background, DSLR-quality image with shallow depth of field, capturing subject's signature facial structure and expression, smart casual attire, balanced color grading, natural skin tones, minimal post-processing, shot from slightly elevated angle to enhance facial symmetry, lighting emphasizing cheekbones and facial contours, maintaining original subject's distinctive characteristics."
                # "textPrompt": "A high-quality professional headshot portrait of a celebrity precise facial details, soft studio lighting, neutral background, and crisp image quality, capturing a confident yet natural expression with true-to-life skin tones, shot on a professional DSLR with shallow depth of field, showcasing shoulders and smart casual attire, maintaining a balanced, flattering composition that emphasizes facial features with minimal post-processing and a subtle, professional smile."
            }

            # Initialize avatar generation
            response = requests.post(
                Settings.LIGHTX_AVATAR_URL,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            logger.info(f"Initial generation response: {response_data}")
            
            # Check if the response is successful
            if response_data.get('statusCode') == 2000:
                body = response_data.get('body', {})
                order_id = body.get('orderId')
                max_retries = body.get('maxRetriesAllowed', Settings.MAX_RETRIES)
                avg_time = body.get('avgResponseTimeInSec', Settings.STATUS_CHECK_DELAY)
                
                if not order_id:
                    logger.error("No order ID received from LightX API")
                    return None
                
                # Update settings based on API response
                Settings.MAX_RETRIES = max_retries
                Settings.STATUS_CHECK_DELAY = avg_time
                
                logger.info(f"Got order ID: {order_id}. Waiting for completion...")
                
                # Wait for initial processing time
                time.sleep(avg_time)
                
                # Check status and wait for completion
                avatar_url = self._check_order_status(order_id)
                
                if not avatar_url:
                    logger.error("Failed to get avatar URL from LightX API")
                    return None

                # Download the generated avatar
                logger.info(f"Downloading avatar from: {avatar_url}")
                avatar_response = requests.get(avatar_url)
                avatar_response.raise_for_status()
                
                # Convert to BytesIO
                image_data = BytesIO(avatar_response.content)
                
                # Convert to base64
                base64_data = self._convert_to_base64(image_data)
                if base64_data:
                    logger.info("Successfully converted avatar to base64")
                    return base64_data
                
                return None
            else:
                logger.error(f"Avatar generation failed with status code: {response_data.get('statusCode')}")
                return None

        except Exception as e:
            logger.error(f"Error generating avatar with LightX: {str(e)}")
            return None