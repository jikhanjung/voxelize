'''
Created on 2012. 9. 6.

@author: jikhanjung
'''
from numpy import *
import numpy
import math 

class MdDatamatrix:
  def __init__(self):
    pass
  def SetMatrix(self,matrix):
    self.matrix = matrix
    self.nVariable, self.nObservation = matrix.shape
  def AddDataset(self,dataset):
    self.dataset = dataset
    self.dimension = dataset.dimension
    self.nObservation = len( dataset.objects )
    self.nVariable = len( dataset.objects[0].landmarks ) * self.dimension
    self.matrix = numpy.zeros( ( self.nVariable, self.nObservation ) )
    i = 0
    #for object in dataset.objects:
    for object in dataset.objects:
      j = 0
      #for lm in object.landmarks:
      
      for lm in object.landmarks:
        #print lm.xcoord, lm.ycoord, lm.zcoord
        self.matrix[j,i] = lm.xcoord
        j += 1
        self.matrix[j,i] = lm.ycoord
        j += 1
        if self.dimension == 3:
          self.matrix[j,i] = lm.zcoord
          j += 1
        if j == self.nVariable:
          break
      i += 1

class MdPrincipalComponent:
  def __init__(self):
    self.dimension = -1
    self.data = MdDatamatrix()
    #self.datamatrix = []
    return
  def AddDataset(self,dataset):
    self.data.AddDataset( dataset )
  def SetMatrix(self, matrix):
    self.data.SetMatrix( matrix )

  def Analyze(self):
    '''analyze'''
    #print "analyze"
    self.raw_eigen_values = []
    self.eigen_value_percentages = []
        
    #for d in self.datamatrix :
      #print d

    sums = []
    avrs = []
    ''' calculate the empirical mean '''
    for i in range ( self.data.nVariable ): 
      sums.append(  0 )
      for j in range ( self.data.nObservation ):
        sums[i] += self.data.matrix[i,j] 
    
    for sum in sums:
      avrs.append( float( sum ) / float( self.data.nObservation ) )
    
    #print "sum:", sums
    #print "avgs:",avrs
    #return
    
    for i in range ( self.data.nVariable ): 
      for j in range ( self.data.nObservation ):
        self.data.matrix[i,j] -= avrs[i] 

    #print self.datamatrix
    
    ''' covariance matrix '''
    self.covariance_matrix = numpy.dot( self.data.matrix, numpy.transpose(self.data.matrix)) / self.data.nObservation

    #print "covariance_matrix", self.covariance_matrix
  
    ''' zz '''
    v, s, w = numpy.linalg.svd( self.covariance_matrix )
    #print "v", v
    #print "w", w
    
    #print "s[",
    self.raw_eigen_values = s
    sum = 0
    for ss in s:
      sum += ss
    for ss in s:
      self.eigen_value_percentages.append( ss/sum )
    cumul = 0
    eigen_values = []
    i = 0
    nSignificantEigenValue = -1
    nEigenValues = -1
    for ss in s:
      cumul += ss
      eigen_values.append( ss )
      #print sum, cumul, ss
      if cumul / sum > 0.95 and nSignificantEigenValue == -1:
        nSignificantEigenValue = i + 1
      if (ss /sum ) < 0.00001 and nEigenValues == -1:
        nEigenValues = i + 1
      i += 1
    
    #print nEigenValues, "eigen values obtained,", nSignificantEigenValue, "significant."
    #print eigen_values
    
    #for i in range( len(s) ):
      #print math.floor( ( s[i] / sum ) * 10000 + 0.5 ) / 100

    #print "s", int( s * 100 )/100
    #print "w", w
    #print v
    
    #print self.data.matrix
    for i in range(nSignificantEigenValue):
      k = v[...,i]
      #print i, k, numpy.transpose(k) 
      det = numpy.dot( k, numpy.transpose( k ))
      #print det
    self.rotated_matrix = numpy.dot( w, self.data.matrix )
    self.rotation_matrix = w
    #print w
    #print self.datamatrix[...,2]
    #print self.rotated_matrix[...,2]
    #print self.rotated_matrix
    self.loading = w
    return
    self.new_dataset = self.data.dataset.copy()
    self.new_dataset.objects = []
    for i in range( self.data.nObservation ):
      #object = MdObject()
      object.objname = self.data.dataset.objects[i].objname
      object.coords = self.rotated_matrix[...,i]
      object.group_list[:] = self.data.dataset.objects[i].group_list[:]
      self.new_dataset.objects.append( object )
      #if( i == 2 ) : print object.coords
