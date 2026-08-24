import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class ParentChildSpider(scrapy.Spider):
    name = "parent_child"

    def start_requests(self):
        yield scrapy.Request(
            url="https://web.klokah.tw/parent-child/json/tid.json",
            callback=self.get_topic_info,
        )

    def get_topic_info(self, response):
        response = response.json()
        for dialect_id in range(1, 44):
            if f"D{dialect_id}" in response:
                dialect_topic_info = response[f"D{dialect_id}"]

                # TODO: also have word, maybe later we can add them too
                for lesson_id, topic_id_list in dialect_topic_info["sentence"].items():
                    for topic_id in topic_id_list:
                        yield scrapy.Request(
                            url=f"https://web.klokah.tw/parent-child/php/get.php?tid={topic_id}",
                            meta={"dialect_id": dialect_id},
                            callback=self.parse_topic,
                        )

    def parse_topic(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()
        for sentence in response:
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/text/sound/{sentence['sn']}.mp3"],
                text=sentence["ab"],
                mandarin=sentence["ch"],
                dialect_id=dialect_id,
            )
