import scrapy
import io
import PyPDF2
import urllib.request



class PdfSpider(scrapy.Spider):
    name = 'pdf'
    allowed_domains = ['www.capitol.hawaii.gov']
    start_urls = ['http://www.capitol.hawaii.gov/sessions/session2022/testimony/']

    def parse(self, response):
        links = response.xpath("//a[contains(text(),'PDF')]")
        for link in links:
            # Extracting the URL
            partialURL = link.xpath(".//@href").get()
            URL = response.urljoin(partialURL)
            filename = link.xpath(".//text()").get()

            #yield{'filename':filename,
            #'url':URL}

            # calling urllib to create a reader of the pdf url
            req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
            File = urllib.request.urlopen(req)
            reader = PyPDF2.PdfFileReader(io.BytesIO(File.read()))

            # creating data
            data=""
            for datas in reader.pages:
                data += datas.extractText()

            #print(data)

            yield{
                'filename': filename,
                'PDF':data
            }
