import scrapy

from klokah_crawler.utils.parse_read_embed import parse_read_embed


class CuPracticeSpider(scrapy.Spider):
    name = "cu_practice"

    async def start(self):
        yield scrapy.Request(
            url="https://web.klokah.tw/extension/cu_practice/textId.json",
            callback=self.get_read_embed_url,
        )

    def get_read_embed_url(self, response):
        response = response.json()
        for dialect_id, read_embed_id_list in response.items():
            for read_embed_id in read_embed_id_list:
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/text/read_embed.php?tid={read_embed_id}&mode=1",
                    meta={"dialect_id": dialect_id},
                    callback=parse_read_embed,
                )
