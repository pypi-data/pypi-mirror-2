#!/usr/bin/env python
# encoding: utf-8

import signal_lab as slab  

import optparse
import sys
import os

def rm( env ):
    """
    remove rsf file and its binary 
    """
    
    
    
    


interactive_opt = optparse.Option( '-i',
                 dest='interactive',
                 default=None,
                 action='store_true',
help='''Request confirmation before attempting to remove each file, 
regardless of the file's permissions, or whether or not the
standard input device is a terminal.  The -i option overrides
any previous -f options.'''  
                )


no_interactive_opt = optparse.Option( '-f',
                 dest='interactive',
                 #default=False,
                 action='store_false',
help='''Attempt to remove the files without prompting for confirmation, 
regardless of the file's permissions.  If the file does
not exist, do not display a diagnostic message or modify the
exit status to reflect an error.  The -f option overrides any
previous -i options.'''
                )

if __name__ == '__main__':
    user_options=[interactive_opt,
                  no_interactive_opt]
    
    arg1 = slab.Parameter( 'x', float, 4.0, 'get parameter x' )
    arg2 = slab.Parameter( 'file', float, help='get parameter y' )
    rm_arguments = [ arg1,arg2 ]
    
    env = slab.Environment( sys.argv,
                            
                            #Arguments for command line help
                            user_options=user_options,user_arguments=rm_arguments,
                            use_stdin=True,use_stdout=True,
                            help=rm.__doc__ )
    
    rm(env)


