import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            name = product.xpath(".//a[@class='p_box_title']/text()").get()
            url = product.xpath(".//a[@class='p_box_title']/@href").get()
            discounted_price = product.xpath(".//span[@class='productSpecialPrice fl']/text()").get()
            original_price = product.xpath(".//span[@class='normalprice fl']/text()").get()




            yield{
                'name': name,
                'url': url,
                'discounted price': discounted_price,
                'original_price': original_price
            }

            next = response.xpath("//a[@class='nextPage']/@href").get()
            if (next):
                yield scrapy.Request(url = next, callback = self.parse)
