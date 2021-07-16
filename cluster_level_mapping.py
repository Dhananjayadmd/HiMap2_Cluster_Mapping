#!/usr/bin/env python
import sys
import os
import os.path
import shutil
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re
#from antlr4 import tree

import numpy as np
import networkx as nx

from sklearn.cluster import SpectralClustering
from sklearn import metrics
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import to_pydot
from sklearn.cluster._agglomerative import AgglomerativeClustering
import pydot
from _ast import If
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

import gurobipy as gp
from gurobipy import GRB
from networkx.classes.function import neighbors

try:
    clus_dfg = nx.read_gexf('inter_cluster.gexf')
    
    num_of_columns = 3
    num_of_rows = 3
    row  = 0
    number_of_cgra_clusters = num_of_columns*num_of_rows
    #clus_dfg = nx.read_gexf('inter_cluster_nettle.gexf')
    num_nodes =  clus_dfg.number_of_nodes()
    print(clus_dfg.number_of_nodes())
    print(clus_dfg.number_of_edges())
    
    
    for i in range(0,num_nodes):
        clus_dfg.nodes[i]["row"] = -1

    colordict = {
        0:'red',
        1:'green',
        2:'blue',
        3:'yellow',
        4:'cyan',
        5:'purple',
        6:'orange',
        7:'brown',
        8:'magenta',
        9:'rose',
        10:'azure'
        
    }

    while (row < num_of_rows):
        C1 = 1;
        n = 100000;
        C2 = 1;
    
        # Create a new model
        m = gp.Model("mip1")
        
        v =[]
        for i in range(0,num_nodes):
            if clus_dfg.nodes[i]["row"] == -1 :
                v.append(m.addVar(vtype=GRB.BINARY, name="v%d" % (i)))
        m.update()
        
        #Vik1 = m.addVars(num_nodes,vtype=GRB.BINARY, name="Vik1")
        #number_of_cgra_clusters = 2;
        Epsilon = num_nodes/num_of_rows;
        
        #expr1= gp.LinExpr()
        expr1 = gp.quicksum(v) - Epsilon
        #expr1=gp.abs_(Vik1[0]+Vik1[1] - Epsilon)
        print(expr1)
        #for i in range(0,num_nodes):
            #expr1.add(Vik1[i])
        
        #gurobi doesn't support abs in objective. How to convert abs to supported format? Follow the link
        #http://lpsolve.sourceforge.net/5.1/absolute.htm
        #https://support.gurobi.com/hc/en-us/community/posts/360074428532-How-to-handle-absolute-value-in-objective-function-
        x_ = m.addVar(name = 'x_')
        
        m.setObjective(x_ , GRB.MINIMIZE)
        m.addConstr(expr1 <= x_)
        m.addConstr(-expr1 <= x_)
        #m.setObjective(gp.abs_(sum(Vik1[i] for i in range(0,num_nodes)) - Epsilon) , GRB.MINIMIZE)
        
        found_solution = False
        print("initial constr")
        print(m.getConstrs())
        num_of_constr = 2;
        
        while (found_solution!= True):
            num_of_constr = 2;
            for nodes in clus_dfg.nodes:
                #print(nodes)
                node_id = int(nodes)
                print("Node ID:",node_id)
                index_list = []
                index_list.append(nodes)
                degree = 0
                for neighbors in clus_dfg.neighbors(nodes):
                #print(neighbors)
                    index_list.append(neighbors)
                    degree = degree + 1
                    #print(index_list)
                for i in range(0,len(index_list)):
                    index_list[i] = int(index_list[i])
                
                print(v[0])
                print("Constraint 1:", sum(v[i] for i in index_list) <= C1 + n*v[node_id])
                m.addConstr(sum(v[i] for i in index_list) <= C1 + n*v[node_id])
                print("Constraint 2:", sum(v[i] for i in index_list) >= 2*degree - C2 - n*(1-v[node_id]))
                m.addConstr(sum(v[i] for i in index_list) >= 2*degree - C2 - n*(1-v[node_id]))
                num_of_constr = num_of_constr+2
                print("")
            
            m.optimize()
        
            #print(clus_dfg.neighbors(nodes))
            
            print("V0",v[0])
            for var in m.getVars():
                #print('%s %g' % (var.varName, var.x))
                if var.x == 1 :
                    found_solution = True
                    
            if found_solution == True:
                print("Found a solution at C1,C2  : ", C1,C2)
                for var in m.getVars():
                    print('%s %g' % (var.varName, var.x))
                    if str(var.varName[0]) =='v':
                        print(int(var.varName[1:]))
                        clus_dfg.nodes[int(var.varName[1:])]["row"] = row
                row = row + 1
            print('Obj: %g' % m.objVal)
            print("Constraint List:",m.getConstrs())
            print("Number of Constraints:",num_of_constr)
            m.remove(m.getConstrs()[2:(num_of_constr)])
            m.update()
            #print(m.getConstrs())
            C1 = C1+1
            C2 = C2+1
    
    for i in range(0,num_nodes):
        print("node,row",i,clus_dfg.nodes[i]["row"])
    # Create a new model
    #m = gp.Model("mip1")

    # Create variables
    #x = m.addVar(vtype=GRB.BINARY, name="x")
    #y = m.addVar(vtype=GRB.BINARY, name="y")
    #z = m.addVar(vtype=GRB.BINARY, name="z")

    # Set objective
    #m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    #m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

    # Add constraint: x + y >= 1
    #m.addConstr(x + y >= 1, "c1")

    # Optimize model
    #m.optimize()

    #for v in m.getVars():
    #    print('%s %g' % (v.varName, v.x))

    #print('Obj: %g' % m.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')