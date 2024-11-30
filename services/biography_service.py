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
              temperature=0.6,  # Low temperature for more deterministic response
              max_tokens=10     # Very low token count to ensure concise yes/no
          )
          
          # Extract and clean the response
          result = response.choices[0].message.content.strip().lower()
          
          print(result)
          print(result)
          print(result)
          
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
        - Career field: Celebrity
        - Name: {name}
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
#       popularity_prompt = f"""
# Analyze the following celebrity details and determine if they meet the criteria for:
# 1. EXTREME global fame (worldwide recognition)
# 2. MASSIVE fan following

# Celebrity Name: {name}
# Biography: {biography}

# IMPORTANT RULES:
# - Respond with only "yes" if the celebrity is globally recognized and has a massive fan base across multiple regions or demographics.
# - Consider these factors:
#   a) International box office success or widespread streaming popularity
#   b) Significant cultural impact or iconic status
#   c) Large and active social media following
#   d) Longevity or dominance in their field
# - Respond with "no" if the celebrity's fame is largely regional, niche, or lacks consistent global impact.
# - Be selective, but ensure truly global icons are recognized appropriately.
# """

      popularity_prompt = f"""Comprehensive Celebrity Global Fame Assessment

      Analyze the following celebrity details to determine their global recognition and significance:

      Evaluation Criteria:
      1. Global Reach and Recognition
      2. Cultural Impact
      3. Measurable Influence
      4. Fan Engagement

      Celebrity Name: {name}
      Biography: {biography}

      Evaluation Guidelines:
      - Holistically assess the celebrity's global prominence
      - Consider multiple dimensions of fame:
        * International media presence
        * Cross-cultural appeal
        * Sustained career achievements
        * Impact beyond their primary field of work

      Scoring Factors:
      a) Worldwide recognition across different continents
      b) Substantial international media coverage
      c) Global social media following (over 5 million combined platforms)
      d) Breakthrough performances or achievements
      e) Awards and critical acclaim
      f) Influence on global pop culture
      g) Humanitarian or philanthropic contributions
      h) Endorsement deals and brand recognition
      i) Longevity in their career
      j) Ability to attract international audience/fans

      Decision Process:
      - Respond only "YES" if the celebrity demonstrates:
        * Significant global recognition
        * Proven impact across multiple regions
        * Substantial fan base
        * Notable achievements in their field

      - Respond only "NO" only if:
        * Fame is extremely limited
        * Minimal international recognition
        * Lack of substantial global impact

      Nuanced Approach:
      - Recognize that fame is multifaceted
      - Consider subjective elements of cultural significance
      - Be inclusive of diverse talents and achievements
      - Avoid overly restrictive criteria

      Provide a brief justification for your decision that highlights key global recognition factors. only response "yes" or "no" nothing else."""
      
      return popularity_prompt
