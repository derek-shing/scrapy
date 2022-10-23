import scrapy
from scrapy import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['http://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formid='register',
            formdata={
            'username':'', #your username
            'password':,#your password''
            'redirect':'/',
            'debug_token':'',
            'login':'Log In'
            },
            callback =self.afterlogin
        )


    def afterlogin(self , response):

        print('logged in........')
