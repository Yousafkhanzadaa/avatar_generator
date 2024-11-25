# services/biography_service.py
from openai import OpenAI
from config.settings import Settings
from utils.logger import logger

client = OpenAI(api_key=Settings.OPENAI_API_KEY)

class BiographyService:
    # def __init__(self):
    #     openai.api_key = Settings.OPENAI_API_KEY
    def generate_creative_biography(self, celebrity_data):
        """
        Generates a creative, fictionalized biography based on the celebrity's real information.
        Maintains the essence of their career while creating an imaginative narrative.
        """
        try:
            # Create a detailed prompt that captures key aspects while encouraging creativity
            prompt = self._create_biography_prompt(celebrity_data)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": """You are a creative biographer who transforms real celebrity 
                    biographies into imaginative narratives. Keep the essence of their career 
                    but create fascinating fictional elements. Use metaphors, creative 
                    storytelling, and avoid direct references to real people or movies. 
                    The tone should be whimsical and engaging."""
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.6,
                max_tokens=500
            )
            
            return completion.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error generating creative biography: {str(e)}")
            return None

    def _create_biography_prompt(self, celebrity_data):
        """
        Creates a detailed prompt for the GPT model based on celebrity data.
        """
        name = celebrity_data['name']
        # known_for = celebrity_data['known_for']
        original_bio = celebrity_data['biography']
        birthday = celebrity_data['birthday']

        # Extract key career achievements and roles
        # career_highlights = [item.get('title', '') for item in known_for]
        
        # - Known for: {', '.join(career_highlights)}
        return f"""
        Transform this celebrity's biography into a creative, fictional narrative.
        Original details:
        - Career field: Actor/Actress
        - Era active: {birthday}
        - Original bio excerpt: {original_bio}...

        Create a whimsical, engaging biography that:
        1. Transforms their career journey into a metaphorical adventure
        2. Reimagines their achievements in creative ways
        3. Includes fictional elements while maintaining their career essence
        4. Avoids direct references to real movies, shows, or people
        5. Uses creative storytelling devices (metaphors, allegories)
        6. Maintains a sense of wonder and inspiration
        
        The biography should feel like a magical realism story while subtly reflecting 
        their real career path and achievements.
        """
