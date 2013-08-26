'''
Created on 2012. 3. 4.

@author: jikhanjung
'''
X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2
import numpy
import math

def rotate_on_axis(angle,axis, point):
  if axis == X_AXIS:
      idx1 = 1
      idx2 = 2
  elif axis == Y_AXIS:
      idx1 = 0
      idx2 = 2
  elif axis == Z_AXIS:
      idx1 = 0
      idx2 = 1
  print math.degrees(angle)
  rotate = numpy.zeros( (3,3) )
  for i in range(3):
      rotate[i,i] = 1
  rotate[idx1,idx1] = rotate[idx2,idx2] = math.cos( angle )
  rotate[idx2,idx1] = math.sin( angle )
  rotate[idx1,idx2] = -1.0 * math.sin( angle )
  print rotate
  print "hello"
  #self.rotated_verts = {}

  ''' rotate point of origin as well''' 
  vec = numpy.zeros( ( 3 ) )
  vec[:] = point[:]
  rotated_vec = numpy.dot( rotate, vec )
  point = rotated_vec[:]
  return point
def align_to_minus_zaxis(point):
    print point
    x, y, z = point
    sin_val = y / math.sqrt( x*x + y*y )
    angle = math.degrees( math.asin(sin_val) )
    if x < 0: angle = 180 - angle
    rotate_angle = 90 - angle
    print rotate_angle
    rotate_angle_radian = math.radians( rotate_angle )
    
    point = rotate_on_axis( rotate_angle_radian, Z_AXIS,point )
    print point

    x, y, z = point
    sin_val = z / math.sqrt( y*y + z*z )
    angle = math.degrees( math.asin(sin_val ))
    if y < 0: angle = 180 - angle
    rotate_angle = ( 90 - angle ) + 180 
    print rotate_angle
    rotate_angle_radian = math.radians( rotate_angle )
    point = rotate_on_axis( rotate_angle_radian, X_AXIS,point ) 
    print point
    return

def align_using_point_of_origin( x, y, z ):
      sin_val = y / math.sqrt( x*x + y*y )
      #print sin_val
      angle = math.degrees( math.asin(sin_val) )
      if x < 0: angle = 180 - angle
      rotate_angle = 90 - angle
      rotate_angle_radian = math.radians( rotate_angle )
      return rotate_angle
point = [ 1, 1, 0 ]
align_to_minus_zaxis( point)
  
import sys  

sys.exit()
angle = align_using_point_of_origin( 1, 2, 1 )

print angle

angle = align_using_point_of_origin( -1, 2, 1 )

print angle

angle = align_using_point_of_origin( -1, -2, 1 )

print angle

angle = align_using_point_of_origin( 1, -2, 1 )

print angle
    