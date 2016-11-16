from selenium import webdriver
import time
import json
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import sys

tfile = open('tsales.txt','w')

start = time.time()
binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)
# driver.get('http://capitaline.com/SiteFrame.aspx?id=1')
# time.sleep(1)
backgroundurl = 'file:///D:/study/btp/btp_git/scraping/html/'
# driver.get('https://www.capitaline.com/Company/BackGround.aspx?CoCode=1')
with open('json/companies2.json') as f:
	data = json.load(f)
html_f = True
csv_f = True
cnt = 48000
for obj in data[48000:51500]:
	print obj
	driver.get(backgroundurl+obj['id'] + "/finOver.html")
	# time.sleep(1)
	# driver.get('https://www.capitaline.com/Company/FinOverview.aspx?id=fin')
	# time.sleep(1)
	if csv_f:
		csv_data = ""
		for i,sel in enumerate(driver.find_elements_by_xpath('//table[@class="tablelines"]')):
			# year = sel.find_element_by_xpath('.//td[@class="tdCenterHeader"]').text
			heads = [i.text for i in sel.find_elements_by_xpath('.//td[@class="SubSbHdrLeft"]')+sel.find_elements_by_xpath('.//td[@class="SubSbHdr"]')]
			# print heads
			heads = heads[2:]
			col_hds = [i.text for i in sel.find_elements_by_xpath('.//td[@class="ColmElement"]')]
			cols = [i.text for i in sel.find_elements_by_xpath('.//td[@class="ColmElementWht"]')]

			pos = -1
			if("Sales" in col_hds):
				pos = col_hds.index("Sales")
			if(pos==-1 and ("Gross Sales" in col_hds)):
				pos=col_hds.index("Gross Sales")
			# print len(heads)
			# print pos
			# print len(cols)
			# print str(cols[(pos+1)*len(heads)-1])
			if(len(heads) > 0 and pos >= 0):
				if(len(cols) >= (pos+1)*len(heads)):
					csv_data = str(cols[(pos+1)*len(heads)-1])
				# break
			else:
				print "len heads 0!!"
			# print csv_data
			if csv_data!="":
				try:
					with open('json_sample/'+obj['id']+'/finOver.csv','w') as f:
						f.write(csv_data)
				except:
					os.makedirs('json_sample/'+obj['id'])
					with open('json_sample/'+obj['id']+'/finOver.csv','w') as f:
						f.write(csv_data)
	tfile.write(str(cnt)+'\n')
	cnt=cnt+1
end = time.time()
print "time taken: " + str(end-start)