#############################
#		WITH URLLIB			#
#############################
import os
import requests
import tempfile
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger

def getcookies():
	
	url = 'https://my.zanichelli.it/kitaboo/XXXXXXXXXXXXXXXXXXXXXXXX'
	r = requests.get(url, allow_redirects=True)
	print (r.cookies)

def download():

	#open the book with webreader and press CTRL + SHIFT + I
	#Network -> page*.svgz copy the link and replace it in 'url_pt1' removing ****.svgz
	url_pt1 = 'https://webreader.zanichelli.it/ContentServer/mvc/s3view/XXXXX/html5/XXXXX/OPS/images/page'
	url_pt2 = '.svgz'
	#Application -> Cookies copy and replace them in 'cookies' = { CloudFront-Key-Pair-Id, CloudFront-Policy, CloudFront-Signature }
	cookies = {
		'CloudFront-Key-Pair-Id': 'XXXXXXXXXXXXXXXXXX',
		'CloudFront-Policy': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
		'CloudFront-Signature': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
	}
	#'first_page' replace X with the first page (you can skip index pages)
	#'final_page' replace X with the final page and check the link ...OPS/images/page0XXX.svgz
	first_page = X
	final_page = X		

	dir = tempfile.mkdtemp()
	pdfs = ["" for x in range(final_page)]

	for cont in range(first_page, final_page):
		r = requests.get(url_pt1 + str("%04d" % cont) + url_pt2, 'wb', cookies=cookies)
		
		with open(os.path.join(dir, "page" + str("%04d" % cont) + ".svg"), 'wb') as output:
			output.write(r.content)
		output.close()
		drawing = svg2rlg(os.path.join(dir, "page" + str("%04d" % cont) + ".svg"))
		renderPDF.drawToFile(drawing, os.path.join(dir, "page" + str("%04d" % cont) + ".pdf"))

	for cont in range(final_page-first_page):
		print("page " + str(first_page))
		pdfs[cont] = os.path.join(dir, "page" + str("%04d" % first_page) + ".pdf")
		print (pdfs[cont])
		first_page = first_page+1

	merger = PdfFileMerger()
	print("merging pdfs...")

	while '' in pdfs:
		pdfs.remove('')

	for pdf in pdfs:
		merger.append(open(pdf, 'rb'))

	with open("book.pdf", 'wb') as fout:
		merger.write(fout)

	print("finished") 


def deletePngs():
	test = os.listdir(tempfile.gettempdir())
	for item in test:
		if item.endswith(".png"):
			os.remove(os.path.join(tempfile.gettempdir(), item))

#call
#getcookies()

download()

deletePngs()







'''
#############################
#		WITH SELENIUM		#
#############################

import os
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger
from tempfile import TemporaryDirectory

#download https://sites.google.com/a/chromium.org/chromedriver/downloads
#and put chromedriver in the same folder

driver_options = webdriver.ChromeOptions()
driver_options.add_argument("--incognito")
driver_options.add_argument("--start-maximized")
driver = webdriver.Chrome("chromedriver", options=driver_options)

#book link (copy link -> https://my.zanichelli.it/scrivania -> button[Apri il web reader di Zanichelli])
driver.get("https://my.zanichelli.it/kitaboo/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
delay = 5
try:
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'container')))
except TimeoutException:
    print ("Error loading")

url_pt1 = 'https://webreader.zanichelli.it/ContentServer/mvc/s3view/XXXXX/html5/XXXXX/OPS/images/page'
url_pt2 = '.svgz'


dir = tempfile.mkdtemp()
first_page = X
final_page = X

pdfs = ["" for x in range(final_page)]

for cont in range(first_page, final_page):
	driver.get(url_pt1 + str("%04d" % cont) + url_pt2)
	page_src = driver.page_source.encode("utf-8")
	f = open(os.path.join(dir, "page" + str("%04d" % cont) + ".svg"), 'wb')
	f.write(page_src)
	drawing = svg2rlg(os.path.join(dir, "page" + str("%04d" % cont) + ".svg"))
	renderPDF.drawToFile(drawing, os.path.join(dir, "page" + str("%04d" % cont) + ".pdf"))

for cont in range(final_page-first_page):
	pdfs[cont] = os.path.join(dir, "page" + str("%04d" % first_page) + ".pdf")
	print (pdfs[cont])
	first_page = first_page+1

driver.quit()

merger = PdfFileMerger()
print("merging pdfs...")

while '' in pdfs:
	pdfs.remove('')

for pdf in pdfs:
	merger.append(open(pdf, 'rb'))

with open("book.pdf", 'wb') as fout:
	merger.write(fout)
f.close()

print("finished")
'''