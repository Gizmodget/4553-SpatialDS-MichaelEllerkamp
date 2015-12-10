"""
Michael Ellerkamp
Program 5 - Part 1
"""
import csv
import json
import random

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

nodes = []
edges = []
geometry = {}
graph = {}
#obtains all nodes and edges from their respective files
with open('nodes.csv', 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter = ',', quotechar = '|')
    for row in rows:
        nodes.append(row)
with open('edges.csv', 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter = ',', quotechar = '|')
    for row in rows:
        edges.append(row)
#accessing json and creating dictionary of id-geometry
f = open('nodegeometry.json','r')
for line in f:
    line = json.loads(line)
    geometry[line['id']] = json.loads(line['geometry'])

print "Michael Ellerkamp"
print "Program 5 - Part 1"
print "nodes.csv read containing " + str(len(nodes))
print "edges.csv read containing " + str(len(edges))
print "Nodes 203982 contains " + str(len(geometry[str(203982)])) + " points. The geometry follows:"
print geometry[str(203982)]


for e in edges:
    A,B = e
    if A in graph:
        graph[A].append(B)
    else:
        graph[A] = [B]
boo = True
iterated = 0
while(boo):
    start = random.choice(graph.keys())
    end = random.choice(graph.keys())
    print start
    print end
    print find_path(graph,start,end)
    iterated += 1
    if(find_path(graph,start,end) != None):
        boo = False
        print iterated
