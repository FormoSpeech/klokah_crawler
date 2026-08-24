import scrapy
import xmltodict

from klokah_crawler.items import KlokahCrawlerItem
from klokah_crawler.utils.parse_rd_practice import parse_vocabulary_metadata


class RdPracticeWordSpider(scrapy.Spider):
    name = "rd_practice_word"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            yield scrapy.Request(
                url=f"https://web.klokah.tw/extension/rd_data/xml/{dialect_id}/reading.xml",
                meta={
                    "dialect_id": dialect_id,
                },
            )

    def parse(self, response):
        dialect_id = response.meta["dialect_id"]
        for vocabulary_xml in response.xpath("/dataroot/vocabulary").getall():
            vocabulary_metadata = xmltodict.parse(vocabulary_xml)["vocabulary"]
            parsed_metadata_list = parse_vocabulary_metadata(
                vocabulary_metadata, dialect_id=dialect_id
            )

            for parsed_metadata in parsed_metadata_list:
                audio_name = parsed_metadata["audio_name"]
                yield KlokahCrawlerItem(
                    audio_url=[
                        f"https://web.klokah.tw/extension/rd_data/audio/{dialect_id}/{audio_name}"
                    ],
                    text=parsed_metadata["text"],
                    mandarin=parsed_metadata["mandarin"],
                    dialect_id=response.meta["dialect_id"],
                    raw_text=parsed_metadata["raw_text"],
                )
