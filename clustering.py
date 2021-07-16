#!/usr/bin/env python
import sys
import os
import os.path
import shutil
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re
from antlr4 import tree

import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
from sklearn import metrics
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import to_pydot
from sklearn.cluster._agglomerative import AgglomerativeClustering
import pydot
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

def main():
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/aes/hycube_compilation/encrypt_INNERMOST_LN1_PartPred_DFG_without_clustering_1.xml'
    #xml_name = '//home/dmd/Workplace/Morphor/github_ecolab_repos/Morpher_DFG_Generator/applications/madgwick_fp_v2/MadgwickAHRSupdateIMU_INNERMOST_LN1_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/edn/jpegdct_POST_LN111_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/nettle-sha256/_nettle_sha256_compress_INNERMOST_LN1_PartPred_DFG_2.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/nsichneu/benchmark_body_INNERMOST_LN1_PartPred_DFG_1.xml'
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/picojpeg/idctRows_INNERMOST_LN1_PartPred_DFG_1.xml'
    xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/picojpeg/idctCols_INNERMOST_LN1_PartPred_DFG_1.xml'
    
    
    #https://www.datacamp.com/community/tutorials/python-xml-elementtree
    #tree = ET.fromstring(xml_name)
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(xml_name, parser=parser)
    root = tree.getroot()
    print(root.tag)
    print(root.attrib)
    
    DFG = nx.DiGraph()
    for nodes in root:
        print(nodes.tag, nodes.attrib)
        print(nodes.attrib["idx"])
        #DFG.add_node(nodes.attrib["idx"])
        for nodeelm in nodes:
            #print(nodeelm.tag, nodeelm.attrib)
            if nodeelm.tag == 'Outputs':
                for outputs in nodeelm:
                    print(outputs.tag, outputs.attrib)
                    DFG.add_edge(nodes.attrib["idx"], outputs.attrib["idx"])
    print(ET.tostring(tree.getroot()))
    #tree = ET.parse('/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/aes/hycube_compilation/encrypt_INNERMOST_LN1_PartPred_DFG_without_clustering_1.xml')
    #with open("/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/aes/hycube_compilation/encrypt_INNERMOST_LN1_PartPred_DFG_without_clustering_1.xml") as f:
    #    xml = f.read()
    #tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
    #root = tree.getroot()
    #root.tag
    #doc = xml.dom.minidom.parse("/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/aes/hycube_compilation/encrypt_INNERMOST_LN1_PartPred_DFG_without_clustering_1.xml")
    print('\nRunning Morpher_DFG_Generator\n')
    MORPHER_HOME = os.getenv('MORPHER_HOME')

    np.random.seed(1)

    print(DFG.number_of_nodes())
# Get your mentioned graph
    #G = nx.karate_club_graph()
    #plt.subplot(121)
    #nx.draw_spectral(G, with_labels=True, font_weight='bold')
    #plt.subplot(122)
    #nx.draw_spectral(DFG, with_labels=True, font_weight='bold')
    #plt.show()

    #pos = nx.nx_agraph.graphviz_layout(G)

    #nx.draw(G, pos=pos)

   # write_dot(G, 'file.dot')
    


# Get ground-truth: club-labels -> transform to 0/1 np-array
#     (possible overcomplicated networkx usage here)
    #gt_dict = nx.get_node_attributes(G, 'club')
    #gt = [gt_dict[i] for i in G.nodes()]
    #gt = np.array([0 if i == 'Mr. Hi' else 1 for i in gt])

# Get adjacency-matrix as numpy-array
    #adj_mat = nx.to_numpy_matrix(G)

    #print('ground truth')
    #print(gt)

# Cluster
    #sc = SpectralClustering(2, affinity='precomputed', n_init=100)
    #sc.fit(adj_mat)

# Compare ground-truth and clustering-results
    #print('spectral clustering')
    #print(sc.labels_)
    #print('just for better-visualization: invert clusters (permutation)')
    #print(np.abs(sc.labels_ - 1))

# Calculate some clustering metrics
    #print(metrics.adjusted_rand_score(gt, sc.labels_))
    #print(metrics.adjusted_mutual_info_score(gt, sc.labels_))
    
    adj_mat_dfg = nx.to_numpy_matrix(DFG)
    # Cluster
    scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)#madgwick
    #scdfg = SpectralClustering(7, affinity='precomputed', n_init=100)//aes
    #scdfg = AgglomerativeClustering(7, affinity='precomputed', linkage='average')
    #https://stackoverflow.com/questions/46258657/spectral-clustering-a-graph-in-python
    #https://ptrckprry.com/course/ssd/lecture/community.html
    scdfg.fit(adj_mat_dfg)
    
    print('spectral dfg clustering')
    print(scdfg.labels_)
    #i = 0
    #for nodes in DFG.nodes:
    #    nx.set_node_attributes(nodes, scdfg.labels_[i], "cluster_id")
    #    i = i+1
    #nx.set_node_attributes(DFG, scdfg.labels_, "cluster_id")
    #print(DFG.nodes[0]["cluster_id"])
    #print(DFG.nodes[2]["cluster_id"])    
    
    #print("pos DFG")   
    #pos = nx.nx_agraph.graphviz_layout(DFG, prog='dot')
    

    #nx.draw(DFG, pos=pos,cmap=plt.get_cmap('viridis'),  node_color = scdfg.labels_, with_labels=True, font_color='white')
    #https://stackoverflow.com/questions/13517614/draw-different-color-for-nodes-in-networkx-based-on-their-node-value
    #plt.show()
    #write_dot(DFG, 'dfg.dot')
    
    #p=to_pydot(DFG)
    #print("writing dot dfg")   
    #p.write_png('example.png')
    
    node_list = list(DFG)
    clustering_outcome = xml_name + "_clustering_outcome.txt"
    i=0
    with open(clustering_outcome, "w") as f:
        for i in range(0, DFG.number_of_nodes()):
            #node_id = nodes.attrib["idx"]
            print(node_list[i],scdfg.labels_[i]) 
            f.write(str(node_list[i]) + '\t' + str(scdfg.labels_[i]) + '\n')
            i=i+1
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
    
    print("adding nodes to colored dot dfg")
    for nodes in DFG.nodes:
        #print(colordict[scdfg.labels_[i]])
        pydot_dfg.add_node(pydot.Node(nodes, fontcolor="white", style="filled", fillcolor=colordict[scdfg.labels_[i]]))
        i = i+1
        
    print("adding edges to colored dot dfg")    
    for edges in DFG.edges:
        #print(edges)
        #print(edges[0],edges[1])
        pydot_dfg.add_edge(pydot.Edge(edges[0],edges[1]))
        print(edges[0],edges[1])
    print("adding edges to colored dot dfg")    
    
    pydot_dfg.write_png('dfg.png')
    #pydot_dfg.write_pdf('dfg.pdf')
    print("Done")
    

    #https://www.programcreek.com/python/example/105084/networkx.drawing.nx_agraph.graphviz_layout
  
def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
  main()
