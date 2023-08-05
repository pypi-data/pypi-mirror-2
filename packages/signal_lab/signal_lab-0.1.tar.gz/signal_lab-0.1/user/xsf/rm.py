#!/usr/bin/env python
# encoding: utf-8
#  Copyright (C) 2008 The University of British Columbia
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from esf import Remove
import socket
import slab
import slabxml
from subprocess import Popen
import os
"""
remove eslab file header and data 
"""

#hostname = socket.gethostname()

#def Remove( env, fname, f, verb ):
#    
#    if verb: print "removing xsf file:",fname
#    try:
#        sfile = slab.sl_file( fname, env=env )
#        xfile = slabxml.eslfile( sfile )
#    except Exception, e:
#        if not f: raise
#        if verb: print e
#        return
#    procs = []
#    for i in range( sfile.size ):
#        subname = xfile.get_value( i, 'filename' ,'' )
#        nodename = xfile.get_value( i, 'nodename' ,'' )
#        if verb: print "  - removing rsf sub file: %s:%s" %(nodename,subname) 
#        if nodename in ['localhost',hostname]:
#            command = "sfrm %(subname)s " %vars()
#        else:
#            command = "ssh %(nodename)s sfrm %(subname)s " %vars()
#        p0 = Popen( command, shell=True )
##        print command  
##        err = p0.wait()
#        procs.append((p0,command))
#        
#    for p0,command in procs:
#        err = p0.wait()
#        if err and not f: raise IOError( err,"command '%s' failed" %(command) ) 
#        
#    try:
#        os.remove(sfile[ 'in' ])
##        print "remove" , sfile[ 'in' ]
#    except Exception,e :
#        if not f: raise
#        if verb: print e
#    try:
#        os.remove(fname)
##        print "remove" , fname
#    except Exception,e:
#        if not f: raise
#        if verb: print e



def main( ):
    
    env = slab.Environment(  )
    
    args = list(env.args)
    
#    import pdb;pdb.set_trace()
    local_opts = set()
    
    for arg in list(args):
        if arg.startswith( '-' ):
            local_opts.update( arg[1:] )
            args.remove( arg )
        else:
            break
        
    verb = 'v' in local_opts
    f = 'e' in local_opts
    
    if verb: print
    for fname in args:
        if verb: print "removing xsf file:",fname
        try:
            sfile = slab.sl_file( fname, env=env )
            xfile = slabxml.eslfile( sfile )
        except Exception, e:
            if not f: raise
            if verb: print e
            return

        Remove( xfile, f, verb )
        


if __name__ == '__main__':
    main( )