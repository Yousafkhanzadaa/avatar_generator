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
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error generating creative biography: {str(e)}")
            return None
          
    def check_celebrity_global_popularity(self, celebrity_data):
      """
      Checks if a celebrity has a global popularity with high teen following.
      
      Args:
          celebrity_data (dict): Dictionary containing celebrity information
      
      Returns:
          str: "yes" or "no" indicating global popularity status
      """
      try:
          # Create the detailed prompt for checking global popularity
          prompt = self.check_global_popularity(celebrity_data)
          
          response = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[{
                  "role": "system",
                  "content": """You are an expert in global celebrity culture and fan demographics. 
                  Your task is to rigorously evaluate a celebrity's global fame and teenage fan appeal. 
                  Be extremely selective and critical in your assessment."""
              }, {
                  "role": "user",
                  "content": prompt
              }],
              temperature=0.2,  # Low temperature for more deterministic response
              max_tokens=10     # Very low token count to ensure concise yes/no
          )
          
          # Extract and clean the response
          result = response.choices[0].message.content.strip().lower()
          
          # Ensure only "yes" or "no" is returned
          return "yes" if result == "yes" else "no"
      
      except Exception as e:
          logger.error(f"Error checking celebrity global popularity: {str(e)}")
          return "no"

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
        
    def check_global_popularity(self, celebrity_data):
      """
      Determines if a celebrity has a very high global fan following, 
      especially among teenagers.
      
      Args:
          celebrity_data (dict): Dictionary containing celebrity information
      
      Returns:
          str: "yes" if the celebrity is globally famous with high teen following,
              "no" otherwise
      """
      name = celebrity_data['name']
      print(name)
      biography = celebrity_data['biography']
      birthday = celebrity_data['birthday']
      popularity = celebrity_data['popularity']

      # Prompt designed to evaluate global popularity and teen appeal
      popularity_prompt = f"""
      Analyze the following celebrity details and determine if they have:
      1. EXTREME global fame (worldwide recognition)
      2. MASSIVE fan following
      
      Celebrity Name: {name}
      TMDB Popularity Score: {popularity}
      birthday: {birthday}
      Biography Excerpt: {biography}

      IMPORTANT RULES:
      - ONLY respond with "yes" IF:
        a) Celebrity is GLOBALLY recognized
      - ONLY respond with "yes" for truly GLOBAL icons
      - Respond with "no" for any doubt or less than EXTREME fame
      - Consider factors like social media following, global movie/music success, 
        and widespread cultural impact
      - Be EXTREMELY selective about who qualifies as a global teen and middle age icon
      """
      
      return popularity_prompt
