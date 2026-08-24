import scrapy

from klokah_crawler.items import KlokahCrawlerItem
from klokah_crawler.utils.parse_read_embed import parse_read_embed


class LiveTutorialSpider(scrapy.Spider):
    name = "livetutorial"

    async def start(self):
        urls = [
            (
                dialect_id,
                f"https://web.klokah.tw/livetutorial/learn.php?d={dialect_id}&b={lesson_type}-{lesson_id}&p={part_id}",
            )
            for part_id in range(1, 11)
            for lesson_id in range(1, 4)
            for lesson_type in ["A", "B"]
            for dialect_id in [i for i in range(1, 44) if i != 12]
        ]
        for dialect_id, url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.get_iframe_url,
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def get_iframe_url(self, response):
        for url in response.css("div.tutoframe-inner::attr(data-src)").getall():
            if "read_embed" in url:
                yield scrapy.Request(
                    url=url,
                    meta={"dialect_id": response.meta["dialect_id"]},
                    callback=parse_read_embed,
                )

        for sentence in response.css("#read-main > div"):
            sentence_text = " ".join(sentence.css("div.word::text").getall())
            translated_text = sentence.css("div.read-sentence.Ch::text").get()
            audio_data_value = sentence.css(".read-play-btn::attr(data-value)").get()
            audio_url = response.css(
                f'audio[data-value="{audio_data_value}"] > source::attr(src)'
            ).get()

            yield KlokahCrawlerItem(
                audio_url=[audio_url],
                text=sentence_text,
                mandarin=translated_text,
                dialect_id=response.meta["dialect_id"],
            )
