import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class CuPracticeWordSpider(scrapy.Spider):
    name = "cu_practice_word"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/extension/cu_data/get_data.php?did={dialect_id}",
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        for lesson_metadata in response.json()["lesson"].values():
            lesson_no = lesson_metadata["no"]
            for word_metadata in lesson_metadata["word"].values():
                word_order = word_metadata["word_order"]
                word_metadata["word_ab"] = word_metadata["word_ab"].replace(
                    "&rsquo;", "’"
                )

                yield KlokahCrawlerItem(
                    audio_url=[
                        f"https://web.klokah.tw/extension/cu_data/audio/{dialect_id}/{dialect_id}_{lesson_no}_V{word_order}.mp3"
                    ],
                    text=word_metadata["word_ab"],
                    mandarin=word_metadata["word_ch"],
                    dialect_id=dialect_id,
                )
