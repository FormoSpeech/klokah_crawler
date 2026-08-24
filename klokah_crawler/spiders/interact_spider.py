import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class InteractSpider(scrapy.Spider):
    name = "interact"

    async def start(self):
        for dialect_id in [i for i in range(1, 44) if i != 12]:
            # primaryInteract_new
            primary_interact_stages = [
                "stage_1",
                "stage_2_1",
                "stage_2_2",
                "stage_3",
                "stage_4",
                "stage_6",
            ]
            for category in range(1, 4):
                for stage in primary_interact_stages:
                    yield scrapy.Request(
                        url=f"https://web.klokah.tw/kongmode/primaryInteract_new/json/{category}/{dialect_id}/{stage}.json",
                        meta={
                            "dialect_id": dialect_id,
                        },
                        callback=self.parse_primary_interact_new,
                    )

            # hordequest
            for category in ["lesson", "find", "outside"]:
                yield scrapy.Request(
                    url=f"https://web.klokah.tw/interact/hordequest/json/{dialect_id:02}/{category}.json",
                    meta={
                        "dialect_id": dialect_id,
                    },
                    callback=self.parse_hordequest,
                )

    def parse_primary_interact_new(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()
        for data in response:
            audio_path = data["soundPath"]
            if audio_path is not None:
                audio_path = audio_path.replace("../../../", "")

            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{audio_path}"],
                text=data["Ab"],
                mandarin=data["Ch"],
                dialect_id=dialect_id,
            )

    def parse_hordequest(self, response):
        dialect_id = response.meta["dialect_id"]
        response = response.json()["data"]

        # phase1
        for metadata in response["phase1"][1:]:
            audio_path = metadata["sound"]
            yield KlokahCrawlerItem(
                audio_url=[f"https://web.klokah.tw/{audio_path}.mp3"],
                text=metadata["text"],
                mandarin=metadata["textCh"],
                dialect_id=dialect_id,
            )

        # phase2
        for list_name, metadata_list in response["phase2"].items():
            if list_name == "player":
                for metadata in metadata_list:
                    audio_path = metadata["sound"]
                    yield KlokahCrawlerItem(
                        audio_url=[f"https://web.klokah.tw/{audio_path}.mp3"],
                        text=metadata["text"],
                        mandarin=metadata["textCh"],
                        dialect_id=dialect_id,
                    )

            if "target" in list_name:
                for metadata in metadata_list.values():
                    audio_path = metadata["sound"]
                    yield KlokahCrawlerItem(
                        audio_url=[f"https://web.klokah.tw/{audio_path}.mp3"],
                        text=metadata["text"],
                        mandarin=metadata["textCh"],
                        dialect_id=dialect_id,
                    )
