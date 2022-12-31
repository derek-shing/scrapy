import PyPDF2
import urllib.request
import ssl
import io
ssl._create_default_https_context = ssl._create_unverified_context

URL = "https://www.capitol.hawaii.gov/sessions/session2022/testimony/GM501_TESTIMONY_CPN_02-18-22_.PDF"
#URL = "https://codex.cs.yale.edu/avi//os-book/OS9/practice-exer-dir/1-web.pdf"

req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
remoteFile = urllib.request.urlopen(req)

reader = PyPDF2.PdfFileReader(io.BytesIO(remoteFile.read()))

#fileobj = open(remoteFile,'rb')

#reader = PyPDF2.PdfFileReader(fileobj)

# printing number of pages in pdf file
print(reader.numPages)

# creating a page object
pageObj = reader.getPage(0)

# extracting text from page
print(pageObj.extractText())

# closing the pdf file object
remoteFile.close()
