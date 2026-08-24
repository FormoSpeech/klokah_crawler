import scrapy

from klokah_crawler.items import KlokahCrawlerItem
from klokah_crawler.spiders.twelve_spider import audio_url, twelve_dialect_map


class TwelveWordSpider(scrapy.Spider):
    name = "twelve_word"

    async def start(self):
        urls = [
            (
                class_id,
                level,
                dialect_id,
                f"https://web.klokah.tw/twelve/php/getTextNew.php?d={twelve_dialect_map[dialect_id]}&l={level}&c={class_id}",
            )
            for class_id in range(1, 11)
            for level in range(1, 10)
            for dialect_id in [i for i in range(1, 44) if i != 12]
        ]
        for class_id, level, dialect_id, url in urls:
            yield scrapy.Request(
                url=url,
                meta={
                    "twelve_version_dialect_id": twelve_dialect_map[dialect_id],
                    "dialect_id": dialect_id,
                    "level": level,
                    "class_id": class_id,
                },
            )

    def parse(self, response):
        response_json = response.json()
        twelve_version_dialect_id = response.meta["twelve_version_dialect_id"]
        dialect_id = response.meta["dialect_id"]
        level = response.meta["level"]
        class_id = response.meta["class_id"]

        title = response_json["title"]
        title_translated = response_json["titleCh"]
        title_audio = f"{audio_url}/{twelve_version_dialect_id:02d}/{level:02d}/{class_id:02d}-A.mp3"

        yield KlokahCrawlerItem(
            audio_url=[title_audio],
            text=title,
            mandarin=title_translated,
            dialect_id=dialect_id,
        )

        for sentence in response_json["sentence"]:
            word_index = 1
            for word in sentence["word"]:
                if len(word["ch"]) > 0:
                    word_audio = f"{audio_url}/{twelve_version_dialect_id:02d}/{level:02d}/{class_id:02d}-C-{sentence['order']}-{word_index}.mp3"
                    word_text = word["ab"]
                    word_translated = word["ch"]

                    yield KlokahCrawlerItem(
                        audio_url=[word_audio],
                        text=word_text,
                        mandarin=word_translated,
                        dialect_id=dialect_id,
                    )
                    word_index += 1
