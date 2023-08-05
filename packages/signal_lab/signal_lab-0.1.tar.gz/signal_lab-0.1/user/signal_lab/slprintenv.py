#!/usr/bin/env python
# encoding: utf-8
"""
Print the current environment options that signal_lab 
detects at runtime 
"""

import signal_lab as slab
import sys

def printenv( env ):
    
    print"="*40 
    print"   SIGNAL LAB ENVIRONMENT VARIABLES" 
    print"="*40 
    for key,val in env.options.items( ):
        print >> sys.stderr, "%-17s=%r" %(key,val)

    print"="*40 
    print"="*40 

if __name__ == '__main__':
    
    env = slab.Environment( sys.argv, help=__doc__ )
    
    printenv(env)

