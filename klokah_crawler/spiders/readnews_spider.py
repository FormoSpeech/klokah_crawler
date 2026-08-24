import scrapy

from klokah_crawler.items import KlokahCrawlerItem


class ReadNewsSpider(scrapy.Spider):
    name = "readnews"

    async def start(self):
        yield scrapy.Request(
            url="https://web.klokah.tw/readnews/php/getNews.php?d=0&t=&p=1",
            callback=self.get_page_of_news,
            meta={
                "page": 1,
            },
        )

    def get_page_of_news(self, response):
        response_json = response.json()
        if response_json["last"] == "n":
            next_page = response.meta["page"] + 1
            yield scrapy.Request(
                url=f"https://web.klokah.tw/readnews/php/getNews.php?d=0&t=&p={next_page}",
                callback=self.get_page_of_news,
                meta={"page": next_page},
            )

        for news in response_json["data"]:
            news_id = news["id"]
            dialect_id = news["did"]
            yield scrapy.Request(
                url=f"https://web.klokah.tw/readnews/read.php?tid={news_id}",
                meta={"dialect_id": dialect_id},
            )

    def parse(self, response):
        title = response.css("#rn-read-title-name")
        title_text = title.css(".Ab::text").get()
        title_translated = title.css(".Ch::text").get()
        yield KlokahCrawlerItem(
            audio_url=[],
            text=title_text,
            mandarin=title_translated,
            dialect_id=response.meta["dialect_id"],
        )

        for sentence in response.css("#rn-read-left > div"):
            sentence_text = " ".join(sentence.css("div.word::text").getall())
            translated_text = sentence.css("div.rn-read-sentence.Ch::text").get()

            yield KlokahCrawlerItem(
                audio_url=[],
                text=sentence_text,
                mandarin=translated_text,
                dialect_id=response.meta["dialect_id"],
            )
