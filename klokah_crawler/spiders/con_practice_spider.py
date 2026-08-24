import scrapy
import xmltodict

from klokah_crawler.items import KlokahCrawlerItem
from klokah_crawler.utils.parse_con_practice import parse_content_metadata


class ConPracticeSpider(scrapy.Spider):
    name = "con_practice"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/extension/con_data/xml/{dialect_id}/conversation.xml",
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        for content_xml in response.xpath("/dataroot/content").getall():
            content_metadata = xmltodict.parse(content_xml)["content"]
            parsed_metadata_list = parse_content_metadata(
                content_metadata, dialect_id=dialect_id
            )

            for parsed_metadata in parsed_metadata_list:
                audio_name = parsed_metadata["audio_name"]
                yield KlokahCrawlerItem(
                    audio_url=[
                        f"https://klokah.tw/extension/con_data/sound/{dialect_id}/sentence/{audio_name}"
                    ],
                    text=parsed_metadata["text"],
                    mandarin=parsed_metadata["mandarin"],
                    dialect_id=response.meta["dialect_id"],
                    raw_text=parsed_metadata["raw_text"],
                )
