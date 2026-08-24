import re

import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class VideoLearningSpider(scrapy.Spider):
    name = "video_learning"

    async def start(self):
        yield scrapy.Request(
            url="https://web.klokah.tw/videoLearning/json/videoId.json",
            callback=self.get_video_info,
        )

    def get_video_info(self, response):
        response = response.json()

        for year, video_dict in response.items():
            for video_id, video_info in video_dict.items():
                for dialect_id, subtitle_id in video_info["subtitle"].items():
                    yield scrapy.Request(
                        url=f"https://web.klokah.tw/videoLearning/php/getText.php?tid={subtitle_id}",
                        meta={"dialect_id": dialect_id},
                        callback=self.parse_subtitles,
                    )

    def parse_subtitles(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()
        for subtitle in response:
            text = subtitle["ab"].replace("#", " ")
            mandarin = re.sub(r"[(（]\d+秒[)）]", "", subtitle["ch"]).strip()
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/text/sound/{subtitle['sn']}.mp3"],
                text=text,
                mandarin=mandarin,
                dialect_id=dialect_id,
            )
