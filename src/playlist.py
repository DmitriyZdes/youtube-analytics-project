import os
from googleapiclient.discovery import build
import datetime
import isodate


class PlayList:

    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        result = self.youtube.playlists().list(id=self.__playlist_id,
                                     part='contentDetails,snippet',
                                     maxResults=50,
                                     ).execute()
        self.title = result['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=",".join(self.video_ids)
                                                    ).execute()

    @property
    def playlist_id(self):
        """Геттер для приватного атрибута playlist_id"""

        return self.__playlist_id

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        max_like = 0
        best_video = ""
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like:
                best_video = video['id']
        return f"https://youtu.be/{best_video}"

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""

        duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration
