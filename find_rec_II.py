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

def main(dfg_xml):
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/aes/hycube_compilation/encrypt_INNERMOST_LN1_PartPred_DFG_without_clustering_1.xml'
    #xml_name = '//home/dmd/Workplace/Morphor/github_ecolab_repos/Morpher_DFG_Generator/applications/madgwick_fp_v2/MadgwickAHRSupdateIMU_INNERMOST_LN1_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/edn/jpegdct_POST_LN111_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/nettle-sha256/_nettle_sha256_compress_INNERMOST_LN1_PartPred_DFG_2.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/nsichneu/benchmark_body_INNERMOST_LN1_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/picojpeg/idctRows_INNERMOST_LN1_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/picojpeg/idctCols_INNERMOST_LN1_PartPred_DFG_1.xml'
    
    
    #https://www.datacamp.com/community/tutorials/python-xml-elementtree
    #tree = ET.fromstring(xml_name)
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(dfg_xml, parser=parser)
    root = tree.getroot()
    #print(root.tag)
    #print(root.attrib)
    
    DFG = nx.DiGraph()
    
    for nodes in root:
        #print(nodes.tag, nodes.attrib)
        #print(nodes.attrib["idx"])
        for nodeelm in nodes:
            #print(nodeelm.tag, nodeelm.attrib)
            if nodeelm.tag == 'Outputs':
                for outputs in nodeelm:
                    #print(outputs.tag, outputs.attrib)
                    DFG.add_edge(nodes.attrib["idx"], outputs.attrib["idx"])

    np.random.seed(1)

    print(DFG.number_of_nodes())
    
    print('simple cycles')
    
    print(list(nx.simple_cycles(DFG)))
    
    
    #adj_mat_dfg = nx.to_numpy_matrix(DFG)
    # Cluster
    
    '''
    print('no_clusters affinity no_init')
    print(no_clusters, affinity_, no_init)
    scdfg = SpectralClustering(int(no_clusters), affinity=str(affinity_), n_init=int(no_init))
    #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)#madgwick
    #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)//aes
    #scdfg = AgglomerativeClustering(7, affinity='precomputed', linkage='average')
    #https://stackoverflow.com/questions/46258657/spectral-clustering-a-graph-in-python
    #https://ptrckprry.com/course/ssd/lecture/community.html
    scdfg.fit(adj_mat_dfg)
    
    print('spectral dfg clustering')
    #print(scdfg.labels_)
    
    node_list = list(DFG)
    nodeid_clusterlabel_dict = {}
    clustering_outcome = "clustering_outcome.txt"
    i=0
    with open(clustering_outcome, "w") as f:
        for i in range(0, DFG.number_of_nodes()):
            #node_id = nodes.attrib["idx"]
            #print(node_list[i],scdfg.labels_[i]) 
            f.write(str(node_list[i]) + '\t' + str(scdfg.labels_[i]) + '\n')
            nodeid_clusterlabel_dict[node_list[i]] = scdfg.labels_[i]
            i=i+1
    f.close()
    #pydot graph
    #https://pypi.org/project/pydot/
    pydot_dfg = pydot.Dot('DFG',graph_type='graph')
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
    i=0
    #https://graphviz.org/doc/info/attrs.html
    
    #print("adding nodes to colored dot dfg")
    for nodes in DFG.nodes:
        #print(colordict[scdfg.labels_[i]])
        pydot_dfg.add_node(pydot.Node(nodes, fontcolor="white", style="filled", fillcolor=colordict[scdfg.labels_[i]]))
        i = i+1
    
    
    #print("adding edges to colored dot dfg")    
    for edges in DFG.edges:
        #print(edges)
        #print(edges[0],edges[1])
        pydot_dfg.add_edge(pydot.Edge(edges[0],edges[1]))
        #print(edges[0],edges[1]) 
    
    
    pydot_dfg.write_png('clustered.png')
    
    print(nodeid_clusterlabel_dict)
    
    #print("Inter cluster edges:")
    total_edges = 0
    inter_cluster_edges = 0
    with open("inter_cluster_edges.txt", "w") as f:
        for edges in DFG.edges:
            total_edges = total_edges + 1
            if nodeid_clusterlabel_dict[edges[0]] != nodeid_clusterlabel_dict[edges[1]]:
                #print(edges[0],edges[1])
                f.write(str(edges[0]) + '\t' + str(edges[1]) + '\n')
                inter_cluster_edges = inter_cluster_edges + 1
    f.close()
    
    
    with open("all_edges.txt", "w") as f:
        for edges in DFG.edges:
            f.write(str(edges[0]) + '\t' + str(edges[1]) + '\n')
    f.close()
    #print("Total edges:",total_edges)       
    #print("Inter cluster edges:",inter_cluster_edges)
    #print("Total nodes:", DFG.number_of_nodes())
    #pydot_dfg.write_pdf('dfg.pdf')
    #print("Done")
    
    CLUS_DFG = nx.DiGraph()
    for i in range(0, int(no_clusters)):
        CLUS_DFG.add_node(i, label = 0, color=colordict[i])
        
    for i in range(0, DFG.number_of_nodes()): 
        CLUS_DFG.nodes[nodeid_clusterlabel_dict[node_list[i]]]["label"] = CLUS_DFG.nodes[nodeid_clusterlabel_dict[node_list[i]]]["label"] + 1
    
    #print("Inter cluster edges:")
    total_edges = 0
    inter_cluster_edges = 0
    for edges in DFG.edges:
        total_edges = total_edges + 1
        if nodeid_clusterlabel_dict[edges[0]] != nodeid_clusterlabel_dict[edges[1]]:
            if CLUS_DFG.has_edge(nodeid_clusterlabel_dict[edges[0]], nodeid_clusterlabel_dict[edges[1]]):
                CLUS_DFG[nodeid_clusterlabel_dict[edges[0]]][nodeid_clusterlabel_dict[edges[1]]]['label'] = CLUS_DFG[nodeid_clusterlabel_dict[edges[0]]][nodeid_clusterlabel_dict[edges[1]]]['label'] + 1
                inter_cluster_edges = inter_cluster_edges + 1
            else:
                CLUS_DFG.add_edge(nodeid_clusterlabel_dict[edges[0]], nodeid_clusterlabel_dict[edges[1]], label=1)
                #print(nodeid_clusterlabel_dict[edges[0]], nodeid_clusterlabel_dict[edges[1]])
                inter_cluster_edges = inter_cluster_edges + 1
                
    print("Total edges:",total_edges)       
    print("Inter cluster edges:",inter_cluster_edges)
    print("Total nodes:", DFG.number_of_nodes())        
  
    #https://graphviz.org/doc/info/attrs.html
    
    write_dot(CLUS_DFG,'inter_cluster.dot')
    
    # Number of nodes in each cluster
    print("Number of nodes in each cluster:")    
    with open("number_of_nodes_in_each_cluster.txt", "w") as f:
        for i in range(0,int(no_clusters)): 
            print(i,CLUS_DFG.nodes[i]['label'],(CLUS_DFG.nodes[i]['label']/DFG.number_of_nodes())*100)
            f.write(str(i) + '\t'+ str(CLUS_DFG.nodes[i]['label']) + '\t' +str((CLUS_DFG.nodes[i]['label']/DFG.number_of_nodes())*100) + '\n')
    f.close()
    nx.write_gexf(CLUS_DFG, 'inter_cluster.gexf')
    #https://www.programcreek.com/python/example/105084/networkx.drawing.nx_agraph.graphviz_layout
    '''
    
    
  
def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
    dfg_xml = sys.argv[1]
    main(dfg_xml)
