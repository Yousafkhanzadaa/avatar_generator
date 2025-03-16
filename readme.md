# Celebrity Avatar Generator - Detailed Explanation
## Project Overview
# _________
_nerdy_
# gggghhgffffg
The application fetches celebrity data from TMDB (The Movie Database), generates cartoon-style avatars from their profile pictures, and stores everything in MongoDB.

## Project Structure

```plaintext
celebrity_avatar/
├── ── config/               # Configuration management
├── database/             # Database operations
├── services/             # External API interactions
├── models/               # Data structures
├── utils/                # Helper functions
├── .env                  # Environment variables
└── main.py               # Application entry point
```
# 
# 
# 
# 


## Detailed Flow

### Initialization Flow
1. The application starts in `main.py`.
2. Loads environment variables from `.env`.
3. Sets up logging.
4. Initializes services:
   - MongoDB connection
   - TMDB API service
   - Avatar generation service

### Data Processing Flow

```plaintext
Start
  │
  ├─► Fetch Popular Celebrities (TMDB)
  │     │
  │     ├─► For each celebrity:
  │           │
  │           ├─► Check if update needed
  │           │     (Skip if updated within 7 days)
  │           │
  │           ├─► Fetch detailed info
  │           │
  │           ├─► Download profile image
  │           │
  │           ├─► Generate avatar
  │           │
  │           └─► Save to MongoDB
  │
  └─► End
```


## Component Details

### Configuration (`config/settings.py`)
```python
class Settings:
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')
```

- Centralizes all configuration.
- Loads sensitive data from environment variables.
- Defines constants and API endpoints.

### Database Operations (`database/mongodb.py`)
```python
class MongoDB:
    def save_celebrity(self, celebrity_data):
        # Upsert operation (update if exists, insert if not)
```

- Handles all MongoDB interactions.
- Provides CRUD operations for celebrity data.
- Manages database connections.

### TMDB Service (`services/tmdb_service.py`)
```python
class TMDBService:
    def fetch_popular_celebrities(self, num_pages=5):
        # Fetches multiple pages of celebrity data
```

- Fetches celebrity lists and details.
- Handles TMDB API pagination.
- Manages rate limiting.

### Avatar Service (`services/avatar_service.py`)
```python
class AvatarService:
    def generate_avatar(self, image_data):
        # Converts profile picture to avatar
```

- Handles avatar generation using DeepAI.
- Processes image data.
- Manages avatar API interactions.

## Data Flow Example

Let's follow the journey of processing one celebrity:

1. **Initial Fetch**:
```python
# In TMDBService
celebrities = self.tmdb_service.fetch_popular_celebrities()
```
# Returns: [{"id": 123, "name": "John Doe", ...}, ...]


2. **Detail Check**:
```python
# In CelebrityAvatarGenerator
details = self.tmdb_service.fetch_celebrity_details(celeb_basic['id'])
```
# Returns: {"id": 123, "biography": "...", "profile_path": "/xyz.jpg"}


3. **Image Processing**:
```python
# Download profile image
image_url = self.tmdb_service.get_profile_image_url(details['profile_path'])
image_data = download_image(image_url)
```

# Generate avatar
avatar_data = self.avatar_service.generate_avatar(image_data)


4. **Data Storage**:
```python
# Create celebrity object
celebrity = Celebrity(details, avatar_data)
```

# Save to MongoDB
self.db.save_celebrity(celebrity.to_dict())


## Expected Results

### MongoDB Document Structure
```json
{
  "tmdb_id": 123,
  "name": "John Doe",
  "popularity": 84.5,
  "profile_path": "/xy
```z.jpg",
  "biography": "Actor known for...",
  "birthday": "1970-01-01",
  "known_for": ["Movie1", "Movie2"],
  "avatar": "base64_encoded_avatar_image",
  "last_updated": "2024-11-24T10:00:00Z"
}


### Performance Expectations
- Processes ~100 celebrities (5 pages × 20 celebrities).
- Takes 1-2 minutes per celebrity (due to rate limiting).
- Total runtime: ~2-3 hours for full dataset.

## Error Handling

The code handles various error scenarios:

1. **API Failures**:
```python
try:
    response = requests.get(url)
    response.raise_for_status()
except Exception as e:
    logger.error(f"API Error: {str(e)}")
```


2. **Image Processing Errors**:
```python
if not image_data:
    logger.info(f"Skipping {name} - no profile image")
    return
```


3. **Database Errors**:
```python
try:
    self.db.save_celebrity(celebrity.to_dict())
except Exception as e:
    logger.error(f"Database Error: {str(e)}")
```


## Usage and Running

1. **Setup**:
```bash
# Create virtual environment
python -m venv v```env
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
```

# Install dependencies
pip install -r requirements.txt


2. **Configuration**:
```env
TMDB_API_KEY=your_tmdb_api_key
MONGODB_URI=mongodb://localhost:27017
DEEPAI_API_KEY=your_deepai_api_key
```


3. **Running**:
```bash
python main.py
```


## Monitoring and Logs

The application generates detailed logs:
```plaintext
2024-11-24 10:00:00 - INFO - Fetched page 1 of celebrities
2024-11-24 10:00:01 - INFO - Processing celebrity: John Doe
2024-11-24 10:00:30 - INFO - Successfully generated avatar
```


## Output Validation

You can verify the results by:
1. Checking MongoDB for new entries.
2. Verifying avatar generation quality.
3. Monitoring the logs for any errors.
4. Checking rate limit compliance.

- [ ] this is working 😀