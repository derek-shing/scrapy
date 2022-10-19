import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']
    start_urls = ['http://worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_country)



    def parse_country(self,response):
        logging.info(response.url)
