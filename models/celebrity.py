from datetime import datetime

class Celebrity:
    def __init__(self, tmdb_data, avatar_base64=None):
        self.tmdb_id = tmdb_data['id']
        self.name = tmdb_data['name']
        self.popularity = tmdb_data.get('popularity', 0)
        self.profile_path = tmdb_data.get('profile_path', '')
        self.biography = tmdb_data.get('biography', '')
        self.birthday = tmdb_data.get('birthday')
        self.known_for = tmdb_data.get('known_for', [])
        self.avatar = avatar_base64
        self.last_updated = datetime.now()

    def to_dict(self):
        return {
            'tmdb_id': self.tmdb_id,
            'name': self.name,
            'popularity': self.popularity,
            'profile_path': self.profile_path,
            'biography': self.biography,
            'birthday': self.birthday,
            'known_for': self.known_for,
            'avatar': self.avatar,
            'last_updated': self.last_updated
        }