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
from esf import genname

"""

"""

import slab #@UnresolvedImport
import slabxml #@UnresolvedImport
from esf import Distribute

from sys import argv as _argv , stderr
from subprocess import Popen
    
def main( ):
    try:
        idx = _argv.index( '-c' )
    except ValueError:
        raise Exception( "need option -c cmd" )
        
    #===============================================================================
    # Get command and parse args
    #===============================================================================
    command = _argv[idx+1:]
    args = _argv[:idx]
    
    
#    env = slab.Environment( )
    
    argv  = list( args )
    
    sips = []
    sops = []
    rms  = []
    fifo = False
    fifoin = False
    
    for i,arg in enumerate(argv):
        print "arg", arg
        if arg.startswith('-'):
            if 'i' in arg:
                sips.append( argv[i+1] )
                if 'r' in arg:
                    rms.append( argv[i+1] )
                if (argv[i+1] == 'in') and 'f' in arg:
                    fifoin = True
                
            elif 'o' in arg:
                
                sops.append( argv[i+1] )
#                print >> stderr, "'f' in arg", 'f' in arg
                if ( argv[i+1] == 'out' ) and 'f' in arg  :
                    fifo = True
    
    print >> stderr, "command", command
    print >> stderr, "fifo", fifo 
    print >> stderr, "inputs",  sips
    print >> stderr, "outputs", sops
    
    inputs = []
    xinputs = []
    for  input in sips:
#        ip = slab.sl_file( input , env=env )
        ip = slab.sl_file( input )
        xip = slabxml.eslfile( ip )
        inputs.append( ip )
        xinputs.append( xip )
    
    if inputs:
        stdinput = inputs[0]
        stdxinput = xinputs[0]
    else:
        stdinput=False
        stdxinput = False
    
    outputs = []
    xoutputs = []

#    import pdb;pdb.set_trace()
#    import pdb; pdb.set_trace( )
    for output in sops:
        if stdinput:
#            op = slab.sl_file( output, input=stdinput, env=env )
            op = slab.sl_file( output, input=stdinput )
            xop = slabxml.eslfile( op, stdxinput )
        else:
            print >> stderr, "input=False"
#            op = slab.sl_file( output, input=False, env=env )
            op = slab.sl_file( output, input=False)
            xop = slabxml.eslfile( op )
        
        outputs.append( op )
        xoutputs.append( xop )
        
    cmd = " ".join(command)
    
    #===============================================================================
    # For each Rank
    #===============================================================================
    
#    if fifo:
    for xop in xoutputs:
#        for xop in xoutputs:
        for rank in range(xop.slfile.shape[0]):
            genname(xop,rank)

        xop.finalize( )
#        xop.slfile.close( )
    
        
    Distribute( xinputs, xoutputs, cmd, fifoout=fifo )
    
#    if not fifo:
#        for xop in xoutputs:
#            xop.finalize( )

    if 'in' in rms:
        rms[rms.index('in')] = 'stdin'
    
    for xip in xinputs:
        name = xip.slfile.header_name
        if name in rms:
            if name == 'stdin' and fifoin:
                Distribute( [xip], [] , "rm %s" %xip.slfile.header_name, nostdin=True  )
            else:
                Distribute( [xip], [] , "sfrm %s" %xip.slfile.header_name, nostdin=True  )
        

    
        
    print >> stderr, "xsfdist: done "
    return 


if __name__ == '__main__':
    main( )
    

