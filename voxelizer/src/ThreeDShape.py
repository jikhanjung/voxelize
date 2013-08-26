'''
Created on 2012. 9. 6.

@author: jikhanjung
'''
import pickle
import random
import os
import re
import math
from numpy import *
import numpy
NEWLINE = "\n" 
X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2

class ThreeDShape:
  def __init__(self):
    scale = 1
    self.orig_verts = {}
    self.verts = {}
    self.faces = {}
    self.verts_in_sphere = {}
    self.dists = {}
    self.centroid_size = -1
    self.point_of_origin = []

    self.is_centered = False
    self.is_aligned = False
    self.is_voxelized = False
    self.outlier_removed = False

    self.name = ""
    self.max_x = 0
    self.max_y = 0
    self.max_z = 0
    self.avg_dist = 0
    self.scale_factor = 1.0
    self.max_D2_dist = -9999
    self.min_D2_dist = 9999

    self.D2_dist_list = []
    self.dist_dist_list = []
    self.dist_dist_list_pct = []
    self.sp_dist = []
    self.sp_dist_pct = []

  def ToTpsString(self):
        tpsstring = "lm=" + str( len( self.verts ) ) + " " + self.filename + "\n"
        tpsstring += " ".join( [ str( x ) for x in self.point_of_origin ] ) + "\n" 
        for k in self.verts.keys():
            tpsstring += " ".join( [ str( x ) for x in self.verts[k] ] ) + "\n"
        return tpsstring
  def SaveAsTps(self,path):
        f = open( path, 'wb' )
        f.write( self.ToTpsString() )
        f.close()
  def SaveAsPickle(self, path):
        output = open( path, 'wb' )
        pickle.dump( self, output )
        output.close()

  def RestoreFromPickle(self, path ):
        pkl_file = open( path, "rb" )
        data = pickle.load( pkl_file )
        print data.name, data.no_of_vertices, "vertices"
        
        self.verts = data.verts
        self.no_of_vertices = data.no_of_vertices
        self.avg_dist = data.avg_dist
        self.max_x = data.max_x
        self.max_y = data.max_y
        self.max_z = data.max_z
        return

  def Simplify(self,n_vert=1000):
    #n_total_vert = self.no_of_vertices
    print "simplify"
    if self.no_of_vertices <= n_vert: return
    print "begins.", len( self.verts.keys() ), "verts,", len( self.faces.keys()), "faces,"#, self.voxels.shape, "voxels."
    new_verts = {}
    idx_list = []
    for i in range( n_vert ):
        idx = int( random.random() * self.no_of_vertices )
        while( idx in idx_list or idx not in self.verts.keys() ):          
            idx = int( random.random() * self.no_of_vertices )
        new_verts[i] = self.verts[idx]
    self.verts = new_verts
    self.orig_verts = {}
    self.faces = {}
    self.dists = {}
    self.verts_in_sphere = {}
    self.no_of_vertices = len( self.verts.keys() )

    self.D2_dist_list = []
    self.dist_dist_list = []
    self.dist_dist_list_pct = []
    self.sp_dist = []
    self.sp_dist_pct = []

    print "simplify done.", len( self.verts.keys() ), "verts,", len( self.faces.keys()), "faces,"#, self.voxels.shape, "voxels."
    
  def OpenObjFile(self, filepath, load_faces = False, use_pickle = True ):
    if os.path.exists( filepath + ".pkl" ) and use_pickle:
        self.name = filepath
        self.RestoreFromPickle()
        return
            
    self.name = filepath
    verts = {}
    faces = {}
    vert_exist = {}
    num_v = 1
    num_f = 1  
    scale = 1

    f = open( filepath, 'r' )
    #objdata = f.read()
    

    #obj_lines = [ l.strip() for l in objdata.split( NEWLINE ) ]
    for line in f:
      line = line.strip() 
      fpoint = re.split( '\s+', line )
      if fpoint[0] == 'v':
        x, y, z = float( fpoint[1] ), float( fpoint[2] ), float( fpoint[3] )
        verts[num_v] = [ x/scale, y/scale, z/scale ]
        num_v += 1 
      if fpoint[0] == 'f' and load_faces:
        #print line
        #print fpoint, fpoint[1:]
        f_vert = []
        for point in fpoint[1:]:
          p_split = point.split( "/" )
          if len( p_split ) > 0:
            v_idx = int( p_split[0] )
            f_vert.append( v_idx )
            vert_exist[v_idx] = 1
        faces[num_f] = f_vert
        #print f_vert
        num_f += 1
    f.close()
    real_verts = {}
    for k in vert_exist.keys():
      real_verts[k] = verts[k]

    self.faces = faces
    self.verts = verts #self.orig_verts = verts  
    self.no_of_vertices = len( verts.keys() )
    return

  def remove_outlier(self):
    sum = 0
    dist_avg = 0
    dist_diff = {}
    ids = self.dists.keys()
    num_dist = len(ids)
    for id in ids:
      sum += self.dists[id]
    dist_avg = sum / num_dist
    #max_diff = -9999
    #min diff = 9999
    sum_sq_diff = 0
    for id in ids:
      diff = self.dists[id] - dist_avg
      sum_sq_diff += diff ** 2.0
      dist_diff[id] = diff
    var = sum_sq_diff / num_dist
    std = var ** 0.5
    max_dist = max( self.dists.values() )
    min_dist = min( self.dists.values() )
    #print dist_avg, var, std, max_dist, min_dist
    for id in ids:
      if abs( dist_diff[id] ) > 5 * std:
        del dist_diff[id]
        del self.verts[id]
        del self.dists[id]
    max_dist = max( self.dists.values() )
    min_dist = min( self.dists.values() )
    #print dist_avg, var, std, max_dist, min_dist
    self.outlier_removed = True
    self.is_centered = False

  def center( self ): 
    ( max_x, max_y, max_z ) = ( -9999, -9999, -9999 )
    ( min_x, min_y, min_z ) = ( 9999, 9999, 9999 )
    #print len( verts )
    #return
    
    verts = self.verts
    new_verts = {}
    x_sum, y_sum, z_sum = 0, 0, 0
    for id in verts.keys( ):
      x, y, z = verts[id]
      x_sum += x
      y_sum += y
      z_sum += z
      max_x = max( x, max_x )
      max_y = max( y, max_y )
      max_z = max( z, max_z )
      min_x = min( x, min_x )
      min_y = min( y, min_y )
      min_z = min( z, min_z )
    n_vert = len( verts.keys() )
    x_avg = x_sum / n_vert
    y_avg = y_sum / n_vert
    z_avg = z_sum / n_vert
    max_x -= x_avg
    max_y -= y_avg
    max_z -= z_avg
    min_x -= x_avg
    min_y -= y_avg
    min_z -= z_avg
    
    #print max_x, max_y, max_z, min_x, min_y, min_z\
    for id in verts.keys( ):
      x, y, z = verts[id]
      x -= x_avg
      y -= y_avg
      z -= z_avg
      verts[id] = [ x, y, z ]
    self.point_of_origin[0] -= x_avg
    self.point_of_origin[1] -= y_avg
    self.point_of_origin[2] -= z_avg
      #new_verts.setdefault( ( x - min_x, y - min_y, z - min_z ), set() ).add( id ) #[id] = [ x - min_x, y - min_y, z - min_z ]
    self.max_x = max_x
    self.max_y = max_y
    self.max_z = max_z
    self.min_x = min_x
    self.min_y = min_y
    self.min_z = min_z
    self.verts = verts
    self.is_centered = True
    #return verts, max_x, min_x, max_y, min_y, max_z, min_z

  def get_centroid_size(self, calculate_anyway = False ):
    if not calculate_anyway and self.centroid_size > 0:
      return self.centroid_size
    
    #if not self.is_centered:
    #  self.center()
    sum_of_squares = 0
    min_dist = 9999
    max_dist = -9999
    dists = {}
    sum_dist = 0
    for id in self.verts.keys( ):
      x, y, z = self.verts[id]
      sum_of_squares += x**2 + y**2 + z**2 
      dist = ( x**2 + y**2 + z** 2 ) ** 0.5
      sum_dist += dist
      min_dist = min( min_dist, dist )
      max_dist = max( max_dist, dist )
      dists[id] = dist 
      #if int( id ) < 10:
      #  print "x,y,z", x, y, z
    #print "sum of squares", sum_of_squares, self.no_of_vertices
    sss = sum_of_squares ** 0.5
    #print "sss", sss
    self.centroid_size = ( sss ) 
    self.min_dist = min_dist
    self.max_dist = max_dist 
    self.avg_dist = sum_dist / len( self.verts.keys() )
    self.dists = dists
    return self.centroid_size

  def rotate_on_axis(self,angle,axis):
    if axis == X_AXIS:
        idx1 = 1
        idx2 = 2
    elif axis == Y_AXIS:
        idx1 = 0
        idx2 = 2
    elif axis == Z_AXIS:
        idx1 = 0
        idx2 = 1

    ks = self.verts.keys()
    rotate = numpy.zeros( (3,3) )
    for i in range(3):
        rotate[i,i] = 1
    rotate[idx1,idx1] = rotate[idx2,idx2] = math.cos( angle )
    rotate[idx2,idx1] = math.sin( angle )
    rotate[idx1,idx2] = -1.0 * math.sin( angle )
    #self.rotated_verts = {}
    for k in ks:
        #x, y, z = self.verts[k]
        #print self.verts[k],
        vec = numpy.zeros( ( 3 ) )
        vec[:] = self.verts[k][:]
        rotated_vec = numpy.dot( rotate, vec )
        self.verts[k] = rotated_vec[:]
        #print self.verts[k]
      
    ''' rotate point of origin as well''' 
    vec = numpy.zeros( ( 3 ) )
    vec[:] = self.point_of_origin[:]
    rotated_vec = numpy.dot( rotate, vec )
    self.point_of_origin[:] = rotated_vec[:]
      

  def rotate(self, theta, phi ):
    ks = self.verts.keys()
    rotate_theta = numpy.zeros( (3,3) )
    rotate_phi = numpy.zeros( (3,3) )
    for i in range(3):
      rotate_theta[i,i] = 1
      rotate_phi[i,i] = 1
    rotate_phi[0,0] = rotate_phi[1,1] = math.sin( phi)
    rotate_phi[0,1] = math.cos(phi)
    rotate_phi[1,0] = -1.0 * math.cos(phi)
    rotate_theta[0,0] = rotate_theta[2,2] = math.sin( theta )
    rotate_theta[0,2] = math.cos(theta)
    rotate_theta[2,0] = -1.0 * math.cos(theta)
    #self.rotated_verts = {}
    for k in ks:
      #x, y, z = self.verts[k]
      vec = numpy.zeros( ( 3 ) )
      vec[:] = self.verts[k][:]
      rotated_vec = numpy.dot( rotate_phi, numpy.dot( rotate_theta, vec ) )
      self.verts[k] = rotated_vec[:]
      
    ''' rotate point of origin as well''' 
    vec = numpy.zeros( ( 3 ) )
    vec[:] = self.point_of_origin[:]
    rotated_vec = numpy.dot( rotate_phi, numpy.dot( rotate_theta, vec ) )
    self.point_of_origin[:] = rotated_vec[:]
    #self.verts = self.rotated_verts

  def translate_using_origin(self):
      for k in self.verts.keys():
          x, y, z = self.verts[k] 
          ox, oy, oz = self.point_of_origin
          x -= ox
          y -= oy
          z -= oz
          self.verts[k] = [ x, y, z ]
      self.point_of_origin = [ 0,0,0 ]

  def align_using_point_of_origin(self):
      #for k in self.verts.keys()[0:10]:
      #    print self.verts[k]
          
      #print self.point_of_origin
      x, y, z = self.point_of_origin
      sin_val = y / math.sqrt( x*x + y*y )
      angle = math.degrees( math.asin(sin_val) )
      if x < 0: angle = 180 - angle
      rotate_angle = 90 - angle
      rotate_angle_radian = math.radians( rotate_angle )
      
      self.rotate_on_axis( rotate_angle_radian, Z_AXIS )
      #print self.point_of_origin

      x, y, z = self.point_of_origin
      sin_val = z / math.sqrt( y*y + z*z )
      angle = math.degrees( math.asin(sin_val ))
      if y < 0: angle = 180 - angle
      rotate_angle = ( 90 - angle ) + 180 
      rotate_angle_radian = math.radians( rotate_angle )
      self.rotate_on_axis( rotate_angle_radian, X_AXIS ) 

      #for k in self.verts.keys()[0:10]:
      #    print self.verts[k]
      
      #print self.point_of_origin
      self.is_aligned = True
      return

  def align_on_xy_plane(self):    
    ks = self.verts.keys()
    matrix = numpy.zeros( ( 2, len( ks ) ) )
    i = 0
    for k in ks:
      matrix[0,i] = self.verts[k][0]
      matrix[1,i] = self.verts[k][1]
      i+= 1
  
    pca = MdPrincipalComponent()
    pca.SetMatrix( matrix )
    #print "a"
    pca.Analyze()
    #print pca.rotated_matrix
    #print "rotation:", pca.rotation_matrix
    new_verts = {}
    i = 0
    for k in ks:
      vert = []
      vert[:] = pca.rotated_matrix[:,i]
      vert.append( self.verts[k][2] )
      new_verts[k] = vert
      i+=1
    #print "rotation", pca.rotation_matrix
    self.rotation_matrix = pca.rotation_matrix
    self.is_aligned = True
    self.verts = new_verts
  
  def align(self):
    
    ks = self.verts.keys()
    matrix = numpy.zeros( ( 3, len( ks ) ) )
    i = 0
    for k in ks:
      matrix[:,i] = self.verts[k][:]
      i+= 1
  
    pca = MdPrincipalComponent()
    pca.SetMatrix( matrix )
    #print "a"
    pca.Analyze()
    #print pca.rotated_matrix
    #print "rotation:", pca.rotation_matrix
    new_verts = {}
    i = 0
    for k in ks:
      new_verts[k] = pca.rotated_matrix[:,i]
      i+=1
    #print "rotation", pca.rotation_matrix
    self.rotation_matrix = pca.rotation_matrix
    self.is_aligned = True
    self.verts = new_verts

  def scale(self, factor = -1):
    if factor < 0 : return
    #print "before scale", self.centroid_size
    new_verts = {}
    for id in self.verts.keys( ):
      x, y, z = self.verts[id]
      new_x, new_y, new_z = x * factor, y * factor, z * factor 
      new_verts[id] = [ new_x, new_y, new_z ]
      #self.scaled_verts[id] = [ new_x, new_y, new_z ]
      #if int( id ) < 10:
        #print "old x,y,z", x, x*factor, y, y*factor, z, z*factor
        #print "new x,y,z", new_verts[id]

    ''' scale point of origin '''
    x, y, z = self.point_of_origin
    new_x, new_y, new_z = x * factor, y * factor, z * factor
    self.point_of_origin = [ new_x, new_y, new_z ]  

    
    self.verts = new_verts
    self.get_centroid_size( True )
    #print "after scale", self.centroid_size
    self.max_x *= factor
    self.max_y *= factor
    self.max_z *= factor
    self.min_x *= factor
    self.min_y *= factor
    self.min_z *= factor
    return

  def get_voxels( self, min_x, max_x, min_y, max_y, min_z, max_z ):
    #print "min, max", min_x, max_x, min_y, max_y, min_z, max_z
    dim_x = max_x-min_x+3
    dim_y = max_y-min_y+3
    dim_z = max_z-min_z+3
    data = numpy.zeros((dim_x, dim_y, dim_z))
    
    #print dim_x, dim_y, dim_z
    count = 0
    for id in self.verts.keys():
        x, y, z = [ int( math.floor( co ) ) for co in self.verts[id] ]
        if y-min_y >= dim_y or z-min_z >= dim_z or x-min_x>=dim_x:
            print x, y, z
        if data[x-min_x,y-min_y,z-min_z] == 0:
            data[x-min_x,y-min_y,z-min_z]+= 1
            count += 1
    '''        
    for id in self.faces.keys():
      vs = self.faces[id]
      #print vs
      ( mx_x, mx_y, mx_z ) = ( -9999, -9999, -9999 )
      ( mn_x, mn_y, mn_z ) = ( 9999, 9999, 9999 )
      for v in vs:
        if v in self.verts.keys():
          x, y, z = [ int( math.floor( co ) ) for co in self.verts[v] ]
          #print v, self.verts[v], x, y, z
          #if int(id)<10: print x, y, z
          mx_x = max( mx_x, x )
          mx_y = max( mx_y, y )
          mx_z = max( mx_z, z )
          mn_x = min( mn_x, x )
          mn_y = min( mn_y, y )
          mn_z = min( mn_z, z )
      #if mx_x - mn_x > 1 or mx_y - mn_y > 1 or mx_z - mn_z > 1: print mx_x - mn_x, mx_y - mn_y, mx_z - mn_z  
      #print "x,y,z", mx_x, mx_y, mx_z, mn_x, mn_y, mn_z
      for x in range( mn_x, mx_x + 1):
        for y in range( mn_y, mx_y + 1):
          for z in range( mn_z, mx_z + 1):
            #if x
            #print x-min_x, y-min_y, z-min_z
            if data[x-min_x,y-min_y,z-min_z] == 0:
              data[x-min_x,y-min_y,z-min_z]+= 1
              count += 1
    '''

    self.no_of_filled_voxels = count
    #print "dim", data.shape, "count", count
    self.voxels = data
    self.is_voxelized = True
    return data

  def print_voxels(self):
    z = 0
    (max_x,max_y,max_z)= self.voxels.shape
    if z > 0:
      from_z = z-1
      to_z = z
    else:
      from_z = 0
      to_z = max_z
    retstr = ""
    count = 0
    for z in range( from_z, to_z):
      for y in range( max_y ):
        retstr += "|"
        for x in range( max_x ):
          n = int(self.voxels[x,y,z])
          if n != 0:
            if n > 9 : n = 9
            retstr += str(n)
            count += 1
          else:
            retstr += " "
        retstr += "|\n"
      retstr += str(z)+"------------\n"
    print_log( self.name )
    print_log( retstr )
    print self.name
    print retstr
    return count
    
  def voxel_as_vector(self):
    x, y, z = self.voxels.shape
    vlen = x * y * z
    return self.voxels.reshape( vlen, 1 )

  def calculate_D2(self):
    D2_dist_list = []
    for k1 in self.verts.keys():
      for k2 in self.verts.keys() :
        if k1 != k2:
          x1, y1, z1= self.verts[k1]
          x2, y2, z2= self.verts[k1]
          dist = ((x2-x1)**2.0 + (y2-y1)**2.0 + (z2-z1)**2.0 ) ** 0.5
          D2_dist_list.append( dist )
    max_d = max( D2_dist_list )
    min_d = min( D2_dist_list )
    self.max_D2_dist = max_d
    self.min_D2_dist = min_d
    self.D2_dist_list = D2_dist_list
  def get_D2_distribution(self, max_dist, no_of_bin):
    bin_size = float( max_dist ) / float( no_of_bin )
    bins = numpy.zeros(no_of_bin)
    c = 0
    ks = self.verts.keys()
    
    for i in range( len( ks ) - 1 ):
      #print i
      for j in range( i+1, len(ks)):
          x1, y1, z1= self.verts[ks[i]]
          x2, y2, z2= self.verts[ks[j]]
          dist = ((x2-x1)**2.0 + (y2-y1)**2.0 + (z2-z1)**2.0 ) ** 0.5
          bin_idx = int( math.floor( float( dist ) / float( bin_size ) ) )
      #bin_idx = int( math.floor( bin_idx ) )
          #if c < 10:
          #  print bin_idx, dist
          #  c += 1
          bins[bin_idx] += 1
    self.D2_dist_list = bins
    self.D2_dist_list_pct = bins / len( self.verts.keys() )
    return bins
  def get_dist_distribution(self, max_dist, no_of_bin):
    bin_size = float( max_dist ) / float( no_of_bin )
    bins = numpy.zeros(no_of_bin+1)
    
    for dist in self.dists.values():
          bin_idx = int( math.floor( float( dist ) / float( bin_size ) ) )
      #bin_idx = int( math.floor( bin_idx ) )
          #if c < 10:
          #  print bin_idx, dist
          #  c += 1
          #print dist, bin_size, bin_idx, len( bins )
          bins[bin_idx] += 1
    self.dist_dist_list = bins
    self.dist_dist_list_pct = bins / len( self.verts.keys() )
    return bins

  def calculate_spherical_coordinate(self):
    for id in self.verts.keys():
      x,y,z = self.verts[id]
      r = ( x**2.0 +y**2.0+z**2.0 ) ** 0.5
      theta = math.acos( z / r )
      rho = math.atan2( y, x )
      self.verts_in_sphere[id] = [ r, theta, rho ]
      
  def get_spherical_distribution(self, max_r, r_div, theta_div, phi_div ):
    unit_r = max_r / r_div
    unit_theta = math.pi * 2 / theta_div
    unit_phi = math.pi * 2 / phi_div
    bins = numpy.zeros( ( r_div, theta_div, phi_div ))
    for id in self.verts_in_sphere.keys():
      r, theta, phi = self.verts_in_sphere[id]
      r_idx = int( math.floor( r / unit_r ) )
      theta_idx = int( math.floor( theta / unit_theta ) )
      phi_idx = int( math.floor( phi / unit_phi ) )
      bins[r_idx, theta_idx, phi_idx ] += 1
    self.sp_dist = bins
    self.sp_dist_pct = bins / len( self.verts_in_sphere.keys() )
    return bins

  def compute_distance( self, a_obj, keyword ):
    sum_sq_diff = 0
    if keyword == "SECSHELL":
      r,t,p = self.sp_dist.shape
      for i in range(r):
        for j in range(t):
          for k in range(p):
            diff = self.sp_dist_pct[i,j,k] - a_obj.sp_dist_pct[i,j,k]
            sum_sq_diff += diff ** 2
      euc_dist = ( sum_sq_diff ** 0.5 ) / r*t*p
      return euc_dist
    elif keyword == "D2":
      for i in range( len( self.D2_dist_list )):
        diff = self.D2_dist_list_pct[i] - a_obj.D2_dist_list_pct[i]
        sum_sq_diff += diff**2
      euc_dist = ( sum_sq_diff ** 0.5 ) / len( self.D2_dist_list )
      return euc_dist
    elif keyword == "SHELL":
      for i in range( len( self.dist_dist_list )):
        diff = self.dist_dist_list_pct[i] - a_obj.dist_dist_list_pct[i]
        sum_sq_diff += diff**2
      euc_dist = ( sum_sq_diff ** 0.5 ) / len( self.dist_dist_list )
      return euc_dist
    elif keyword == "VOXEL":
      x,y,z = self.voxels.shape
      for i in range(x):
        for j in range(y):
          for k in range(z):
            diff = self.voxels[i,j,k] - a_obj.voxels[i,j,k]
            sum_sq_diff += diff ** 2
      euc_dist = ( sum_sq_diff ** 0.5 ) / x*y*z
      return euc_dist      
