from neo4j.v1 import GraphDatabase, basic_auth
import csv
import time

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "btp"))
session = driver.session()

data = [];
with open('up_ind_map.csv', 'rb') as csvfile:
	csvreader = csv.reader( csvfile );
	for row in csvreader:
		data.append(row)
	insert_query = '''
	UNWIND {data} as data
	MERGE (s:Sector{name:data[1], idSector:data[0]})
	MERGE (i:Industry{name:data[2]})
	CREATE (i)-[:SECTOR{}]->(s)
	'''
	session.run(insert_query, parameters={"data": data});
	session.close()