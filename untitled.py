#considering only companies that have subsidiary/holding company   or invester/investee company
import MySQLdb
import pickle
import os
import numpy as np
import math as mt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv

figNo = 1;
index_to_industry_map = {};

def getGraph( add_investments_too, isDirected ):
	db = MySQLdb.connect("localhost","root","<PASSWORD>","btp");
	global index_to_industry_map;
	cursor = db.cursor();

	get_all_companies_query = "SELECT * FROM Company";
	cursor.execute( get_all_companies_query );
	results = cursor.fetchall();

	index_to_companies_map = {};
	index_to_industry_map = {};
	edges_weight_between_industries = {};
	for row in results:
		index_to_companies_map[ row[0] ] = [row[1],row[2]];

	cursor.execute( "SELECT * FROM Industry");
	results = cursor.fetchall();
	for row in results:
		index_to_industry_map[ row[0] ] = row[1];

	sql_query = "SELECT * FROM Subsidiaries";
	cursor.execute( sql_query );
	results = cursor.fetchall();
	for row in results:
		if index_to_companies_map.has_key( row[0] ) and index_to_companies_map.has_key( row[1] ):
			cmp1 = index_to_companies_map[ row[0] ][1];
			cmp2 = index_to_companies_map[ row[1] ][1];
			if not edges_weight_between_industries.has_key( cmp1 ):
				edges_weight_between_industries[ cmp1 ]  = {};
			if not edges_weight_between_industries[ cmp1 ].has_key( cmp2 ):
				edges_weight_between_industries[ cmp1 ][ cmp2 ] = 1;
			else:
				edges_weight_between_industries[ cmp1 ][ cmp2 ] = \
					edges_weight_between_industries[ cmp1 ][ cmp2 ] + 1;
	fname = '_subsidiaries'
	if add_investments_too:
		fname = '_subsidiaries_and_investments';
		cursor.execute( "SELECT * FROM Investments");
		results = cursor.fetchall();
		for row in results:
			if index_to_companies_map.has_key( row[0] ) and index_to_companies_map.has_key( row[1] ):
				cmp1 = index_to_companies_map[ row[0] ][1];
				cmp2 = index_to_companies_map[ row[1] ][1];
				if not edges_weight_between_industries.has_key( cmp1 ):
					edges_weight_between_industries[ cmp1 ]  = {};
				if not edges_weight_between_industries[ cmp1 ].has_key( cmp2 ):
					edges_weight_between_industries[ cmp1 ][ cmp2 ] = 1;
				else:
					edges_weight_between_industries[ cmp1 ][ cmp2 ] = \
						edges_weight_between_industries[ cmp1 ][ cmp2 ] + 1;
	
	Graph = None;
	DrawGraph = False;
	DoDirectedGraph = isDirected;
	if DoDirectedGraph:
		Graph = nx.DiGraph();
		maxWeightIs = -1;
		for ind1 in edges_weight_between_industries.keys():
			for ind2 in edges_weight_between_industries[ind1].keys():
				maxWeightIs = max( maxWeightIs, edges_weight_between_industries[ind1][ind2] );
		for ind1 in edges_weight_between_industries.keys():
			for ind2 in edges_weight_between_industries[ind1].keys():
				edges_weight_between_industries[ind1][ind2] = \
					(edges_weight_between_industries[ind1][ind2]*1.0)/maxWeightIs;
				Graph.add_edge( ind1, ind2 , weight=edges_weight_between_industries[ind1][ind2] );
		if DrawGraph:
			f1 = plt.figure(1);
			nx.draw( Graph, edge_color='b', node_color='r', node_size=30, width=0.2, node_shape='.');
			plt.draw();
			pickle.dump( f1, open("./Results/Industry_Analysis/Figures/directed_industries"+fname+".fig","wb"));
	DoUnDirectedGraph = not isDirected;	
	if DoUnDirectedGraph:
		Graph = nx.Graph();
		maxWeightIs = -1;
		
		edges_weight_between_industriesNew = {};
		for ind1 in edges_weight_between_industries.keys():
			if not edges_weight_between_industriesNew.has_key( ind1 ):
				edges_weight_between_industriesNew[ind1] = {};
			for ind2 in edges_weight_between_industries[ind1].keys():
				if not edges_weight_between_industriesNew.has_key( ind2 ):
					edges_weight_between_industriesNew[ind2] = {};

				if not edges_weight_between_industriesNew[ind1].has_key(ind2):
					edges_weight_between_industriesNew[ind1][ind2] = edges_weight_between_industries[ind1][ind2];
					edges_weight_between_industriesNew[ind2][ind1] = edges_weight_between_industries[ind1][ind2];
				else:
					edges_weight_between_industriesNew[ind1][ind2] = edges_weight_between_industriesNew[ind1][ind2] + \
																	 edges_weight_between_industries[ind1][ind2];
					edges_weight_between_industriesNew[ind2][ind1] = edges_weight_between_industriesNew[ind2][ind1] + \
																	 edges_weight_between_industries[ind1][ind2]; 

				maxWeightIs = max( maxWeightIs, edges_weight_between_industriesNew[ind1][ind2] );
		
		for ind1 in edges_weight_between_industriesNew.keys():
			for ind2 in edges_weight_between_industriesNew[ind1].keys():
				edges_weight_between_industriesNew[ind1][ind2] = \
					(edges_weight_between_industriesNew[ind1][ind2]*1.0)/maxWeightIs;
				Graph.add_edge( ind1, ind2 , weight=edges_weight_between_industriesNew[ind1][ind2] );

	#Get the Graph here, might be directed or undirected
	#Please draw the graphs, total 4 graphs:   (undirected/directed) and (with/without investments)

def analyzeOnGraph():
	for add_investments in [True, False]:
		for isDirected in [True, False]:
			getGraph( add_investments, isDirected );

analyzeOnGraph(); 
