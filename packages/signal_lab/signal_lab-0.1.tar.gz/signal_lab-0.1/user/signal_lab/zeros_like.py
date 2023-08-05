
import signal_lab as slab
import sys

def zeros_like_map( inputs, env=None ):
    
    
    output = slab.File('out', env=env , input=inputs[0] )
    
    
    return [output]

def zeros_like( env, inputs, outputs ):
    
    output = outputs[0]
    
    output.binary_file.seek( (output.nbytes)-1 )
    output.binary_file.write('\x00')
    

if __name__ == '__main__':
    env = slab.Environment( sys.argv )
    
    input = slab.File( 'in', env=env ) 
    [output] = zeros_like_map( [input] )
    
    output.finalize( )
    
    zeros_like( env, [input], [output] )