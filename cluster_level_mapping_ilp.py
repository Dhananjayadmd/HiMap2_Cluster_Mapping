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
from _ast import If, Assign

import pygraphviz as gz
#from pygraphviz import Digraph
import graphviz
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
    num_of_columns = 3#4#5#4
    num_of_rows = 3#4#2#4
    row  = 0
    number_of_cgra_clusters = num_of_columns*num_of_rows
    num_of_dfg_nodes = 0
    
    
    #clus_dfg = nx.read_gexf('inter_cluster_nettle.gexf')
    num_cluster_nodes =  clus_dfg.number_of_nodes()
    print("Number of cluster nodes:",clus_dfg.number_of_nodes())
    print("Number of cluster edges:",clus_dfg.number_of_edges())
    
    #for nodes in clus_dfg.nodes:#range(0,num_cluster_nodes):
    #print(clus_dfg.edges)
    #for edges in clus_dfg.edges:
    #    print(clus_dfg[edges[0]][edges[1]]["label"])
    cluster_node_to_dfg_nodes = []
    i = 0
    min_dfg_nodes = 1000000
    for nodes in clus_dfg.nodes:
        #print(clus_dfg.nodes[nodes]["label"])
        num_of_dfg_nodes = num_of_dfg_nodes + int(clus_dfg.nodes[nodes]["label"])
        cluster_node_to_dfg_nodes.insert(i,int(clus_dfg.nodes[nodes]["label"]))
        if min_dfg_nodes > int(clus_dfg.nodes[nodes]["label"]):
            min_dfg_nodes = int(clus_dfg.nodes[nodes]["label"])
        i = i+1
        
        #num_of_dfg_nodes = num_of_dfg_nodes + int(clus_dfg.nodes[i]['label'])
        
    num_of_dfg_nodes_per_cgra_cluster = int(num_of_dfg_nodes/number_of_cgra_clusters)
    print("Number of dfg nodes:",num_of_dfg_nodes)
    print("Number of cgra clusters:",number_of_cgra_clusters)
    print("Number of dfg nodes per cgra cluster:",num_of_dfg_nodes_per_cgra_cluster)
    
    #modify the clus dfg
    if False:
        i=0
        new_nodes = []
        new_node_color = []
        new_edge_source = []
        new_edge_dest = []
        new_edge_degree = []
        new_node_id = 0
        for nodes in clus_dfg.nodes:
            num_new_nodes = int(cluster_node_to_dfg_nodes[i]/min_dfg_nodes)
            print("Node ID, new nodes to be added:", i,num_new_nodes)
            for j in range(0,num_new_nodes):
                #clus_dfg.add_node(new_node_id, label = 0, color=colordict[i])
                new_node_color.append(colordict[i])
                new_nodes.append(num_cluster_nodes+new_node_id)
            
                new_edge_source.append(num_cluster_nodes+new_node_id)
                new_edge_dest.append(nodes)
                new_edge_degree.append(1)
                for neighbors in clus_dfg.neighbors(nodes):
                    neighbor_id = int(neighbors)
                    degree = clus_dfg[nodes][neighbors]['label']
                #new_edge_source.append(num_cluster_nodes+new_node_id)
                #new_edge_dest.append(neighbors)
                #new_edge_degree.append(degree)
                new_node_id = new_node_id+1
                #clus_dfg.add_edge(new_node_id,neighbor_id,label =  degree)
        #if i == num_cluster_nodes-1:
        #    break
            i=i+1
        
        for i in range(0,len(new_nodes)):
            clus_dfg.add_node(new_nodes[i], label = 0, color=new_node_color[i])
            colordict[new_nodes[i]]=new_node_color[i]
        #    print(new_nodes[i],new_node_color[i])
    
    #print("cluster nodes:",clus_dfg.number_of_nodes())
        for i in range(0,len(new_edge_source)):
            clus_dfg.add_edge(new_edge_source[i],new_edge_dest[i],label =  new_edge_degree[i])
        #print(new_edge_source[i],new_edge_dest[i],new_edge_degree[i])
    #exit()
   # print("cluster nodes:",clus_dfg.number_of_nodes())
    #for nodes in clus_dfg.nodes:
    #    print(nodes)
        num_cluster_nodes = clus_dfg.number_of_nodes()
        num_of_new_cluster_nodes_per_cgra_cluster = int(num_cluster_nodes/number_of_cgra_clusters)
        print("number of cluster nodes in updated clus dfg:",num_cluster_nodes)
        print("num_of_new_cluster_nodes_per_cgra_cluster:",num_of_new_cluster_nodes_per_cgra_cluster)  
    #exit()     
    
    m = gp.Model("mip1")
    
    v =[]
    j=0
    for i in range(0,num_cluster_nodes):
        for c in range(0,num_of_columns):
            for r in range(0,num_of_rows):
                v.insert(j,m.addVar(vtype=GRB.BINARY, name="v%d%d%d" % (i,r,c)))
                j=j+1
    m.update()
    
    objective = gp.LinExpr()
    for edges in clus_dfg.edges:
        weight = int(clus_dfg[edges[0]][edges[1]]["label"])
        for c in range(0,num_of_columns):
            for r in range(0,num_of_rows):
            #print(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
                objective = objective + weight*(r+c)*(m.getVarByName(str("v"+str(edges[0])+str(r)+str(c))) - m.getVarByName(str("v"+str(edges[1])+str(r)+str(c))))
    
    print(objective)
    #m.setObjective(objective , GRB.MINIMIZE)
    x_ = m.addVar(name = 'x_')
        
    m.setObjective(x_ , GRB.MINIMIZE)
    m.addConstr(objective <= x_)
    m.addConstr(-objective <= x_)
    
    
    for i in range(0,num_cluster_nodes):
        constr1 = gp.LinExpr()
        for c in range(0,num_of_columns):
            for r in range(0,num_of_rows):
            #print(m.getVarByName(str("v"+str(i)+str(c))))
                constr1 = constr1 + m.getVarByName(str("v"+str(i)+str(r)+str(c))) 
        m.addConstr(constr1 <= 1)#int(cluster_node_to_dfg_nodes[i]/num_of_dfg_nodes_per_cgra_cluster)+1)
        #print("Constraint:", constr1 <= int(cluster_node_to_dfg_nodes[i]/num_of_dfg_nodes_per_cgra_cluster)+1)
        m.addConstr(constr1 >= 1)
        print("Constraint:", constr1 >= 1)
        
    for c in range(0,num_of_columns):
        for r in range(0,num_of_rows):
            constr2 = gp.LinExpr()
            for i in range(0,num_cluster_nodes):
                constr2 = constr2 + m.getVarByName(str("v"+str(i)+str(r)+str(c)))   #cluster_node_to_dfg_nodes[i]* m.getVarByName(str("v"+str(i)+str(r)+str(c)))    
            #print(sum(m.getVarByName(str("v"+str(k)+str(c))) for k in index_list) <= 1)
            m.addConstr( constr2 <= 2)#  num_of_new_cluster_nodes_per_cgra_cluster+1)# num_of_dfg_nodes_per_cgra_cluster+10)
    
    m.optimize()
    g = graphviz.Digraph('G', engine="neato", filename='cluster_map.gv', format='png')
    
    print('Obj: %g' % m.objVal)
    for i in range(0,num_cluster_nodes):
        print("node:",i)
        for c in range(0,num_of_columns):
            for r in range(0,num_of_rows):
            #print(m.getVarByName(str("v"+str(i)+str(c))), m.getVarByName(str("v"+str(i)+str(c))).x)
                if m.getVarByName(str("v"+str(i)+str(r)+str(c))).x == 1:  
                    posit = str(""+str(c)+","+str(r)+"!")
                    print(posit)
                    g.node(str(i),pos=posit,color=colordict[i])
                    print("position:",posit)
    
    #for i in range(0,num_cluster_nodes):
    #    print("node: (row,col)",i,assigned_row[i],assigned_col[i])
        
    
    for edges in clus_dfg.edges:
        g.edge(str(edges[0]),str(edges[1]))
    #pos1 = str('')
    #g.node('1', pos='1,2!')
    #g.node('2', pos='2,3!')
    #g.node('3',pos='0,0!')
    #g.edge('1','2')
    #g.edge('1','3')
    g.render()
    
    exit()
    
    
    assigned_row = []
    for i in range(0,num_cluster_nodes):
        assigned_row.insert(i, -1)


    #Column wise scattering
    while (row < num_of_rows):
        C1 = 1;
        n = 100000;
        C2 = 1;
    
        # Create a new model
        m = gp.Model("mip1")
        
        v =[]
        for i in range(0,num_cluster_nodes):
            if assigned_row[i] == -1 :
                v.insert(i,m.addVar(vtype=GRB.BINARY, name="v%d" % (i)))
        m.update()
        
        #Vik1 = m.addVars(num_cluster_nodes,vtype=GRB.BINARY, name="Vik1")
        #number_of_cgra_clusters = 2;
        Epsilon = num_cluster_nodes/num_of_rows;
        
        #expr1= gp.LinExpr()
        expr1 = gp.quicksum(v) - Epsilon
        #expr1=gp.abs_(Vik1[0]+Vik1[1] - Epsilon)
        print(expr1)
        #for i in range(0,num_cluster_nodes):
            #expr1.add(Vik1[i])
        
        #gurobi doesn't support abs in objective. How to convert abs to supported format? Follow the link
        #http://lpsolve.sourceforge.net/5.1/absolute.htm
        #https://support.gurobi.com/hc/en-us/community/posts/360074428532-How-to-handle-absolute-value-in-objective-function-
        x_ = m.addVar(name = 'x_')
        
        m.setObjective(x_ , GRB.MINIMIZE)
        m.addConstr(expr1 <= x_)
        m.addConstr(-expr1 <= x_)
        #m.setObjective(gp.abs_(sum(Vik1[i] for i in range(0,num_cluster_nodes)) - Epsilon) , GRB.MINIMIZE)
        
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
                if assigned_row[node_id] == -1:
                    index_list = []
                    #index_list.append(nodes)
                    degree = 0
                    for neighbors in clus_dfg.neighbors(nodes):
                        #print(neighbors)
                        neighbor_id = int(neighbors)
                        if assigned_row[neighbor_id] == -1 :
                            index_list.append(neighbors)
                            index_list.append(nodes)
                            degree = degree + 1
                    #print(index_list)
                    for i in range(0,len(index_list)):
                        index_list[i] = int(index_list[i])
                
                #print(v[0])
                    print(index_list)
                    print(v)
                    #print(v[0])
                    #print(m.getVarByName("v6"))
                    #print(m.getVarByName("v9"))
                    if degree > 1:
                        print("Constraint 12:", sum(m.getVarByName(str("v"+str(i))) for i in index_list) <= C1 + n*m.getVarByName(str("v"+str(node_id))) )
                        m.addConstr(sum(m.getVarByName(str("v"+str(i))) for i in index_list) <= C1 + n*m.getVarByName(str("v"+str(node_id))) )
                        print("Constraint 13:", sum(m.getVarByName(str("v"+str(i))) for i in index_list) >= 2*degree - C2 - n*(1-m.getVarByName(str("v"+str(node_id)))  ))
                        m.addConstr(sum(m.getVarByName(str("v"+str(i))) for i in index_list) >= 2*degree - C2 - n*(1-m.getVarByName(str("v"+str(node_id)))  ))
                        num_of_constr = num_of_constr+2
                        print("")
            
            m.optimize()
        
            #print(clus_dfg.neighbors(nodes))
            
            #print("V0",v[0])
            for var in m.getVars():
                #print('%s %g' % (var.varName, var.x))
                if var.x == 1 :
                    found_solution = True
                    
            if found_solution == True:
                print("Found a solution at C1,C2  : ", C1,C2)
                for var in m.getVars():
                    print('%s %g' % (var.varName, var.x))
                    if str(var.varName[0]) =='v':
                        if var.x == 1:
                            print(int(var.varName[1:]))
                            assigned_row[int(var.varName[1:])] = row
                row = row + 1
            print('Obj: %g' % m.objVal)
            print("Constraint List:",m.getConstrs())
            print("Number of Constraints:",num_of_constr)
            m.remove(m.getConstrs()[2:(num_of_constr)])
            m.update()
            #print(m.getConstrs())
            C1 = C1+1
            C2 = C2+1
    
    for i in range(0,num_cluster_nodes):
        print("node,row",i,assigned_row[i])
        if (assigned_row[i]==-1):
            assigned_row[i]= num_of_rows-1
        
    #row wise scattering
    
    m = gp.Model("mip1")
    
    v =[]
    cid = []
    j=0
    for i in range(0,num_cluster_nodes):
        for c in range(1,num_of_columns+1):
            v.insert(j,m.addVar(vtype=GRB.BINARY, name="v%d%d" % (i,c)))
            cid.insert(j,cid)
            j=j+1
    m.update()
    #print(v)
    #for i in range(0,num_cluster_nodes*num_of_columns):
    #    print((i%num_of_columns+1)) 
    #    print(v[i])
    
    #14 maximize number of unexecuted column
    #objective = gp.quicksum([v[i]*(i%num_of_columns+1) for i in range(0,num_cluster_nodes*num_of_columns)]) 
   # print(objective)
    #m.setObjective(objective , GRB.MINIMIZE)
    
    # objective to minimize edge distance
    objective = gp.LinExpr()
    for edges in clus_dfg.edges:
        weight = int(clus_dfg[edges[0]][edges[1]]["label"])
        for c in range(1,num_of_columns+1):
            #print(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
            objective = objective + weight*(m.getVarByName(str("v"+str(edges[0])+str(c))) - m.getVarByName(str("v"+str(edges[1])+str(c))))
    
    print(objective)
    m.setObjective(objective , GRB.MINIMIZE)
    
    #15
    #m.addConstr()
    for i in range(0,num_cluster_nodes):
        #for c in range(1,num_of_columns+1):
            #print(m.getVarByName(str("v"+str(i)+str(c))))
        print(sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) == 1)
        m.addConstr(sum(m.getVarByName(str("v"+str(i)+str(c))) for c in range(1,(num_of_columns+1) )) == 1 )
    
    #16
    for c in range(1,num_of_columns+1):
        for r in range(0,num_of_rows):
            index_list=[]
            for i in range(0,num_cluster_nodes):
                if assigned_row[i]==r:
                    index_list.append(i)
            print(sum(m.getVarByName(str("v"+str(k)+str(c))) for k in index_list) <= 1)
            m.addConstr(sum(m.getVarByName(str("v"+str(k)+str(c))) for k in index_list) <= 1 )
    #17       
    for edges in clus_dfg.edges:
        print(clus_dfg[edges[0]][edges[1]]["label"])
        print(edges[0],edges[1])
        weight = int(clus_dfg[edges[0]][edges[1]]["label"])
        if weight > 4:
            for c in range(1,num_of_columns+1):
                print(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
                m.addConstr(m.getVarByName(str("v"+str(edges[0])+str(c))) == m.getVarByName(str("v"+str(edges[1])+str(c))))
        #print(sum( gp.abs_(c*m.getVarByName(str("v"+str(edges[0])+str(c))) - c*m.getVarByName(str("v"+str(edges[1])+str(c)))) for c in range(1,(num_of_columns+1) )) == 0)
    # Optimize model
    m.optimize()

    
        
    assigned_col = []
    for i in range(0,num_cluster_nodes):
        assigned_col.insert(i, -1)
        
    #for var in m.getVars():
        #print('%s %g' % (var.varName, var.x))
        
    print('Obj: %g' % m.objVal)
    for i in range(0,num_cluster_nodes):
        for c in range(1,num_of_columns+1):
            print(m.getVarByName(str("v"+str(i)+str(c))), m.getVarByName(str("v"+str(i)+str(c))).x)
            if m.getVarByName(str("v"+str(i)+str(c))).x == 1:
                assigned_col[i] = c
    
    for i in range(0,num_cluster_nodes):
        print("node: (row,col)",i,assigned_row[i],assigned_col[i])
        
    g = graphviz.Digraph('G', engine="neato", filename='cluster_map.gv', format='png')
    
    for i in range(0,num_cluster_nodes):
        #posit = str("'"+str(assigned_row[i])+","+str(assigned_col[i])+"!'")
        posit = str(""+str(assigned_col[i])+","+str(assigned_row[i])+"!")
        print(posit)
        g.node(str(i),pos=posit,color=colordict[i])
    
    for edges in clus_dfg.edges:
        g.edge(str(edges[0]),str(edges[1]))
    #pos1 = str('')
    #g.node('1', pos='1,2!')
    #g.node('2', pos='2,3!')
    #g.node('3',pos='0,0!')
    #g.edge('1','2')
    #g.edge('1','3')
    g.render()
    

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