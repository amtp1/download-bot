import traceback
from dataclasses import dataclass

from pytube import YouTube
from pytube.exceptions import VideoUnavailable

@dataclass
class ContentMeta:
    is_error: bool
    message: str
    stream: str

    author: str
    title: str

    def __init__(self, is_error=False, message="", stream="", author="", title=""):
        self.is_error = is_error
        self.message = message
        self.stream = stream
        self.author = author
        self.title = title

class YoutubeDownloader:
    @staticmethod
    def download(url: str, is_audio: bool = False, itag: int = None) -> dict:
        try:
            yt: YouTube = YouTube(url)  # Init YouTube class.
        except TypeError:
            return ContentMeta(is_error=True, message="Paste new link👇")

        if is_audio:
            try:
                stream = yt.streams.filter(only_audio=True).desc().first()
            except Exception as e:
                traceback.print_exc()
                return ContentMeta(is_error=True, message=e)
        else:
            try:
                stream = yt.streams.get_by_itag(itag)
            except VideoUnavailable as e:
                return ContentMeta(is_error=True, message=e)
            except Exception as e:
                traceback.print_exc()
                return ContentMeta(is_error=True, message=e)
        # Convert to mb value size.
        mb_size: float = float(stream.filesize / 8 / 8 / 16 / 1024)
        if mb_size < 1024:
            # Format in string file size.
            str_filesize: str = "{:.2}MB".format(mb_size)
        elif mb_size > 1024:
            _mb_size = mb_size / 1024
            # Format in string file size.
            str_filesize: str = "{:.2}GB".format(_mb_size)
        if mb_size > 50:
            return ContentMeta(is_error=True, message=f"Video size ({str_filesize}) large then 50MB")
        else:
            return ContentMeta(stream=stream.url, author=yt.author, title=yt.title)
