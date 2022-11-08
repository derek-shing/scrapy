import scrapy
from scrapy import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['steadyoptions.com']
    start_urls = ['http://steadyoptions.com/login']

    def parse(self, response):
        csrf = response.xpath('//input[@name="csrfKey"]/@value').get()
        print("csrf....................",csrf)
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
            'auth':'', #your username
            'password':'',#your password''
            'remember_me':'1',
            '_processLogin':'usernamepassword',
            '_processLogin':'usernamepassword'
            },
            callback =self.afterlogin
        )

        pass

    def afterlogin(self, response):

        print('logged in........')
        forum = response.xpath("//a[@data-navitem-id='63']/text()").get()
        url = 'https://steadyoptions.com/forums/forum/10-steadyoptions-trades/'
        print(url)
        yield scrapy.Request(url=url, callback=self.scrap_post)
        #print(response.xpath("//body").get())


    def scrap_post(self, response):
        print('scrap post.................')

        print(response.xpath("//h1[@class='ipsType_pageTitle']/text()").get())
        i=0
        list = response.xpath("//ol[@class='ipsDataList ipsDataList_zebra ipsClear cForumTopicTable  cTopicList ']")
        links = list.xpath(".//h4/a/@href")

        """
        for trade in response.xpath("//span[@itemprop='name headline']"):
            trade_name = trade.xpath("normalize-space(.//text())").get()
            i+=1
            #print(i,' : ',trade_name)
            yield{"trade": trade_name}
        """

        for link in links:
            #yield{"link":link.get()}
            yield response.follow(url=link, callback=self.parse_trade)

        next = response.xpath("(//a[@rel='next'])[1]/@href").get()
        #if (next):
            #yield scrapy.Request(url = next, callback = self.scrap_post)

            #response.xpath("//div[@class='col-md-8']/h1/a/text()")
            #test

    def parse_trade(self, response):
        articles = response.xpath("//article")
        for article  in articles:
            content = article.xpath("normalize-space(.//div[@class = 'cPost_contentWrap ipsPad']/descendant-or-self::*/text())").getall()
            final_txt = ''.join( _ for _ in content).strip()
            yield{"trade post": final_txt}
            #scrap all post text
