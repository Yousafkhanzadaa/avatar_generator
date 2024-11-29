import base64
from io import BytesIO
import requests
from utils.logger import logger
from PIL import Image

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
      
def reseize_base64_Image(base64_img):
    """
    Resize a Base64-encoded image to the specified dimensions.
    
    Args:
        base64_image (str): The Base64-encoded image string.
        width (int): The desired width of the resized image.
        height (int): The desired height of the resized image.

    Returns:
        str: The resized image as a Base64-encoded string.
    """
    try:
      max_size = 640
      
      # Decode the Base64 image to binary
      image_data = base64.b64decode(base64_img)

      # Open the image using Pillow
      image = Image.open(io.BytesIO(image_data))

      # Calculate the new size preserving aspect ratio
      width, height = image.size
      if width > height:
          new_width = max_size
          new_height = int((max_size / width) * height)
      else:
          new_height = max_size
          new_width = int((max_size / height) * width)

      # Resize the image
      resized_image = image.resize((new_width, new_height), Image.LANCZOS)

      # Save the resized image to a bytes buffer
      buffered = io.BytesIO()
      resized_image.save(buffered, format="jpeg")

      # Encode the resized image back to Base64
      resized_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        return None