import scrapy

from klokah_crawler.items import KlokahCrawlerItem
from klokah_crawler.utils.parse_read_embed import parse_read_embed


class EssaySpider(scrapy.Spider):
    name = "essay"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/essay/json/ES112{dialect_id:02}.json",
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for season in ["S1", "S2"]:
            for lesson_name, lesson_tid_list in response[season].items():
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/essay/php/getEssay.php?tid={lesson_tid_list[0]}",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=self.parse_get_essay,
                )

                sentece_practice_idx = 2
                if lesson_name in ["L9", "L10", "L11", "L12"]:
                    sentece_practice_idx = 1

                yield scrapy.Request(
                    url=f"https://web.klokah.tw/text/read_embed.php?tid={lesson_tid_list[sentece_practice_idx]}&mode=1",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=parse_read_embed,
                )

    def parse_get_essay(self, response):
        dialect_id = response.meta["dialect_id"]
        for sentence in response.json():
            audio_url = []
            if sentence["snd"]:
                audio_path = sentence["sn"]
                audio_url.append(f"https://web.klokah.tw/text/sound/{audio_path}.mp3")

            yield KlokahCrawlerItem(
                audio_url=audio_url,
                text=sentence["ab"],
                mandarin=sentence["ch"],
                dialect_id=dialect_id,
            )
