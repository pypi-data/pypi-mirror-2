import sys
import os
import socket
from subprocess import Popen, PIPE

hostname = socket.gethostname( )

from sys import argv as _argv , stderr


def genname( xop, rank ):
#    env = xop.slfile.env
#    env = slab.Environment()
#    datapath = env.options['datapath']
    datapath ='.'
    pid = os.getpid( )
    xop.set_value( rank, 'filename', "%(datapath)s/dist.%(pid)s.%(rank)s.rsf" %vars() )
#    import pdb;pdb.set_trace()


def Distribute( xinputs, xoutputs, cmd , verb=True, 
                nostdin=False, nostdout=False, fifoout=False):
#    if verb: print >> stderr,  "Distribute, fifoout", fifoout 
    sizes = [ ip.slfile.shape[0] for ip in xinputs ]
    size = sizes[0] 
    sizes_eq = [ s==size for s in sizes ]
    if not all( sizes_eq ):
        raise Exception( "size of meta files must be equal: got sizes %s" %(sizes) )


    procs = []
    for rank in range(size):
        for xop in xoutputs:
            genname(xop,rank)
            
        rank_nodes = [ xip.get_value( rank, 'nodename' ) for xip in xinputs ]
        nodename = rank_nodes[0] 

        if nodename in ['localhost',hostname]:
            ssh_cmd = lambda x: x
        else:
            ssh_cmd = lambda x: "ssh %s '%s'" %(nodename,x) 

        nodes_eq = [ node==nodename for node in rank_nodes ]
        if not all( nodes_eq ):
            raise Exception( "nodename of each subheader on a rank must be the same" %(sizes) )
        
        rank_cmd = cmd
        for xip in xinputs:
            old = xip.slfile.header_name
            new = xip.get_value( rank, 'filename' )
            if old == "stdin" and not nostdin:
                rank_cmd = "< %s %s" %(new,rank_cmd)
            else:
                
                rank_cmd = rank_cmd.replace( old,new )

        for xop in xoutputs:
            old = xop.slfile.header_name
            new = xop.get_value( rank, 'filename' )
            if old == "stdout" and not nostdout:
                if fifoout:
                    fifocmd = ssh_cmd("mkfifo %s"%(new)) 
                    if verb: print >> stderr, fifocmd
                    pF = Popen( fifocmd, shell=True )
                    pF.wait( )
                    
                rank_cmd = "%s > %s" %(rank_cmd,new)
            else:
                nostdout = True
                rank_cmd = rank_cmd.replace( old,new )
        
        command = ssh_cmd(rank_cmd)
#        if nodename in ['localhost',hostname]:
#            pass
#        else:
#            rank_cmd = "ssh %s '%s'" %(nodename,rank_cmd) 
        if verb: print >> stderr, command
        
        p0 = Popen( command, shell=True )
        procs.append( p0 )
    
    err=0
    
#    for p0 in procs:
#        err -= abs(p0.wait( ))
    
    if err:
        raise Exception( "an error occured within a subprocess")
    
    return 


def Remove( xinput , verb, f ):
    header_name = xinput.slfile.header_name
    binary_name = xinput.slfile.binary_name
    
    try:
        Distribute( [xinput], [], "sfrm %s" %(header_name), verb )
    except Exception,e:
        if not f: raise
        if verb: print e

    try:
        os.remove(binary_name)
#        print "remove" , sfile[ 'in' ]
    except Exception,e :
        if not f: raise
        if verb: print e
    try:
        os.remove(header_name)
#        print "remove" , fname
    except Exception,e:
        if not f: raise
        if verb: print e


