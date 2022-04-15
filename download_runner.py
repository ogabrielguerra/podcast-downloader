
from podcast_downloader import PodcastDownloader

url = r"https://podtail.com/en/podcast/tedtalks-audio/"

podcast_downloader = PodcastDownloader(url, 'tedtalks-audio')
podcast_downloader.download()