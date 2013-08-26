'''
Created on 2012. 10. 1.

@author: jikhanjung
'''

import wx
import os
import math

def AutoCropWhiteSpace( InputImage ):
    nHeight = InputImage.GetHeight()
    nWidth=InputImage.GetWidth()
    nR=InputImage.GetRed(0,0)
    nG=InputImage.GetGreen(0,0)
    nB=InputImage.GetBlue(0,0)
    nCloseness=15
    found = False
    ClipRect = wx.Rect();
    ''' Calculate top clip '''
    max_y = 0
    min_y = nHeight
    max_x = 0
    min_x = nWidth
    InputImage.InitAlpha()
    for y in range( nHeight ):
        for x in range( nWidth ):
            if math.fabs( InputImage.GetRed(x,y) - nR ) > nCloseness or math.fabs(InputImage.GetGreen(x,y)-nG)>nCloseness or math.fabs(InputImage.GetBlue(x,y)-nB)>nCloseness :
                max_y = max( y-1, max_y)
                min_y = min( y+1, min_y)
                max_x = max( x-1, max_x)
                min_x = min( x+1, min_x)
            else:
                InputImage.SetAlpha( x, y, 0 )
    ClipRect.y = min_y
    ClipRect.height = max_y - min_y + 1
    ClipRect.x = min_x
    ClipRect.width = max_x - min_x + 1
    return InputImage.GetSubImage( ClipRect )
    
    for y in range( nHeight ):
        for x in range( nWidth ):
            if math.fabs( InputImage.GetRed(x,y) - nR ) > nCloseness or math.fabs(InputImage.GetGreen(x,y)-nG)>nCloseness or math.fabs(InputImage.GetBlue(x,y)-nB)>nCloseness :
                ClipRect.y= max(y-1,0,ClipRect.y)
                found = True
                break
        if found: break

    found = False
    ''' Calculate bottom clip '''
    for y in range( nHeight-1, -1, -1 ):
        for x in range( nWidth ):
            if math.fabs(InputImage.GetRed(x,y)-nR)>nCloseness or math.fabs(InputImage.GetGreen(x,y)-nG)>nCloseness or math.fabs(InputImage.GetBlue(x,y)-nB)>nCloseness :
                ClipRect.height= min( y+1,nHeight)-ClipRect.y;
                found = True
                break
        if found: break
    
    found = False
    ''' Calculate left clip '''
    for x in range( nWidth ):
        for y in range( ClipRect.y, nHeight ):
            if math.fabs(InputImage.GetRed(x,y)-nR)>nCloseness or math.fabs(InputImage.GetGreen(x,y)-nG)>nCloseness or math.fabs(InputImage.GetBlue(x,y)-nB)>nCloseness:
                ClipRect.x=max(x-1,0)
                found = True
                break
        if found: break

    found = False
    ''' Calculate right clip '''
    for x in range( nWidth-1,-1,-1 ):
        for y in range( ClipRect.y, nHeight ):
            if math.fabs(InputImage.GetRed(x,y)-nR)>nCloseness or math.fabs(InputImage.GetGreen(x,y)-nG)>nCloseness or math.fabs(InputImage.GetBlue(x,y)-nB)>nCloseness :
                ClipRect.width= min(x+1,nWidth)-ClipRect.x
                found = True
                break
        if found: break
        
    return InputImage.GetSubImage(ClipRect)

dir = "D:/images_crop/"
dir2 = "D:/images_crop4/"
files = os.listdir( dir )
for fn in files:
    ( name, ext ) = os.path.splitext( fn )
    if ext != ".png": continue
    print fn
    img = wx.Image( dir + fn )
    new_img = AutoCropWhiteSpace( img ) 
    new_img.SaveFile( dir2 + fn, wx.BITMAP_TYPE_PNG )
