#!/usr/bin/env python
# encoding: utf-8
import sys
import signal_lab as slab
import numpy as np
#from  user.slab import stich as _c_stich 

def _c_stich( out_shape, out_file, files, starts, steps,stops,shapes, out_array, in_array ):
    
    print starts
    print steps
    print stops
    print shapes
    shape = list(out_shape)
    shape.reverse( )
    
    
    starts0 = starts[0]
    stops0  = stops[0]
    steps0  = steps[0]
    shapes0 = shapes[0]

    starts1 = starts[1:]
    stops1 = stops[1:]
    steps1 = steps[1:]
    shapes1 = shapes[1:]
    
    for idx in np.ndindex( *shape[:-1] ):
        idx = list(idx)
        idx.reverse(  )
        #print 'x', idx
        
        relevent_files = []
        for fidx,f in enumerate(files):
            use_file = True
            
            for j in range( len( shape[:-1] ) ):
                jdx = idx[j]
                fstart = starts1[j][fidx]
                fstep = steps1[j][fidx]
                fstop = stops1[j][fidx]
                use_file = use_file and  ( jdx >= fstart) and (jdx < fstop) and ( (jdx-fstart)%fstep )==0
            if use_file:
                size = shapes0[fidx]
                relevent_files.append( (f,starts0[fidx],stops0[fidx],steps0[fidx],size) )
                
#            for j,(jdx,start,stop,step) in enumerate(zip( idx, starts1,stops1, steps1 )):
#                if (jdx >= fstart) and (jdx < fstop) and ( (jdx-fstart)%fstep )==0:
#                    size = shapes0[j]
#                    print  (f,size)
        
        for f,start,stop,step,size in  relevent_files:
            nr = f.readinto( in_array[:size].data )
            if nr != len(in_array[:size].data):
                raise Exception( )
            out_array[start:stop:step] = in_array[:size]
            
        #import pdb; pdb.set_trace()
        
        
        out_file.write( out_array.data )
        

allsame = lambda iterable: all( [ x==iterable[0] for x in iterable] )
def stich( env ):
    
    files = [slab.File(arg ) for arg in env.args]
    
    dims = [ f.ndim for f in files]
    
    
    if not allsame( dims ):
        print >> sys.stderr, 'number of dimensions in each file must be the same'
        for f in files: 
            print >> sys.stderr, '  %s (ndim == %i)' %(f.header,f.ndim)
        
        raise Exception( 'number of dimensions in each file must be the same' )
    
    
    ndim = dims[0]
    origins = [ f.origin for f in files ]
    steps   = [ f.step   for f in files ]
    
    shapes  = [ f.shape  for f in files ]
    
    zorig = zip(  *origins )
    zstep = zip(  *steps )
    zshape = zip( *shapes )
    
    
    
    output_origin = [  ]
    output_step   = [  ]
    output_shape  = [  ]
    
    xstart = [ ]
    xstop =  [ ]
    xstep =  [ ]
    
    for i in range(ndim):
        
        finishes = [ o+((n-1)*d) for o,n,d in zip(zorig[i],zshape[i],zstep[i]) ]
        
        assert allsame( zstep[i] ),'step in dimension %i must be the same for all arrays' %(i+1)
        d = float(zstep[i][0])
        
        if d < 0:
            o = max( zorig[i] )
            f  = min( finishes )
        else:
            o = min( zorig[i] )
            f  = max( finishes )
        
        o = float(o)
        f = float(f)
        
        for oi in zorig[i]:
            x = (o-oi)
            if not x:
                continue
            
            d1 = abs( d/ (o-oi) )
            next = d1
            gran = 1  
            while next%1:
                gran+=1
                next = d1*gran
            
            if next>1.0:
                print 'expanding dimention',i,'by', next,'times'
                d = d / next
             
            
        
        #finest_step = [ abs((o-oi)/d) for oi in zorig[i] ] 
        #print 'finest_step',i, finest_step
        #finest_step = max(finest_step) 
        #finest_step = [ ff and abs(1/ff) or 0. for ff in finest_step]
        
        #print 'finest_step',i, finest_step
        output_step.append( d )
        
        output_origin.append( o )

        n = int( (f-o)/d )+1
        
        output_shape.append( n )
        
        xstart.append( [ (oi-o) and int((oi-o)/d) or 0 for oi in zorig[i] ] )
        xstep.append( [ int(di/d) for di in zstep[i] ] )
        xstop.append( [ 1+o+d*(n-1) for o,d,n in zip(xstart[i],xstep[i],zshape[i]) ] )

    output = slab.File( 'out', env=env, input=files[0] )
    
    output.shape = output_shape
    output.step = output_step
    output.origin = output_origin
    
    output.finalize( )
    
    out_array = np.zeros( output.shape[0], dtype=output.dtype, order=output.order )
    
    in_array  = np.zeros( output.shape[0], dtype=output.dtype, order=output.order )
    
    _c_stich( output_shape, output.binary_file, [ f.binary_file for f in files ], 
              xstart, xstep, xstop, zshape,
              out_array,in_array)
    return 
    
    
if __name__ == '__main__':
    
    env = slab.Environment( sys.argv, help=stich.__doc__ )
    
    stich(env)

