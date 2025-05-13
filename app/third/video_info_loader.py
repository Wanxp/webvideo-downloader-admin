from app.downloader.api import getPlatformType


class VideoInfo:
    def __init__(self, linksurl: str,
                 title: str,
                 description: str,
                 thumbnail_url: str, **kwargs):
        """
        :param linksurl: 视频链接
        :param title: 视频标题
        :param description: 视频描述
        :param thumbnail_url: 视频缩略图链接
        :param kwargs: 其他参数
        """
        self.linksurl = linksurl
        self.platform_type = getPlatformType(linksurl)
        self.title = title
        self.description = description
        self.thumbnail_url = thumbnail_url

    def __repr__(self):
        return f"VideoInfo(linksurl={self.linksurl}, title={self.title}, description={self.description}, thumbnail_url={self.thumbnail_url})"



class VideoInfoLoader:
    def __init__(self, linksurl: str, headers: dict = {}, cookies: dict = {}):
        self.linksurl = linksurl
        self.headers = headers
        self.cookies = cookies
        self.video_info = None

    def load_video_info(self):



    def get_video_info(self):
        return self.video_info