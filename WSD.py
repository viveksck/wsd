import numpy as np
import scipy
import networkx as nx
import sys
import os

RELEXT_FILE_NAME = sys.argv[1]
DICTIONARY_FILE_NAME = sys.argv[2]
CONTEXT_FILE_NAME = sys.argv[3]
PPV = dict()

def PopulateGraph():
    return nx.read_adjlist('Graph_1.txt')

def LookupConcepts(D, key):
    concepts = D[key]
    return concepts

def ReadDictionary(G):
    fh = open(DICTIONARY_FILE_NAME, "r")
    lines = fh.readlines()
    D = dict()
    for line in lines:
        line = line.rstrip()
        tokens = line.split(' ')
        key = tokens[0]
        concepts = tokens[1:]
        nc = []
        for c in concepts:
            nt = c.rsplit(':',1)
            nc.append(nt[0])
        D[key] = nc
    return D

def create_ppv(G):
    global PPV
    keys = G.nodes()
    values = G.number_of_nodes() * [0]
    pairs = zip(keys, values)
    PPV = dict(pairs)

def set_ppv_vector(key, value):
    PPV[key] = value

def set_ppv_vector_key(D, key, weight):
    concepts = LookupConcepts(D, key)
    wt = weight/len(concepts)
    for concept in concepts:
        set_ppv_vector(concept, wt)


def set_ppv_vector_context(D, context):
    global PPV
    PPV = dict.fromkeys(PPV, 0)
    count = 0
    for key in context:
        if key in D:
           count = count + 1
 
    weight = 1.0/count
    for key in context:
           if key in D:
              set_ppv_vector_key(D, key, weight)

def main():
    global PPV
    G = PopulateGraph()
    D = ReadDictionary(G)
    create_ppv(G)

    fh = open(CONTEXT_FILE_NAME, "r")
    lines = fh.readlines()
    for line in lines:
        line = line.rstrip()
        context = line.split(' ')
        print "Context is", context
        set_ppv_vector_context(D, context)
        O = nx.pagerank(G, alpha=0.85, personalization=PPV) 
        for key in context:
            if key in D:
               for concept in LookupConcepts(D, key):
                   print key, concept, O[concept]
   
if __name__ == "__main__":
   main()
