
import signal_lab as slab
import sys



def zeros( env, fin ):
    if fin.packed:
        whence = 1
    else:
        whence = 0
        
    
    fin.binary_file.seek( fin.nbytes-1, whence )
    fin.binary_file.write('\x00')
        

if __name__ == '__main__':
    
    env = slab.Environment( sys.argv )
    env.options['header_in_mode'] = 'r+'
    env.options['binary_in_mode'] = 'w'
     
    for sfile in env.args:
        
        filein = slab.File( sfile, env=env )
        zeros( env, filein )
        filein.close( )

