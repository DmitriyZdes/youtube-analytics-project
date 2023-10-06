import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.url = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.total_views = channel['items'][0]['statistics']['viewCount']


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        data = self.get_service().channels().list(id="UC44oy3QadzoUZt7G0DDf5DQ", part='snippet,statistics,contentDetails').execute()
        print(data)


    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""

        _api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=_api_key)
        return youtube


    def to_json(self, filename):
        """Сохраняет атрибуты экземпляра в файл json"""

        dict_to_json = {"channel_id": self.channel_id, "title": self.title, "description": self.description, "url": self.url, "subscriber": self.subscriber_count, "total_views": self.total_views}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(dict_to_json, file)


    def __str__(self):
        """Информация о название канала и его ссылка"""

        return f'{self.title} {self.url}'


    def __add__(self, other):
        """Сложение количества подписчиков каналов"""

        return int(self.subscriber_count) + int(other.subscriber_count)


    def __sub__(self, other):
        """Вычитание количества подписчиков каналов"""

        return int(self.subscriber_count) - int(other.subscriber_count)


    def __eq__(self, other):
        """Сравнивает количество подписчиков каналов"""

        return self.subscriber_count == other.subscriber_count

