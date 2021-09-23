#!/usr/bin/env python
import sys
import os
import os.path
import shutil
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re
#from antlr4 import tree

import networkx as nx


import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import to_pydot
import pydot
from _ast import If



from mpl_toolkits import mplot3d
#matplotlib inline
import numpy as np
import matplotlib.pyplot as plt



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
    #xml_name = '/home/dmd/Workplace/HiMap2/Morpher_DFG_Generator/applications/picojpeg/idctCols_INNERMOST_LN1_PartPred_DFG_1.xml'
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')# Data for a three-dimensional line
    zline = np.linspace(0, 15, 1000)
    xline = np.sin(zline)
    yline = np.cos(zline)
    ax.plot3D(xline, yline, zline, 'gray')

    
    
  
def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
    #mapping = sys.argv[1]
    main()
