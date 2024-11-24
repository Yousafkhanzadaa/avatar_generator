import base64
from io import BytesIO
import requests
from utils.logger import logger

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        logger.error(f"Error downloading image from {url}: {str(e)}")
        return None

def encode_image_to_base64(image_data):
    try:
        return base64.b64encode(image_data.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        return None