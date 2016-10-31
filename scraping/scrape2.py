from selenium import webdriver
import time
import json
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

start = time.time()
binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)
driver.get('http://capitaline.com/SiteFrame.aspx?id=1')
time.sleep(1)
backgroundurl = 'https://www.capitaline.com/Company/BackGround.aspx?CoCode='
driver.get('https://www.capitaline.com/Company/BackGround.aspx?CoCode=1')
with open('json/companies.json') as f:
	data = json.load(f)
html_f = True
csv_f = True
for obj in data[8500:10000]:
	print obj
	driver.get(backgroundurl+obj['id'])
	time.sleep(1)
	driver.get('https://www.capitaline.com/Company/FinOverview.aspx?id=fin')
	time.sleep(1)
	# driver.find_element_by_xpath("//select[@name='Yearng']/option[text()='Range']").click()
	# l = [e.get_attribute("value") for e in driver.find_elements_by_xpath('//select[@name="Cmbfrm"]/option[text()]')]
	# l.sort()
	# int_l = [int(i) for i in l]
	# if int_l:
	# 	driver.find_element_by_xpath("//select[@name='Cmbfrm']/option[text()="+str(min(int_l))+"]").click()
	# 	driver.find_element_by_xpath("//select[@name='Cmbto']/option[text()="+str(max(int_l))+"]").click()
	# driver.find_element_by_xpath("//input[@name='Btngo']").click()
	if html_f:
		try:
			with open('html/'+obj['id']+'/finOver.html','w') as f:
				f.write(driver.page_source.encode('utf-8'))
		except:
			os.makedirs('html/'+obj['id'])
			with open('html/'+obj['id']+'/finOver.html','w') as f:
				f.write(driver.page_source.encode('utf-8'))
	if csv_f:
		csv_data = ""
		for i,sel in enumerate(driver.find_elements_by_xpath('//table[@class="tablelines"]')):
			# year = sel.find_element_by_xpath('.//td[@class="tdCenterHeader"]').text
			heads = [i.text for i in sel.find_elements_by_xpath('.//td[@class="SubSbHdrLeft"]')+sel.find_elements_by_xpath('.//td[@class="SubSbHdr"]')]
			# print heads
			heads = heads[2:]
			cols = [i.text for i in sel.find_elements_by_xpath('.//td[@class="ColmElementWht"]')]
			# print len(heads)
			if(len(heads) > 0):
				for j in range(len(cols)/len(heads)):
					# tup = [year]
					if(j == 1):
						csv_data = str(cols[2*len(heads)-1])
						break
			else:
				print "len heads 0!!"
			if csv_data!="":
				try:
					with open('json/'+obj['id']+'/finOver.csv','w') as f:
						f.write(csv_data)
				except:
					os.makedirs('json/'+obj['id'])
					with open('json/'+obj['id']+'/finOver.csv','w') as f:
						f.write(csv_data)
end = time.time()
print "time taken: " + str(end-start)