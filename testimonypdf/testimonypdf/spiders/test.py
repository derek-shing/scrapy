import scrapy
import io
import PyPDF2
import urllib.request
from scrapy.item import Item
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['codex.cs.yale.edu']
    start_urls = ['https://codex.cs.yale.edu/avi//os-book/OS9/practice-exer-dir/index.html']

    def parse(self, response):
        # getting the list of URL of the pdf
        pdfs = response.xpath('//tr[3]/td[2]/a/@href')

           # Extracting the URL
        URL = response.urljoin(pdfs[0].extract())

           # calling urllib to create a reader of the pdf url
        File = urllib.request.urlopen(URL)
        reader = PyPDF2.PdfFileReader(io.BytesIO(File.read()))

           # accessing some descriptions of the pdf file.
        print("This is the number of pages"+str(reader.numPages))
        print("Is file Encrypted?"+str(reader.isEncrypted))
