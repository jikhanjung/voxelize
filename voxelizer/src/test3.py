'''
Created on 2012. 11. 21.

@author: jikhanjung
'''

G_NAME = "test"
i = 1
G_Z = 2 
print "%02d" % tuple([i]) 
G_MSG = "e:/stack/" + G_NAME + "-" + "%02d" % tuple([i]) + "_" + \
"%03d" % tuple([G_Z]) + ".png"
print G_MSG, "abc"