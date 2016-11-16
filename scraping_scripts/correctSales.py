import json
import os
import time
import sys

inp = open('sales.csv','r')
out_full = open('cor_sales.csv','w')
out_part = open('changes_sales.csv','w')


for line in inp:
	line = line[:-1]
	lt = line.split(',')
	if(len(lt)>2):
		c_id = lt[0]
		sale = lt[1]+lt[2]
		out_part.write(c_id + "," + sale+"\n")
		out_full.write(c_id + "," + sale+"\n")
	else:
		out_full.write(line+"\n")
