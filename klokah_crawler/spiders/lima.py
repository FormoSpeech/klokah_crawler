import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class LimaSpider(scrapy.Spider):
    name = "lima"

    async def start(self):
        urls = [
            (
                dialect_id,
                f"https://web.klokah.tw/lima/json/{dialect_id}/{lesson_id}.json",
            )
            for lesson_id in range(1, 8)
            for dialect_id in [i for i in range(1, 44) if i != 12]
        ]
        for dialect_id, url in urls:
            yield scrapy.Request(
                url=url,
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for category in ["conversation", "question", "story", "vocabulary"]:
            for item in response[category]:
                audio_name = item["audio"]
                if category == "story":
                    audio_name += "-18"
                yield KlokahCrawlerItem(
                    audio_url=[
                        f"https://web.klokah.tw/lima/sound/{dialect_id}/{category}/{audio_name}.mp3"
                    ],
                    text=item["ab"],
                    mandarin=item["ch"],
                    dialect_id=dialect_id,
                )
