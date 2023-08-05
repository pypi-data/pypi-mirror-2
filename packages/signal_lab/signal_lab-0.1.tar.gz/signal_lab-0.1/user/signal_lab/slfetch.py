
import signal_lab as slab
import sys
from urlparse import urlparse
import re

urlpat = re.compile('^(?:(.+)://)?(?:(.+)@)?(.+?)(?::(.*))?$')

def scp_fetch( scheme, username, hostname, remote_path, password, fetch_args ):
    """
    """
    pass

def ftp_fetch( scheme, username, hostname, remote_path, password, fetch_args ):
    """
    """
    pass

def sftp_fetch( scheme, username, hostname, remote_path, password, fetch_args ):
    """
    """
    pass

def wget_fetch( scheme, username, hostname, remote_path, password, fetch_args ):
    """
    """
    


def fetch( env ):
        
    input = slab.File( '$stdin', env=env , header_only=True )
    
    binary_in = input['in']
    scheme, username, hostname, remote_path = urlpat.findall( binary_in )[0]
     
    
    scheme = input.get( 'scheme' ,scheme )
    hostname = input.get( 'hostname',hostname )
    remote_path = input.get( 'remote_path', remote_path )
    username = input.get( 'username', username )
    password = input.get( 'password', None )
    
    
    if scheme in ['http','https','ftp']:
        fname = 'wget'
    else:
        fname = scheme
        
          
    remote_getter = globals().get('%s_fetch' %fname,None)
    
    
    if not remote_getter:
        print >>sys.stderr, "unkown scheme '%s'"%scheme
        print >>sys.stderr, "must be one of:"
        for item in globals().keys():
            if item.endswith( '_fetch' ):
                print >>sys.stderr, "   ", item[:-6]
                print >>sys.stderr,  globals()[item].__doc__
                
        raise Exception("unkown scheme %s"%scheme)
    
    fetch_args = input.get('fetch_args',[])
    print   
    print "scheme %r username %r hostname %r remote_path %r " %( scheme, username, hostname, remote_path)
    print "fetch_args",fetch_args
    print "password",password
    print
    
    remote_getter( scheme, username, hostname, remote_path, password, fetch_args )
    

if __name__ == '__main__':
    env = slab.Environment( sys.argv )
    
    fetch(env)
