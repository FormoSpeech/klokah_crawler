import scrapy

from klokah_crawler.items import KlokahCrawlerItem

twelve_dialect_map = [
    None,
    24,
    23,
    25,
    26,
    27,
    16,
    17,
    18,
    19,
    43,
    42,
    None,
    28,
    30,
    22,
    20,
    21,
    6,
    7,
    8,
    9,
    5,
    11,
    12,
    13,
    10,
    15,
    14,
    41,
    35,
    37,
    36,
    44,
    31,
    32,
    33,
    34,
    3,
    2,
    1,
    4,
    29,
    38,
]
audio_url = "https://web.klokah.tw/ninew/sound"


class TwelveSpider(scrapy.Spider):
    name = "twelve"

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
            sentence_text = sentence["ab"]
            sentence_translated = sentence["chinese"]
            sentence_order = sentence["order"]
            sentence_audio = f"{audio_url}/{twelve_version_dialect_id:02d}/{level:02d}/{class_id:02d}-B-{sentence_order}.mp3"

            yield KlokahCrawlerItem(
                audio_url=[sentence_audio],
                text=sentence_text,
                mandarin=sentence_translated,
                dialect_id=dialect_id,
            )
