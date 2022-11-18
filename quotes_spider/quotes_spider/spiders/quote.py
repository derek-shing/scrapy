import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            tag = quote.xpath('.//*[@class="tag"]/text()').extract()

            next_url = response.xpath('.//*[@class="next"]/a/@href').extract_first()
            url = response.urljoin(next_url)
            yield scrapy.Request(url)


            
            yield{'Text':text, 'Author':author,'tag':tag}

            print('\n')
            print(text)
            print(author)
            print(tag)
            print('\n')

        pass
