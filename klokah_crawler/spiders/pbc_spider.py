import scrapy

from klokah_crawler.items import KlokahCrawlerItem

DIALECT_ID_LANGUAGE_ID_MAP = {
    3: 1,
    6: 2,
    13: 3,
    14: 4,
    16: 5,
    22: 6,
    24: 7,
    28: 8,
    33: 9,
    34: 10,
    35: 11,
    36: 15,
    37: 16,
    38: 12,
    42: 13,
    43: 14,
}


class PBCSpider(scrapy.Spider):
    name = "pbc"

    async def start(self):
        yield scrapy.Request(
            url="https://web.klokah.tw/pbc/",
            callback=self.get_book_url,
        )

    def get_book_url(self, response):
        for pbid in response.css("div.pbitem::attr(pbid)").getall():
            for dialect_id, language_id in DIALECT_ID_LANGUAGE_ID_MAP.items():
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/pbc/book/online/get_data.php?id={pbid}&lid={language_id}",
                    meta={"dialect_id": dialect_id},
                )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()
        for page_metadata in response["pages"].values():
            audio_path = page_metadata["audio_url"]
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/text/sound/{audio_path}.mp3"],
                text=page_metadata["ab"],
                mandarin=page_metadata["ch"],
                dialect_id=dialect_id,
            )
