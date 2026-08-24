import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class DialogueSpider(scrapy.Spider):
    name = "dialogue"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/dialogue/json/SN112{dialect_id:02}.json",
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for lesson_tid in response["S1"]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/dialogue/php/getDiaData.php?tid={lesson_tid}",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_get_dia,
            )

        for lesson_name, lesson_tid_list in response["S2"].items():
            if lesson_name == "group":
                continue
            yield scrapy.Request(
                url=f"https://web.klokah.tw/dialogue/php/getDiaData.php?tid={lesson_tid_list[0]}",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_get_dia,
            )

        for lesson_name, lesson_tid_list in response["S3"].items():
            if lesson_name == "group":
                continue
            yield scrapy.Request(
                url=f"https://web.klokah.tw/dialogue/php/getDiaData.php?tid={lesson_tid_list[0]}",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_get_dia,
            )

    def parse_get_dia(self, response):
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
