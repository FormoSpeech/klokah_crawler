import scrapy

from klokah_crawler.utils.parse_read_embed import parse_read_embed


class EssayWordSpider(scrapy.Spider):
    name = "essay_word"

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
                if lesson_name in ["L9", "L10", "L11", "L12"]:
                    continue
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/text/read_embed.php?tid={lesson_tid_list[1]}&mode=1",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=parse_read_embed,
                )
