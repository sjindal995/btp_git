it=0
out_f = open("up_ind_map.csv",'w')
with open("ind_map.txt",'r') as in_f:
	for line in in_f:
		if(line[-1]=='\n'):
			line = line[:-1]
		line_list = line.split(': ')
		if(len(line_list)>1):
			it+=1
			sector = line_list[0]
			ind_list = line_list[1].split(', ')
			# out_f.write(str(len(ind_list))+"\n")
			for ind in ind_list:
				out_f.write(str(it)+","+sector+","+ind+"\n")