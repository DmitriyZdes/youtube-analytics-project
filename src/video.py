import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Video:

    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id).execute()
            if 'items' in video_response and video_response['items']:
                self.video_title = video_response['items'][0]['snippet']['title']
                self.video_url = f'https://www.youtube.com/watch?v={video_id}'
                self.view_count = video_response['items'][0]['statistics']['viewCount']
                self.likes_count = video_response['items'][0]['statistics']['likeCount']
            else:
                self.video_title = None
                self.likes_count = None
                self.view_count = None
                self.video_url = None
        except HttpError:
                self.video_title = None
                self.video_url = None
                self.view_count = None
                self.likes_count = None

    def __str__(self):
        return f'{self.video_title}'

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
