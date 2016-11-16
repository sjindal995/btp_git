import time
import json
import os
import time
import sys

with open('json/companies.json') as f:
	data = json.load(f)
# backgroundurl = 'file:///D:/study/btp/btp_git/scraping/json_sample/'
backgroundurl0 = "json_sample/"
out = open('sales.csv','w')
out.write("ID,Sales\n")
it=0
for obj in data:
	st = backgroundurl0+obj['id'] + "/finOver.csv"
	it+=1
	if(os.path.isfile(st)):
		sale = open(st,'r')
		for line in sale:
			print str(it) + " : " + obj['id'] + "," + line+";"
			out.write(obj['id'] + "," + line+"\n")
		# break
it=0
with open('json/companies2.json') as f:
	data2 = json.load(f)
for obj in data2:
	it+=1
	st = backgroundurl0+obj['id'] + "/finOver.csv"
	if(os.path.isfile(st)):
		sale = open(st,'r')
		for line in sale:
			print str(it) + " : " + obj['id'] + "," + line+";"
			out.write(obj['id'] + "," + line+"\n")
		# break