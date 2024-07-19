import scrapy
from scrapy.selector import Selector


class ParallelSpider(scrapy.Spider):
    name = "parallel"

    start_urls = [
        "https://alkitab.mobi/bali/Kej/1/1/"
    ]

    def parse(self, response):
        # language = response.url.split("/")[-5]
        chapter = response.url.split("/")[-4]
        verse_number = response.url.split("/")[-3]
        line_number = response.url.split("/")[-2]

        lines = response.css('body > div')[2].css("p").getall()
        for line in lines:
            selector = Selector(text=line)
            line_text = selector.xpath(".//text()").getall()[1].strip()
            url = selector.xpath('//strong/a/@href').extract_first()
            lang_code = url.split('/')[-3]


            yield {
                "language": lang_code,
                "chapter": chapter,
                "verse_number": verse_number,
                "line_number": line_number,
                "text": line_text
            }


        next_page = response.xpath('//body/div[2]/span[2]/a[2]/@href').get()
        if next_page != self.start_urls[0]:
            yield scrapy.Request(next_page, callback=self.parse)


        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")