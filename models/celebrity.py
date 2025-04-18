from datetime import datetime

class Celebrity:
    def __init__(self, tmdb_data, avatar_base64=None, creative_bio=None, transformed_name=None):
        self.tmdb_id = tmdb_data['id']
        self.name = tmdb_data['name']
        self.new_name = tmdb_data['name'] if (transformed_name == None) else transformed_name
        self.popularity = tmdb_data.get('popularity', 0)
        self.profile_path = tmdb_data.get('profile_path', '')
        self.biography = tmdb_data.get('biography', '') if (creative_bio == None) else creative_bio
        self.birthday = tmdb_data.get('birthday')
        self.known_for = tmdb_data.get('known_for', [])
        self.avatar = avatar_base64
        self.last_updated = datetime.now()

    def to_dict(self):
        return {
            'tmdb_id': self.tmdb_id,
            'name': self.name,
            'new_name': self.new_name,
            'popularity': self.popularity,
            'profile_path': self.profile_path,
            'biography': self.biography,
            'birthday': self.birthday,
            'known_for': self.known_for,
            'avatar': self.avatar,
            'last_updated': self.last_updated
        }