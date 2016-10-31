from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "btp"))
session = driver.session()

#Clear everything before
# delete_everything = '''Match( n:Company ) Delete n;'''
# session.run(delete_everything);

z = 0
data = []
it = 0
#create nodes for companies
with open('directed-subsidiaries-and-investments.csv', 'rb') as csvfile:
	csvreader = csv.reader( csvfile );
	for row in csvreader:
		updated_row = [];
		for item in row:
			if(item == None):
				updated_row.append("NA")
			else:
				updated_row.append(item)
		data.append(updated_row);
		if(z == 1000):
			links_query = '''
			UNWIND {data} as data
			match(i1:Industry{idIndustry: data[0]})
			match(i2:Industry{idIndustry: data[1]})
			create (i1)-[:DIR_SUB_INV_LINKS{num: data[2]}]->(i2)
			'''

			session.run(links_query, parameters={"data": data});
			session.close();
			z = 0
			data = []
			it += 1
			print it
		else:
			z += 1

if (len(data) > 0):
	links_query = '''
	UNWIND {data} as data
	match(i1:Industry{idIndustry: data[0]})
	match(i2:Industry{idIndustry: data[1]})
	create (i1)-[:DIR_SUB_INV_LINKS{num: data[2]}]->(i2)
	'''
	session.run(links_query, parameters={"data": data});
	session.close();
	it += 1
	print it
else:
	pass

#test if there all companies are added
# test_query = '''MATCH (c1:Company{}) return [c1.id, c1.name]'''
# results = session.run( test_query );
# z = 0;
# for row in results:
# 	# print row;
# 	z = z+1;
# print z;