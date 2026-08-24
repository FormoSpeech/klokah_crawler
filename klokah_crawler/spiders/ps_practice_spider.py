import scrapy

from klokah_crawler.utils.parse_read_embed import parse_read_embed


class PsPracticeSpider(scrapy.Spider):
    name = "ps_practice"

    async def start(self):
        urls = [
            (
                dialect_id,
                f"https://web.klokah.tw/extension/ps_practice/index.php?d={dialect_id}&l={lesson_id}&view=story",
            )
            for lesson_id in range(1, 11)
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
        yield scrapy.Request(
            url=response.css("#text-frame::attr(src)").get(),
            meta={"dialect_id": response.meta["dialect_id"]},
            callback=parse_read_embed,
        )
