#!/usr/bin/env python
# encoding: utf-8
import time

import wx
import signal_lab as slab
import sys
import numpy as np


def progress( env ):
    
    app = wx.PySimpleApp( ) #@UnusedVariable
    
    inpt = slab.File( '$stdin' ,env=env )
    outpt = slab.File( '$stdout' ,env=env ,input=inpt )
    
    
    
    buffer_size = env.options['buffer_size']
    
    if buffer_size is None:
        buffer_size = buffer_size = inpt.shape[0]*inpt.esize
    
    buffer_size = int(buffer_size)
    
    print >>sys.stderr, buffer_size
    print >>sys.stderr, inpt.nbytes
    
    array = np.zeros( [buffer_size], dtype=np.int8 ) #@UndefinedVariable

    ibin = inpt.binary_file
    outpt.finalize()
    obin = outpt.binary_file
    
    
    dialog = wx.ProgressDialog( "RSF Progress (%s)"%env.kw.get('name') , "%5.2f" %0)
    wrote = 1
    total = inpt.size/(buffer_size/inpt.esize)
    
    nr = ibin.readinto( array )
    
    
    if not total:
        total = 1
        
    while nr:
        
        obin.write( array[:nr] )
        
            
        perc = 100.0* wrote/ float(total)
        if perc<0:perc=0. 
        elif perc>100:perc=100. 
         
        dialog.Update( int(perc), "%5.2f buffer %i of %i" %(perc,wrote,total))
        #time.sleep(0.2)
        nr = ibin.readinto( array )
        wrote += 1

    inpt.close( )
    outpt.close( )
    
    dialog.Close( )
    
    return


if __name__ == '__main__':
    
    env = slab.Environment( sys.argv )
    
    progress(env)
    