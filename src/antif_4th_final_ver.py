
'''
File_Name: antif_4th_final_ver.py
Created on 11/13/2016
@author: Qi An
Features: 
This is designed to avoid fraud transactions in real life. 
Import data from csv files and use these data to build a network. 
Functions built are to justify whether there's 4th degree friendship between the users before they transfer money to each other.
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

# Define fuction to find whether they are in a 2nd degree friends network
def degree_2(graph, initial, terminal):
  nodes = set(graph.nodes)
  outp = False
  if (initial in nodes) and (terminal in nodes):
    if degree_1(graph, initial, terminal):
      return True
    elif graph.edges[terminal] & graph.edges[initial] !=  set():
      outp = True
  return outp

# func used to save 2nd degree contact for all nodes
def degree_2_cal(graph):
  nodes = graph.nodes
  degree_2 = defaultdict(set)
  for i in nodes:
    for j in graph.edges[i]:
      degree_2[i] = degree_2[i] | graph.edges[j]
  return degree_2

# Define fuction to find whether they are in a 4th degree friends network
def degree_4(graph, savelist, initial, terminal):
  nodes = set(graph.nodes)
  outp = False
  if (initial in nodes) and (terminal in nodes):
    i_edges = graph.edges[initial]
    d2initial = savelist[initial]
    d2terminal = savelist[terminal]
    if terminal in d2initial:
      return True
    elif i_edges & d2terminal != set():
      return True
    else:
      if d2initial & d2terminal != set():
        return True
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


# Generate the initial 2nd degree friend list and save it
degree_2_savelist = degree_2_cal(g)
# extract output test stream data
id1 = list(df_test.iloc[0:outputall,1])
id2 = list(df_test.iloc[0:outputall,2])
# main text - loop
output_4 = []
for i in range(outputall):
  if np.isfinite(id1[i]) != True or np.isfinite(id2[i]) != True:
    output_4.append('N/A')
    continue
  id_1 = int(id1[i])
  id_2 = int(id2[i])
  if degree_4(g, degree_2_savelist, id_1, id_2):
    output_4.append('trusted')
  else: output_4.append('unverified')
  g.add_edge(id_1,id_2)
  if int(id_1 in g.nodes) == 0 and (id_2 in g.nodes):
    g.add_node(id_1)
    degree_2_savelist[id_1] = g.edges[id_2]
    for node in g.edges[id_2]:
      degree_2_savelist[node].add(id_1)
  elif int(id_2 in g.nodes) == 0 and (id_1 in g.nodes):
    g.add_node(id_2)
    degree_2_savelist[id_2] = g.edges[id_1]
    for node in g.edges[id_1]:
      degree_2_savelist[node].add(id_2)
  elif (id_2 in g.nodes) and (id_1 in g.nodes):
    degree_2_savelist[id_1] = degree_2_savelist[id_1] | g.edges[id_2]
    degree_2_savelist[id_2] = degree_2_savelist[id_2] | g.edges[id_1]
    for node in g.edges[id_2]:
      degree_2_savelist[node].add(id_1)
    for node in g.edges[id_1]:
      degree_2_savelist[node].add(id_2)
  elif int(id_2 in g.nodes) == 0 and int(id_1 in g.nodes) == 0:
      g.add_node(id_1)
      g.add_node(id_2)
      degree_2_savelist[id_1].add(id_1)
      degree_2_savelist[id_2].add(id_2)

dff = pd.DataFrame(output_4)
dff.to_csv('./paymo_output/output3.txt',header=False, index=False)
