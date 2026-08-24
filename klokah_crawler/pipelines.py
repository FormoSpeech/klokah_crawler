# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

from itemadapter import ItemAdapter

from klokah_crawler.dialect_id_map import DIALECT_ID_MAP
from klokah_crawler.items import KlokahCrawlerSaveItem


class PreDownloadPipeline:
    def process_item(self, item):
        adapter = ItemAdapter(item)
        if len(adapter["audio_url"]) > 0 and adapter["audio_url"][0] is None:
            adapter["audio_url"] = []
            return item

        return item


class PostDownloadPipeline:
    def __init__(self, files_store):
        self.files_store = files_store

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings["FILES_STORE"])

    def process_item(self, item):
        storage_folder = self.files_store

        adapter = ItemAdapter(item)
        audio_path = None
        if adapter.get("audio_meta") and len(adapter["audio_meta"]) > 0:
            audio_path = adapter["audio_meta"][0]["path"]

            if not os.path.isabs(storage_folder):
                storage_folder = os.path.join(
                    os.getcwd(), storage_folder.replace("./", "")
                )
            audio_path = os.path.join(storage_folder, audio_path)

        return KlokahCrawlerSaveItem(
            text=adapter["text"],
            mandarin=adapter["mandarin"],
            audio_path=audio_path,
            dialect=DIALECT_ID_MAP[str(adapter["dialect_id"])],
            raw_text=adapter["raw_text"],
        )
