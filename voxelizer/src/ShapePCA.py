'''
Created on 2012. 9. 21.

@author: jikhanjung
'''

from MdPCA import MdDatamatrix, MdPrincipalComponent
import os
import math
from numpy import *
import math
import numpy
import re

descriptors = [ "SHELL", "SECSHELL", "D2", "VOXEL" ]
NEWLINE = "\n"
no_of_object = 261

filepath = "category_data.txt"
f = open( filepath, 'r' )
categorydata = f.read()
f.close()

for descriptor in descriptors:

    category_data_list = []
    
    i = 0
    cat_lines = [ l.strip() for l in categorydata.split( NEWLINE ) ]
    for line in cat_lines:
            line = line.strip()
            data = re.split( '\t', line )
            category_data_list.append( data )
    
    filepath = descriptor + "_data.txt"
    f = open( filepath, 'r' )
    objdata = f.read()
    f.close()
    
    
    object_name_list = []
    object_data_list = []
    
    analyzed_name_list = []
    analyzed_data_list = []
    analyzed_category_data = []
    
    
    no_of_variables = 0
    
    i = 0
    dist_lines = [ l.strip() for l in objdata.split( NEWLINE ) ]
    is_first_line = True
    for line in dist_lines:
            
            line = line.strip() 
            data = re.split( '\t', line )
            if len( data ) > 2:
                    no_of_variables = len( data ) - 2 
                    object_name_list.append( data[0]  )
                    object_data_list.append( data[2:] )
                    #print i
                    if category_data_list[i][1] == "IR" or category_data_list[i][2] == "IR":
                        pass
                    else:        
                        analyzed_name_list.append( data[0] )
                        analyzed_data_list.append( data[2:] )
                        analyzed_category_data.append( category_data_list[i][1] )
                    i+= 1
    
    print "moving to shape_matrix"
    shape_matrix = numpy.zeros( ( no_of_variables, len( analyzed_name_list ) ) )
    for i in range( len( analyzed_name_list ) ):
            #print i
            shape_matrix[:,i] = analyzed_data_list[i]
    
    print shape_matrix
    
    pca = MdPrincipalComponent()
    pca.SetMatrix( shape_matrix )
    #print "a"
    pca.Analyze()
    print descriptor, "PCA result"
    print "-\t" + "\t".join( [ str(pct) for pct in pca.eigen_value_percentages[0:10] ] )
    #print pca.eigen_value_percentages[0:10]
    #for 
    for i in range( len( analyzed_name_list ) ):
        print analyzed_name_list[i] + "\t" + analyzed_category_data[i] + "\t" + "\t".join( [ str( val ) for val in pca.rotated_matrix[0:10,i] ])
