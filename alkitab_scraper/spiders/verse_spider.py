import scrapy


class QuotesSpider(scrapy.Spider):
    name = "verses"

    start_urls = [
        "https://alkitab.mobi/bali/Kej/1/",
        "https://alkitab.mobi/bali/Kej/2/",
    ]

    def parse(self, response):
        language = response.url.split("/")[-4]
        chapter = response.url.split("/")[-3]
        verse_number = response.url.split("/")[-2]

        lines = response.css('body > div')[2].css("p::text").getall()
        for line_number, line_text in enumerate(lines):

            yield {
                "language": language,
                "chapter": chapter,
                "verse_number": verse_number,
                "line_number": line_number,
                "text": line_text
            }
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")