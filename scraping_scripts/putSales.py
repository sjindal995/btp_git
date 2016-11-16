from neo4j.v1 import GraphDatabase, basic_auth
import csv
import time

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "btp"))
session = driver.session()

z = 0
data = [];
it = 0
with open('changes_sales.csv', 'rb') as csvfile:
	csvreader = csv.reader( csvfile );
	start=time.time()
	for row in csvreader:
		# print row
		data.append( row );
		if(z == 1000):
			insert_query = '''
			UNWIND {data} as data
			MATCH( c:Company ) WHERE c.idCompany = data[0]
			SET c.sales = data[1]
			'''
			session.run(insert_query, parameters={"data": data});
			session.close()
			z = 0
			data = []
			it += 1
			end = time.time()
			print str(it) + " : " + str(end-start)
			start=end;
		else:
			z += 1

if(len(data) > 0):
	insert_query = '''
	UNWIND {data} as data
	MATCH( c:Company ) WHERE c.idCompany = data[0]
	SET c.sales = data[1]
	'''
	session.run(insert_query, parameters={"data": data});
	session.close()
	it += 1
	end = time.time()
	print str(it) + " : " + str(end-start)
	start=end;
else:
	pass

# data = []
# start = time.time();
# final_query = '''
# 	MATCH( c:Company ) WHERE not exists(c.sales)
# 	SET c.sales = "NA"
# 	'''
# session.run(final_query, parameters={"data": data});
# session.close()
# end = time.time();
# print end-start