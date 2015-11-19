"""
Michael Ellerkamp
Program 5 - Part 1
"""
import csv
import json
nodes = []
edges = []
geometry = {}
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
