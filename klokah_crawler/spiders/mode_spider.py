import scrapy

from klokah_crawler.items import KlokahCrawlerItem

JSON_MAP = {
    "elementary": ["animal", "plant", "feature"],
    "intermediate": ["animal", "class", "item"],
}


class ModeSpider(scrapy.Spider):
    name = "mode"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            # elementary
            for category in JSON_MAP["elementary"]:
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/mode/json/{dialect_id:02}/elementary/{category}.json",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=self.parse_elementary,
                )

            # intermediate
            for category in JSON_MAP["intermediate"]:
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/mode/json/{dialect_id:02}/intermediate/{category}.json",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=self.parse_intermediate,
                )

            for category in ["A", "B", "C"]:
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/kongmode/JSON/{dialect_id}/{category}/main.json",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=self.parse_main,
                )
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/kongmode/JSON/{dialect_id}/{category}/audio.json",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=self.parse_audio,
                )
            yield scrapy.Request(
                url=f"https://web.klokah.tw/kongmode/JSON/{dialect_id}/instructions.json",
                meta={
                    "dialect_id": dialect_id,
                },
                callback=self.parse_instructions,
            )

    def parse_elementary(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for metadata in response["text"].values():
            audio_path = metadata["sound"]
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{audio_path}.mp3"],
                text=metadata["ab"],
                mandarin=metadata["ch"],
                dialect_id=dialect_id,
            )

    def parse_intermediate(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for metadata in response["data"][1:]:
            for audio_path, text_metadata in zip(metadata["sound"], metadata["text"]):
                yield KlokahCrawlerItem(
                    audio_url=[f"https://web.klokah.tw/{audio_path}.mp3"],
                    text=text_metadata["ab"],
                    mandarin=text_metadata["ch"],
                    dialect_id=dialect_id,
                )

        for metadata in response["text"].values():
            audio_path = metadata["sound"]
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{audio_path}.mp3"],
                text=metadata["ab"],
                mandarin=metadata["ch"],
                dialect_id=dialect_id,
            )

    def parse_main(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for metadata in response:
            ab_audio_path = metadata["abPath"]
            if ab_audio_path is not None:
                ab_audio_path = ab_audio_path.replace("../../", "")

            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{ab_audio_path}"],
                text=metadata["ab"],
                mandarin=metadata["ch"],
                dialect_id=dialect_id,
            )
            key_audio_path = metadata["keyPath"]
            if key_audio_path is not None:
                key_audio_path = key_audio_path.replace("../../", "")

            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{key_audio_path}"],
                text=metadata["keyw"],
                mandarin=metadata["keych"],
                dialect_id=dialect_id,
            )

    def parse_audio(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for metadata in response:
            audio_path = metadata["path"]
            if audio_path is not None:
                audio_path = audio_path.replace("../../", "")

            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{audio_path}"],
                text=metadata["ab"],
                mandarin=metadata["ch"],
                dialect_id=dialect_id,
            )

    def parse_instructions(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()

        for metadata in response:
            audio_path = metadata["path"]
            if audio_path is not None:
                audio_path = audio_path.replace("../../", "")

            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{audio_path}"],
                text=metadata["ab"],
                mandarin=metadata["ch"],
                dialect_id=dialect_id,
            )
