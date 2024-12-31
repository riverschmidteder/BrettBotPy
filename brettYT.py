from googleapiclient.discovery import build
import random


class RandomVideo:

    def __init__(self, channel_id, api_key):
        self.channel_id = channel_id
        self.api_key = api_key

    def get_channel_videos(self):
        youtube = build("youtube", "v3", developerKey=self.api_key)
        request = youtube.search().list(
            # specifies that the resource object
            part="id",
            # channel_id goes here
            channelId=self.channel_id,
            maxResults=50,
            type="video",
            fields="items(id(videoId))"
        )
        response = request.execute()
        video_ids = [item["id"]["videoId"] for item in response["items"]]

        return video_ids

    def get_random_video_link(self):
        video_ids = self.get_channel_videos()
        random_video_id = random.choice(video_ids)
        video_link = f"https://www.youtube.com/watch?v={random_video_id}"
        return video_link
