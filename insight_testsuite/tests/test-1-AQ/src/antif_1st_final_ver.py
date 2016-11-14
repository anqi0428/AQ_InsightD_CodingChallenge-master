
'''
File_Name: antif_1st_final_ver.py
Created on 11/13/2016
@author: Qi An
Features: 
This is designed to avoid fraud transactions in real life. 
Import data from csv files and use these data to build a network. 
Functions built are to justify whether there's 1st degree friendship between the users before they transfer money to each other.
'''

# import packages
import numpy as np
import pandas as pd
from collections import defaultdict
import os
os.system("awk -F, \'{if(NF>=5){printf \"%s,%s,%s,%s,\",$1,$2,$3,$4;for(i=5;i<=NF;i++)printf \"%s\",$i}printf \"\\n\"}\' ./paymo_input/batch_payment.txt > ./paymo_input/new_batch_payment.txt")
os.system("awk -F, \'{if(NF>=5){printf \"%s,%s,%s,%s,\",$1,$2,$3,$4;for(i=5;i<=NF;i++)printf \"%s\",$i}printf \"\\n\"}\' ./paymo_input/stream_payment.txt > ./paymo_input/new_stream_payment.txt")
# read file
# oringin data
file_location = './paymo_input/new_batch_payment.txt'
file = open(file_location, 'rU')
df = pd.read_csv(file)
file.close()
df=df.rename(columns = {'time':'time', ' id1':'id1', ' id2':'id2', ' amount':'amount', ' message':'message'})
inputall = len(df)
#testfile
file_location = './paymo_input/new_stream_payment.txt'
file = open(file_location, 'rU')
df_test = pd.read_csv(file)
file.close()
df_test=df_test.rename(columns = {'time':'time', ' id1':'id1', ' id2':'id2', ' amount':'amount', ' message':'message'})
outputall = len(df_test)

# Define class Graph
class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(set)
  def add_node(self, value):
    self.nodes.add(value)
  def add_edge(self, from_node, to_node):
    self.edges[from_node].add(to_node)
    self.edges[to_node].add(from_node)

# Define fuction to find whether they are in a 1st degree friends network
def degree_1(graph, initial, terminal):
  nodes = set(graph.nodes)
  outp = False
  if (initial in nodes) and (terminal in nodes):
    if terminal in graph.edges[initial]:
      outp = True
  return outp

# extract input stream data and build a initial graph
g = Graph()
id1 = list(df.iloc[0:inputall,1])
id2 = list(df.iloc[0:inputall,2])
for i in range(inputall):
  if np.isfinite(id1[i]) != True or np.isfinite(id2[i]) != True:
    continue
  id_1 = int(id1[i])
  id_2 = int(id2[i])
  g.add_node(id_1)
  g.add_node(id_2)
  g.add_edge(id_1,id_2)

# extract output test stream data
id1 = list(df_test.iloc[0:outputall,1])
id2 = list(df_test.iloc[0:outputall,2])
# main text - loop
output_1 = []
for i in range(outputall):
  id_1 = int(id1[i])
  id_2 = int(id2[i])
  if np.isfinite(id_1) != True or np.isfinite(id_2) != True:
    output_1.append('N/A')
    continue
  if degree_1(g, id_1, id_2):
    output_1.append('trusted')
  else: 
    output_1.append('unverified')
    g.add_node(id_1)
    g.add_node(id_2)
    g.add_edge(id_1,id_2)

dff = pd.DataFrame(output_1)
dff.to_csv('./paymo_output/output1.txt',header=False, index=False)
