import scrapy
import xmltodict

from klokah_crawler.items import KlokahCrawlerItem
from klokah_crawler.utils.parse_sp import TYPE_ID_TYPE_NAME_MAP, parse_metadata


class SpJuniorSpider(scrapy.Spider):
    name = "sp_junior"

    async def start(self):
        yield scrapy.Request(
            url="https://web.klokah.tw/extension/sp_data/junior/classView.xml",
            callback=self.get_class_xml,
        )

    def get_class_xml(self, response):
        for item in response.xpath("/dataroot/item"):
            type_id = item.xpath("typeId/text()").get()
            class_id = item.xpath("classId/text()").get()

            for dialect_id in [i for i in range(1, 44) if i != 12]:
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/extension/sp_data/junior/{dialect_id}/{class_id}.xml",
                    meta={
                        "dialect_id": dialect_id,
                        "type_id": type_id,
                    },
                )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        type_id = response.meta["type_id"]
        for item in response.xpath("/dataroot/item").getall():
            item = xmltodict.parse(item)["item"]
            parsed_metadata_list = parse_metadata(
                item, type_id, only_one_audio=(type_id == "2")
            )
            if parsed_metadata_list is None:
                continue

            for parsed_metadata in parsed_metadata_list:
                audio_name = parsed_metadata["audio_name"]
                yield KlokahCrawlerItem(
                    audio_url=[
                        f"https://klokah.tw/extension/sp_junior/sound/{dialect_id}/{type_id}{TYPE_ID_TYPE_NAME_MAP[type_id]}/{audio_name}"
                    ],
                    text=parsed_metadata["text"],
                    mandarin=parsed_metadata["mandarin"],
                    dialect_id=response.meta["dialect_id"],
                    raw_text=parsed_metadata["raw_text"],
                )
