import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestmoviesSpider(CrawlSpider):
    name = 'bestmovies'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/web/20200715000935/https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]"),follow=True)
    )

    def parse_item(self, response):
        title = response.xpath("//div[@class='title_wrapper']/h1/text()").get()
        year = response.xpath("//span[@id='titleYear']/a/text()").get()
        duration = response.xpath("normalize-space(//div[@class='subtext']/time/text())").get()
        genra = response.xpath("//div[@class='subtext']/a[1]/text()").get()
        rating = response.xpath("//span[@itemprop='ratingValue']/text()").get()
        movie_url = response.url

        yield{
            'title':title,
            'year':year,
            'duration':duration,
            'genra':genra,
            'rating':rating,
            'url': movie_url
        }
        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
