'''
Created on 2012. 9. 6.

@author: jikhanjung test
'''
from ThreeDShape import ThreeDShape
from MdPCA import MdDatamatrix, MdPrincipalComponent
import os
import math
import numpy

obj_list = []
fs = [] 
vxs = []
sizes = []
rotated_vs = []
fit_max = 0
fit_max = 7.0


def convert_obj_into_pickle( nvert = 5000 ):
    files = os.listdir( "D:/voxelizer_data/Coral_OBJ/")
    for fn in files:
        fn = fn.lower()

    ''' nvert pickle processing '''
    for fn in files: #nums:
    #fname = "Crystal_" + str( n ) + ".obj"
        fname = "D:/voxelizer_data/Coral_OBJ/" + fn
        ( name, ext ) = os.path.splitext( fn )
        if ext != ".obj":
            continue
        obj = ThreeDShape()
        print "loading", fname + "...", 
        obj.OpenObjFile( fname )
        
        print obj.no_of_vertices, "vertices", 
        obj.Simplify( nvert )
        print "simplified to", obj.no_of_vertices, "vertices"
        pkl1_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_original/" + name + ".pkl"
        if not os.path.exists( pkl1_fname ):
            obj.SaveAsPickle( pkl1_fname )


def load_files( nvert = 5000 ):
    max_abs_x = -9999
    max_abs_y = -9999
    max_abs_z = -9999
    max_dist = -9999
    real_max = -9999
    files = os.listdir( "D:/voxelizer_data/Coral_OBJ/")
    print files
    #for fn in files:
        #fn = fn.lower()

    ''' restore pickle and normalize '''
    for fn in files:
        ( name, ext ) = os.path.splitext( fn )
        if ext != ".obj": continue
        pkl_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_original/" + name + ".pkl"
        obj = ThreeDShape()
        obj.RestoreFromPickle( pkl_fname )
        obj.filename = name
        #print name, point_of_origin_data[name]
        point_of_origin = point_of_origin_data[name]
        #print point_of_origin
        pt = point_of_origin.split( )
        #print pt
        obj.point_of_origin = [ float(x) for x in pt ]
        #print obj.point_of_origin

        if obj.is_centered == False:
            #print "origin before center", obj.point_of_origin
            obj.center()
            #print "origin after center", obj.point_of_origin
        csize = obj.get_centroid_size( True )
        #print "before remove outlier", object.max_dist, object.min_dist, object.avg_dist
        if obj.outlier_removed == False:
            obj.remove_outlier()
            obj.center()
        if obj.is_aligned == False:
            #obj.align()
            #print"before align"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            obj.align_using_point_of_origin()
            #print"after origin align"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            obj.align_on_xy_plane()
            #print"after xy align"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            #print "origin after align", obj.point_of_origin
            obj.translate_using_origin()
            #print"after translate"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            #print "origin after translate", obj.point_of_origin
        csize = obj.get_centroid_size( True )
        #print "after remove outlier", object.max_dist, object.min_dist, object.avg_dist
        #print object.avg_dist
        #print_log( fname + "\n")
        #print_log( "\n".join( [ fname, str(object.no_of_vertices), str(object.get_centroid_size()) ] ) )
        obj.scale( (1.0/obj.avg_dist) )
        obj.get_centroid_size(True)

        #print "after scale", object.max_dist, object.min_dist, object.avg_dist
        max_abs_x = max( abs( obj.max_x ) , abs( obj.min_x ), max_abs_x )
        max_abs_y = max( abs( obj.max_y ) , abs( obj.min_y ), max_abs_y )
        max_abs_z = max( abs( obj.max_z ) , abs( obj.min_z ), max_abs_z )
        max_dist = max( obj.max_dist, max_dist )
        real_max = max( max_abs_x, max_abs_y, max_abs_z, real_max )

        obj_list.append( obj )
    
    #rotated_vs.append( rotated_v )
    #fs.append( f )

    factor = fit_max / max_dist
#print real_max, factor, max_dist

    print "scaling..."
    for obj in obj_list:
  #print "before", obj.get_centroid_size(), 
  #print obj.min_dist, obj.max_dist
        obj.scale( factor ) 
        obj.scale_factor = factor
        #obj.calculate_D2()
        #print obj.name
        #print "after", obj.get_centroid_size(),
        #print obj.min_dist, obj.max_dist
    print "scaling done!"
    max_x = math.ceil( max( [ obj.max_x for obj in obj_list ]) )
    min_x = math.floor( min( [ obj.min_x for obj in obj_list ]) )
    max_y = math.ceil( max( [ obj.max_y for obj in obj_list ]) )
    min_y = math.floor( min( [ obj.min_y for obj in obj_list ]) )
    max_z = math.ceil( max( [ obj.max_z for obj in obj_list ]) )
    min_z = math.floor( min( [ obj.min_z for obj in obj_list ]) )
    print max_x, min_x, max_y, min_y, max_z, min_z

    for obj in obj_list:
        if obj.is_voxelized == False:
            #print "make voxels"
            obj.get_voxels( min_x, max_x, min_y, max_y, min_z, max_z )
            #obj.print_voxels()
  
    for obj in obj_list:
        pkl_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_processed/" + obj.filename + ".pkl"
        if not os.path.exists( pkl_fname ):
            obj.SaveAsPickle( pkl_fname )

    tps_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_tps/" + "coral_" + str(nvert) + ".tps"
    tps_string = ""
    for obj in obj_list:
        tps_string += obj.ToTpsString()
    f = open( tps_fname, "wb" )
    f.write( tps_string )
    f.close()
    
    
convert_obj_into_pickle()
#sys.exit()
