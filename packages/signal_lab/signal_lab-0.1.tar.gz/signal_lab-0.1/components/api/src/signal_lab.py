"""
Use %prog -h for help about user defined arguments.
"""

__synopsis__ = "Signal and image processing utilities for the RSF file format"
__author__ = 'Sean Ross-Ross <srossross@geospining.com>'

import optparse

import os
import sys
import numpy as np
import subprocess
import stat
import warnings
import cPickle
import string
from time import ctime, time
import xml.dom.minidom as minidom

import c_signal_lab as cSlab #@UnresolvedImport
from numpy import little_endian #@UnresolvedImport

warnings.simplefilter('ignore', RuntimeWarning )

dp       = os.environ.get( 'DATAPATH','.' )
dplog       = os.environ.get( 'DATAPATHLOGFILE', True )

opt_datapath = optparse.Option( '--datapath',
                                default=dp, # default value
                                help="path to put binary data to" )

opt_dryrun = optparse.Option( '-n','--dryrun',
                                default=False, # default value.
                                action='store_true',
                                help="do not output data, only headers" )

pack_opt = optparse.Option( '-p','--pack',
                             
                            default=False,
                            
                            action='store_true',
                            help="pack header with binary data" )

accept_tty_opt = optparse.Option( '--accept-tty',
                              dest ='accept_tty',
                             default=False,
                             action='store_true',
                             help="accept a tty device from stdin/out" )

stdinopt = optparse.Option( '--stdin',
                            default="file:sys.stdin",
                            help='redirect input of stdin to file' 
                            )

stdoutopt = optparse.Option( '--stdout',
                            default="file:sys.stdout",
                            help='redirect output of stdout to file' 
                            )

fifoopt = optparse.Option( '--fifo',
                             default=False,
                             action='store_true',
                             help="create and output to a fifo device" )

# defines the ratio of bytes to kilobytes
bmap = {'B':1,'KB':2**10,'MB':2**20,'GB':2**30}
def btype( option, opt, value ):
 
    if value.isdigit( ):
        val = value
        vtype = 'b'
        
    elif value[-2:].isalpha( ):
        val = value[:-2]
        vtype = value[-2:]
    elif value[-1:].isalpha( ):
        val = value[:-1]
        vtype = value[-1:]
    
    nbytes = int(val) * bmap[vtype.upper()]
    
#    if value.endswith( 'b' ):
#        value = int( value[:-1] )
#    elif value.endswith( 'b' )
    print >> sys.stderr, "nbtypes", nbytes 
    return nbytes   

from copy import copy
 
class ByteSizeOption(optparse.Option):
    TYPES = optparse.Option.TYPES + ("bytes",)
    TYPE_CHECKER = copy(optparse.Option.TYPE_CHECKER)
    TYPE_CHECKER["bytes"] = btype
      
buffer_sizeopt = ByteSizeOption( '-b', "--buffer-size",
                                  default=None,
                                  type='bytes',
                                  help='buffer size for reading chunks of data',
                                  )

local_bin = optparse.Option( '-l', "--local-binary",
                                 dest='local_binary',
                                 default=False,
                                 action='store_true',
                                  help='look up local binary files'
                                  )

orderF = optparse.Option( "--order-fortran",
                          action='store_const',
                          const='F',
                          default='F',
                          dest='order',
                          help='process in Fortran ordering'
                                  )
orderC = optparse.Option( "--order-C",
                          action='store_const',
                          const='C',
                          default='F',
                          dest='order',
                          help='process in C ordering'
                                  )

replace_bin = optparse.Option( '-o',"--overwrite-binaries",
                          action='store_true',
                          default=True,
                          dest='replace_binaries',
                          help='overwrite rsf binary file if it already exists'
                                  )

no_replace_bin = optparse.Option( '-k',"--no-overwrite-binaries",
                          action='store_false',
                          dest='replace_binaries',
                          help=('keep binary file if it already exists,\n'
                                'create a new temporary file instead\n'
                                'if the file "file.rsf@" exists, slab will create the \n'
                                'file file1.rsf@' )
                               )

verbose = optparse.Option( '-v',"--verbose",
                          action='store_true',
                          default=False,
                          dest='verbose',
                          help=( 'print verbose diagnostic of internal commands' )
                                  )

datapath_logfile = optparse.Option( "--datapath-log",
                                    #action='store_true',
                                    default=dplog,
                                    dest='datapath_log',
                                    help=( 'data path log file name' )
                                  )

no_datapath_logfile = optparse.Option( "--no-datapath-log",
                                       action='store_false',
                                       dest='datapath_log',
                                       help=( "don't use data path logfile" )
                                       )

permissive = optparse.Option( "--permissive",
                                       action='store_true',
                                       default=False,
                                       dest='permissive',
                                       help=( "SLAB will try its best to avoid throwing exceptions" )
                                       )

werror = optparse.Option( "--werror",
                                       action='store_true',
                                       default=False,
                                       help=( "SLAB will raise exceptions instead of warnings" )
                                       )

slab_options = [opt_datapath,opt_dryrun,pack_opt,accept_tty_opt,stdinopt,stdoutopt,
                fifoopt,buffer_sizeopt,local_bin,orderF,orderC,
                verbose,replace_bin,no_replace_bin,
                datapath_logfile,no_datapath_logfile,
                permissive,werror
                ]

def values_to_dict( values ):
    
    d1 = set(dir(values))
    d2 = set(dir(optparse.Values()))
    
    res = {}
    for key in d1.difference(d2):
        
        res[key] = getattr(values, key)
        
    return res
        
        
class error(Exception):pass

class NoDefault( object ):pass

class Parameter( object ):
    def __init__( self, name, type=str, default=NoDefault, help=None ):
        self.name = name
        if isinstance(type, tuple ): 
            self.type = type[0]
            self.type_name = type[1]
        elif isinstance(type,str):
            self.type = type
            self.type_name = type
        else:
            self.type = type
            self.type_name = getattr(type, '__name__', str(type) )
              
        self.default = default
        self.help = help
        
    def get_default(self):
        if self.default is NoDefault:
            
            
            if self.type_name in [ 'rsf input','rsf output' ]:
                return self.name.upper( ) + ".rsf"
            else:
                return self.name.upper( )
        else:
            return self.default
    
    
class Environment( object ):
    """
    This is an environment. a signal_lab.Environment object is designed to store arguments and 
    options for  signal_lab programs and other objects
    """
    @classmethod
    def option_help(cls,option, opt, value, parser):
        """
        Print the optparse standard help message and exit
        """
        print parser.format_help( )
        raise SystemExit

    def user_help(self, option, opt, value, parser ):
        '''
        print help for main program
        '''
        prog = os.path.basename(self.prog)
        print 'Name:' 
        print
        print '   ',prog
        print
        if self.help:
            print 'Description:'
            print
            print "\n".join( [ "    " + line.strip() for line in self.help.splitlines() if line.strip()] )
            print
        
        print 'Synopsis:'
        print
        print '   ', prog,
        if self.use_stdin:
            print "< in.rsf",
        
        print " ".join( [ str(i) for i in self.inputs  ] ),
        print " ".join( [ "%s=%s" %( arg.name, arg.get_default() ) for arg in self.user_arguments] ),
        
        for opt in self.user_options:
            if opt.action == 'store':
                key = opt.get_opt_string( )
                
                if opt.default != ('NO', 'DEFAULT'):
                    
                    value = opt.default
                else:
                    value = str(opt.dest).upper()
                if opt._long_opts:
                    print "%s=%s" %(key,value),
                else:
                    print "%s %s" %(key,value),
            
            else:
                print opt.get_opt_string(),
         
        if self.use_stdout:
            print "> out.rsf"
        else:
            print 
        
        
        if self.user_arguments:
            
            user_arguments = [ ( par.type_name, par.name, par.help ) for par in self.user_arguments ]
            max_type_name_size = max([ len(p) for (p,_,_) in user_arguments]) 
            max_name_size = max([ len(p) for (_,p,_) in user_arguments])
            
            spacer = '\n    %%-%is | %%-%is | ' %(max_type_name_size,max_name_size) %('','')
            
            #spacer = "\n"+" "*(max_type_name_size+max_name_size+10)
            def format_help( text):
                if not text:
                    return "No Documentation"
                if len(text.splitlines( )) ==1:
                    return text
                
                text = " ".join( text.splitlines( ) ).split()
                
                new_text = []
                last_line = []
                linelen = 0
                numlines = 0
                while text:
                    
                    word = text.pop(0)
                    
                    if linelen+len(word) > 60:
                        new_text.append(" ".join(last_line))
                        last_line=[ ]
                        linelen=0
                        
                    linelen += len(word)+1
                    
                    last_line.append(word)
                    numlines+=1
                    
                if numlines>1:
                    new_text.append("")
                       
                return spacer.join(new_text)
                     
            
            user_arguments = [ ( type_name, name, format_help(help) ) for ( type_name, name, help ) in user_arguments ]
            
            string_form_a = '    %%-%is | %%-%is | %%s' %(max_type_name_size,max_name_size)
            string_form_b = '    %%-%is + %%-%is + %%s' %(max_type_name_size,max_name_size)
            print
            print 'Parameters:'
            print 
            print string_form_a% ( 'type','name' ,'help' )
            print string_form_b% ( '-'*max_type_name_size,'-'*max_name_size ,'-'*60 )
            
            
            for par in user_arguments:
                
                print string_form_a % par
        print
        print 'Use "%s -H" for help about command-line options' %prog
        print
        raise SystemExit
        
        
    @classmethod
    def user_manpage(cls,option, opt, value, parser):
        print "User Man"
        
    
    def __init__( self, args , help=None, inputs=None, user_arguments=None, user_options=None, use_stdin=False,use_stdout=False, **options ):
        '''
        *args*: list of string arguments
        
        *help*: help text to print when '-h' option is in *args*
        
        *inputs*: list of input names for help
        
        *user_arguments*: list of *signal_lab.Parameter* objects
        
        *user_options*: list of optparse.Option instances
        
        *use_stdin*: for help output  
        *use_stdout*: for help output
        
        *options*: overwrite options from *args*
        
        '''
        
        if not args:
            args = [ os.path.basename(sys.argv[0]) ]
        
        self.prog = args[0]
        args = args[1:]
        
            
        parser = optparse.OptionParser( epilog=__doc__, add_help_option=False )
        
        if user_options is None:
            user_options = [ ]
        else:
            user_options = list( user_options )
            
        if user_arguments is None:
            user_arguments = [ ]
        else:
            user_arguments = list( user_arguments )
        
        if inputs is None:
            self.inputs = []
        else:        
            self.inputs = list( inputs )
        
        
        self.user_options = user_options
        self.user_arguments = user_arguments
        self.help = help
        self.use_stdin = use_stdin
        self.use_stdout = use_stdout
            
        syshelp = optparse.Option( '-H','--Help',
                                   action='callback',
                                   callback=self.option_help
                                    )
        
        userhelp = optparse.Option( '-h','--help',
                                   action='callback',
                                   callback=self.user_help
                                    )

        userman = optparse.Option( '--manpage',
                                   action='callback',
                                   callback=self.user_manpage
                                    )
        
        slab_help_options = [ syshelp, userhelp,userman ]
        
        helpgroup = optparse.OptionGroup( parser, 'SLAB help' )
        helpgroup.add_options( slab_help_options )
        
        sysgroup = optparse.OptionGroup( parser, 'SLAB built-in options' )
        sysgroup.add_options(slab_options )

        usergroup = optparse.OptionGroup( parser, 'Program specific options' )
        usergroup.add_options( user_options )
        
        parser.add_option_group( sysgroup )
        parser.add_option_group( usergroup )
        parser.add_option_group( helpgroup )
        
        values, newargs = parser.parse_args(list(args))
        
        kw = {}
        for argdef in self.user_arguments:
            key = argdef.name
            value = argdef.default
            
            if value is NoDefault:
                continue
            else:
                kw[key] = value
                
                
        xargs = []
        for arg in newargs:
            if '=' in arg:
                key,val = arg.split( '=', 1 ) 
                kw[key] = val
                if len(val) == 0:
                    raise Exception( "Expected a value afer '%s=' on command line, got ''"%key )
            else:
                xargs.append( arg )
            
        for argdef in self.user_arguments:
            key = argdef.name
            etype = argdef.type
            
            if etype is not None and key in kw: 
                value = kw[key]
                try:
                    value = etype(value)
                except:
                    kname = getattr(etype, '__name__', str(etype) )
                    raise KeyError( "could not read argument '%s=' from command line with expected type '%s got: %s ' " %(key,kname,value) )
             
            
        self.args = xargs
        self.kw = kw
        
        self.options = values_to_dict( values )
        self.options.update( options )
        
        if self.verbose:
            print >> sys.stderr, "SLAB: Creating Verbose Environment:"
            for key,val in self.options.items():
                print >> sys.stderr, "%20s = %r" %(key,val)
        
        datapath_log = self.options['datapath_log']
        datapath = self.options['datapath']
        if datapath_log is True:
            self.options['datapath_log'] = os.path.join(datapath,'.dp_log')
        
        if self.user_arguments: 
            uargs = set( [u.name for u in self.user_arguments] )
            gargs = set( kw.keys( ) )
            
            diff = gargs.difference( uargs )
            if diff: 
                print >> sys.stderr, ("signal_lab warning: Got unexpected user arguments ( '%s=' )" %("=', '".join(diff)))
                
        return
    
    def copy(self):
        """
        returns a copy of this environment
        """
        env = Environment(None)
        env.kw =  self.kw.copy()
        env.options =  self.options.copy()
        env.args =  list(self.args)
        return env
    
    def _sl_getint(self,value):
        return int(self.kw[value])
    
    def _sl_getfloat(self,value):
        return float(self.kw[value])
    
    def _sl_getstring(self,value):
        return str(self.kw[value])
    
    def get_bool(self,value, kw=None ):
        
        warnings.warn( 'method env.get_bool is depricated, please use get_eval with etype=env._bool', DeprecationWarning )
        
        if kw:
            return self._bool(kw[value])
         
        return self.get_eval( value, etype=self._bool )

    @classmethod
    def _bool(cls,value):
        '''
        If value is a string,  'N','NONE' and 'FALSE' will evaluate to False.
        and 'YES','Y' and 'TRUE' evaluate to true. otherwize the string is evaluated as 
        python expression. 
        '''
        if isinstance( value, str ):
            if value.upper() in ['N','NO','NONE','FALSE']:
                return False
            elif value.upper() in ['YES','Y','TRUE']:
                return True
            else:
                return bool( eval(value) )
        else:
            return bool(value)
        
    def get_eval( self, *args, **kwargs ):
        '''
        env.get_eval( key [, default] [, etype=eval ] )
         
        '''
        if len(args) not in [1,2]:
            raise TypeError( 'Environment.get_eval takes 1 or 2 arguments (%i given)' %len(args) )
        
        
        key = args[0]

        if isinstance(key, str ):
            edefault = eval
        else:
            edefault = lambda args : args
        
        etype = kwargs.get( 'etype' , edefault )
        
        if key in self.kw:
            value = self.kw[key] 
            try:
                result = etype( value )
            except:
                kname = getattr(etype, '__name__', str(etype) )
                raise KeyError( "could not read key '%s=' from command line arguments with constructor '%s( %s )' " %(key,kname,value) )
            
            if self.verbose: print >> sys.stderr, "Eval Command line: %s=%r type '%s' " %( value, result, type(result) )
            
            return result
        
        else:
            if len(args) == 2:
                return args[1]
            else:
                raise KeyError( "no key '%s=' in command line arguments" %key )
            
    
        
    
    def get_sequence( self, id , omit=None, type=eval ):
        """
        get a sequence of parameters from the command line.
        
        eg. for min1=2 min2=3
        
        >>> env.get_sequence( 'min%i' , type=int )
        [2,3]
        """
        x = []
        ndim = 0
        while id%(ndim+1) in self.kw.keys():
             
            key = id%(ndim+1)
            if omit is not None and self.kw[key] == omit:
                pass
            else:
                x.append( type( self.kw[key] ) )
            ndim+=1
        
        if self.options['order'] == 'C':
            x.reverse( )
        
        return tuple(x)

    def _get_verbose( self ):
        return self.options.get('verbose',False)

    def _set_verbose( self, value ):
        self.options['verbose'] = value
    
    verbose = property( _get_verbose, _set_verbose, doc="print verbose output if true" )
    
    def subst(self, strexpr ):
        '''
        substitute names of the form '$names' with values from the keyword and global options
        '''
        template = string.Template( strexpr )
        template_dict = {}
        template_dict.update( self.kw )
        template_dict.update( self.options )

        try:
            result = template.substitute( **template_dict )
        except KeyError, ke:
            key = ke.args[0]
            raise error( "while substituting tag '%s', no Key '%s=' in command line arguments or signal_lab options" %(strexpr,key)  )
        
        return result
    
    def warn( self, msg ):
        '''
        
        '''
        if self.options['permissive']:
            print >> sys.stderr, "SLAB WARNING:",msg
            sys.stderr.flush( )
        else:
            raise error( msg )
        return 
        
    def __getitem__(self,item):
        """
        get an argument from the command line.
        if item is an int, getitem returns the non-keyword argument at that index.
        Otherwize, returns the keyword argument with the key item.
        """
        if isinstance(item, int):
            result = self.args[item]
            if self.verbose: print >> sys.stderr, "getting argument at idx %s, '%s' from command line" %(item,result)
        else:
            if item not in self.kw:
                msg = "No '%s=' was specified on the command line" %item
                raise KeyError( msg )
            
            result = self.kw[item]
            if self.verbose: print >> sys.stderr, "getting key-word argument %s=%s from command line" %(item,result)
            
        if isinstance(result, str):
            try:
                result = eval(result)
            except:
                pass
        
        return result
    
    @classmethod
    def _check_input_(cls,fname):
        fname = str(fname)
        if not os.path.isfile( fname ):
            raise error( "file %s does not exist" %fname )
        
        return fname
    
    @classmethod
    def _check_rsf_input_(cls,fname):
        fname = str(fname)
        if not os.path.isfile( fname ):
            raise error( "file %s does not exist" %fname )
        
        _,suffix = os.path.splitext(fname)
        if suffix.lower() not in['.rsf','.h','.hh']:
            print >> sys.stderr(" warning RSF input does not conform to standard extension '.rsf' " )
        
        return fname
        
    
    _check_input = (_check_input_,'input')
    _check_output = (str,'output')

    _check_rsf_input = (_check_rsf_input_,'rsf input')
    _check_rsf_output = (str,'rsf output')
    
    

def index_to_pos( shape, indexing, order='F' ):
    
    index = np.array( indexing, dtype=np.int64 )
    
    cp = np.cumprod( shape, dtype=np.int64 ) #@UndefinedVariable
    cps = np.sum( index[1:]*cp[:-1],dtype=np.int64) #@UndefinedVariable
    return long(cps+index[0]) #@UndefinedVariable
    

class File( object ):
    """
    slab.File object represents the rsf File format and deals with 
    the seporate header and binary files. 
    """
    __OPENED_HEADER_FILES__ = 0
    __FINALIZED_FILES__ = 0
    
    
    terminate = u'\x0c\x0c\x04'
    _type_map = {
    "shortint": { 2:'int16'},
    "int": { 4:'int32'},
    "longint": { 8: 'int64'},
    
    "float": { 4:'float32'},
    "double": { 8:'float64'},
    "longdouble": { 16: 'float128'},

    "complex": { 8:'complex64'},
    "complexdouble": { 16:'complex128'},
    "complexlongdouble": { 32: 'complex256'},
    }

    _dtype_map = {
    'int16' :("shortint", 2),
    'int32' :("int", 4),
    'int64' :("longint", 8),

    'float32' :("float", 4),
    'float64' :("double", 8),
    'float128' :("longdouble", 16),

    'complex64' :("complex", 8),
    'complex128' :("complexdouble", 16),
    'complex256' :("complexlongdouble", 32),
    
    }

    def __init__( self, tag, input=True, env=None, header_only=False, **options ):
        
        self._changed_header_keys = {}
        self._kw_comments = {}
        self._comments = []
        self._to_delete =[]
        self.nb_read = 0
        self.nb_written = 0
        self.tag = tag
        self.header_only = header_only
        
        
        if input is True:
            if env and env.verbose: print >> sys.stderr, "Initializing input: '%s'" %(tag)
            self.init_input( tag, env=env, **options )
        else:
            self.init_output( tag, input=input, env=env, **options )
            if self.env.verbose: print >> sys.stderr, "Creating output: '%s' from='%s'" %(tag, getattr(input, 'tag', 'new' ) )
        
        return 
    
    def init_input(self, tag, env=None, **options ):
        
        if env is None:
            self.env = Environment( [] )
        else:
            self.env = env.copy( )
         
        self.env.options.update( options )
        
        self.header = self.env.subst( tag )
            
            
        
        #if tag == 'in':
        #    tag = env.options.get( 'stdin', 'stdin' )

        if self.header == 'file:sys.stdin':
            #header = 'stdin'
            header_file = sys.stdin
            self.packed = True
            
            isatty = header_file.isatty( )
            accept_tty = self.env.options.get( 'accept_tty', False )
            if isatty and not accept_tty:
                raise Exception("can not accept tty device '%s' as an rsf file" %self.header)
        elif self.header == 'file:sys.stdout':
            raise error( 'can not initialize header input file with stdout' )
        else:
            read_permissions = self.env.options.setdefault( 'header_in_mode' , 'r' )
            header_file = open( self.header, read_permissions )
            self.packed = False
        
        self.header_file = header_file
        
        header_keys,history = File.read_header(self.header_file,self.env)
        
        self.history = history
        self._header_keys = header_keys
        
        self.is_input = True
        self.finalized = True
    
        self.binary = self['in']
        
        if self.header_only:
            binary_file = None
        else:
            if self.binary == 'stdin': 
                binary_file = self.header_file
                self.packed = True
            else:
                read_permissions = self.env.options.setdefault( 'binary_in_mode' , 'r' )
                
                ########################################################
                ## RSF local path name in binary file
                ########################################################
                if not os.path.isfile(self.binary):
                    if (os.path.abspath( self.binary ) != self.binary) and self.env.options['local_binary']:
                        self.binaryos.path.join( os.path.dirname(self.header), self.binary )
                ########################################################
                ########################################################
                    
                binary_file = open(self.binary, read_permissions)
            
        self.binary_file = binary_file
        
        if not self.packed:
            self.header_file.close( )
        
        File.__OPENED_HEADER_FILES__+=1
        File.__FINALIZED_FILES__+=1
        
        dstat = os.fstat(self.binary_file.fileno())
        stat_fifo = stat.S_ISFIFO( dstat.st_mode )
        stat_size = dstat.st_size 
        #print "ISREG",stat.S_ISREG( dstat.st_mode )
        if stat_fifo:
            self.original_tell_pos = -1
        else:
            if stat_size != self.nbytes:
                self.env.warn( "size of binary '%s' is not as expected (%i != %i)" %(self.binary,stat_size,self.nbytes) )
                
            
            self.original_tell_pos = self.binary_file.tell()
    
    def _get_is_fifo(self):
        
        dstat = os.fstat( self.binary_file.fileno() )
        return stat.S_ISFIFO( dstat.st_mode )
        
    is_fifo = property( _get_is_fifo )
    
    def reset_binary(self):
        
        if self.is_fifo:
            raise Exception( "'%s' is a fifo device, can not reset" %self.header )
        
        self.binary_file.seek( self.original_tell_pos )
        
        return self.original_tell_pos
     
    
    def init_output(self,tag, input=False, env=None, **options):
        
        if isinstance(input, File ):
            if env is None:
                self.env = input.env.copy()
            else:
                self.env= env.copy()

            self._header_keys = input._header_keys.copy( )
            self.history = list(input.history)
        else:
            
            if env is None:
                self.env = Environment( [] )
            else:
                self.env= env.copy( )
            
            self._header_keys = { }
            self.history = [ ]
        
        self.env.options.update( options )
        
        pack = self.env.options.get( 'pack', False )
        
        self.packed = pack
        
        self.header_file = None
        self.binary_file = None
        
        
        self.finalized = False
        self.is_input = False
         
        self.binary_file = None
    
        
        
        #if tag == 'out':
        #    tag = self.env.options.get( 'stdout','out' )
            
        #if tag == 'out':
        #    header = 'stdin'
        #else:
        #    header = tag
            
        self.tag = tag
        #self.header = header
        
        File.__OPENED_HEADER_FILES__+=1
        
        return 
    
    
    def header_is_reg(self):
        return stat.S_ISREG( os.fstat(self.header_file.fileno())[0] )
     
    def _open_output(self):
        
        header = self.env.subst( self.tag )
        
        if header == 'file:sys.stdout':
            self.header = 'stdout'
            header_file = sys.stdout
            
            isatty = header_file.isatty()
            accept_tty = self.env.options.get( 'accept_tty', False )
            if isatty and not accept_tty:
                raise Exception("can not accept tty device '%s' as an rsf file" %self.header )
            
        elif header == 'file:sys.stdin':
            raise error( 'can not initialize header output file with stdin file descriptor' )
        else:
            if self.env.options.get( 'fifo', False ):
                os.mkfifo(self.header)
                
            self.header = header
            
            mode  = self.env.options.setdefault( 'header_out_mode' , 'w' )
            header_file = open( header, mode )
            
            
        fd = header_file.fileno()
        
        
        if stat.S_ISREG( os.fstat(fd)[0] ) and not self.packed:
            if header == 'file:sys.stdout':
                self.header = self.get_open_file_name( header_file )
            else:
                self.header = header
            
            self.packed = False
            
            header_name = os.path.split( self.header )[-1]
            datapath = self.env.options.get('datapath', '.' )
            binary = os.path.join( datapath, header_name ) + '@'
            bin_exists = os.path.isfile(binary)
            
            if not self.env.options['replace_binaries']:
                binary_pt = os.path.splitext(binary)[0]
                count = 0
                if bin_exists and self.env.verbose: print >> sys.stderr,"File '%s' exists. " %(binary),
                while bin_exists:
                    count+=1
                    binary = binary_pt + '%i.rsf@' % count
                    bin_exists = os.path.isfile(binary)
                if count and self.env.verbose: print >> sys.stderr, "Choosing '%s' as new binary file name" %(binary)
            elif bin_exists and self.env.verbose: print >> sys.stderr, "Overwriting exsisting binary file '%s'" %(binary) 
        else:
            self.packed = True
            binary = 'stdin'
            
        #self.header = header
        self.header_file = header_file
        self.binary = binary
        self._header_keys['in'] = binary
        self._changed_header_keys['in'] = binary

    def comment(self, *args, **kw):
        """
        add comments to the header file. if a keyword argument is given.
        The comment will be placed above the keyword in the header file.  
        """
        self._comments.extend(args)
        self._kw_comments.update(kw)
        
    
    def close(self, doraise=True ):
        """
        close both the header and binary files. 
        """
        if self.original_tell_pos != -1:
            self.last_tell_pos = self.binary_file.tell()
        
        self.header_file.close()
        self.binary_file.close()
        
        if self.original_tell_pos != -1:
            nbytes = self.nbytes
            nreadwrite = self.last_tell_pos-self.original_tell_pos
            
            if (doraise and nreadwrite!=nbytes):
                msg = "number of bytes %s is not equal to the number of bytes in the binary file (%i != %i)" %(self.is_input and "read" or "written", nreadwrite,nbytes )
                msg+="\n            : for header '%s' binary '%s'" %(self.header, self.binary)
                
                self.env.warn( msg )
                
#                    
#    def __del__( self ):
#        
#        self.close( )
    
        
    _trace_header = None
    
    def _get_trace_header( self ):
        
        if self._trace_header is None:
            self._trace_header = File( self['head'], env=self.env )
            
        return self._trace_header
    
    def _set_trace_header( self, value ):
        
        self._trace_header = value
        
        if isinstance(value, str):
            self['head'] = value 
        else:
            self['head'] = str( value.header )
        
    trace_header = property( _get_trace_header, _set_trace_header, 
                             doc="Return the trace header given by head= in the header file as a slab.File object" )
    
    def _get_h_abspath(self):
        return os.path.abspath(self.header)
    header_abspath = property( _get_h_abspath, doc='absolute file path to the header' )
    
    def _get_h_dirname(self):
        return os.path.normpath(os.path.dirname(self.header))
    header_dir = property( _get_h_dirname, doc='directory in which the header resides' )
    
    def _get_h_basename(self):
        return os.path.basename(self.header)
    header_base = property( _get_h_basename, doc='name of the header, minus any directory portion' )

    def _get_h_filebase(self):
        return os.path.splitext(self.header_base)[0]
    header_filebase = property( _get_h_filebase,
                                doc='Just the basename of the header file, minus any suffix and minus the directory.' )

    def _get_b_dirname(self):
        return os.path.dirname(self.binary)
    binary_dir = property( _get_b_dirname ,doc='directory in which the binary resides')
    
    def _get_b_basename(self):
        return os.path.basename(self.binary)
    binary_base = property( _get_b_basename,doc='name of the binary, minus any directory portion'  )

    def _get_b_filebase(self):
        return os.path.splitext(self.binary)[0]
    binary_filebase = property( _get_b_filebase,
                                doc='Just the basename of the binary file, minus any suffix and minus the directory.' )
    
    def _get_b_abspath(self):
        return os.path.abspath(self.binary)
    binary_abspath = property( _get_b_abspath, doc='absolute file path to the header' )

    def _log_output(self):
        
        dp_log = self.env.options['datapath_log']
        
        if (not dp_log) or self.packed:
            return

        impl = minidom.getDOMImplementation()

        if not os.path.isfile( dp_log ):
            try:
                doc = impl.createDocument(None,"SLAB_DATA_LOG",None)
                flog = open(dp_log, 'w' )
                flog.write( doc.toprettyxml() )
                flog.close()
            except Exception,e:
                warnings.warn( "Trouble initializing xml datapath logfile, reason: '%s'" %e , Warning, 3 )
                return 
        
        st_mtime = os.stat(dp_log).st_mtime
        
        while 1:
            
            try:
                flog = open( dp_log, 'r' )
                doc = minidom.parse( flog )
                flog.close()
            except Exception,e:
                warnings.warn( "Trouble reading xml datapath logfile, reason: '%s'" %e , Warning, 3 )
                return 
            
            root = doc.firstChild
            
            header_abspath = self.header_abspath
            binary_abspath = self.binary_abspath
            
            
            for element in root.getElementsByTagName('binary_header_pair'):
                if header_abspath == element.getAttribute('header'):
                    if binary_abspath == element.getAttribute('binary'):
                        return # Already have this element 
            
            for element in root.childNodes:
                if element.nodeType == doc.TEXT_NODE:
                    root.removeChild( element )
            
                
            element = doc.createElement( 'binary_header_pair' )
            element.setAttribute( 'header', header_abspath )
            element.setAttribute( 'binary', binary_abspath )
            
            root.appendChild( element )
            
            next_st_mtime = os.stat(dp_log).st_mtime
            
            if st_mtime != next_st_mtime:
                continue
            
            flog = open(dp_log, 'w+' )
            doc.writexml( flog, indent='  ' , addindent='', newl='\n' )
            flog.close( )
            
            break
            
        
        
        
        
        
    def finalize(self):
        """
        For outputs only.
        
        Header file is created and written to. Binary file is created.
        """
        if self.is_input:
            raise  Exception( 'can not finalize input')
        if self.finalized:
            raise  Exception( 'header output is already written' )
        
        self._open_output( )
        
        self._log_output( )
        
        self.finalized = True
        
        File.__FINALIZED_FILES__+=1
        
        self.header_file.writelines(self.history)
        
        try:
            user = os.getlogin()
        except:
            user = os.environ.get( 'USER', 'unknown' )
            
        if self.env.verbose: print >> sys.stderr, "writing header: '%s'" %(self.header)
        
        loging = "%s@%s"%( user, os.uname()[1] )
        print >> self.header_file, "#",self.env.prog, loging, ctime(time())
        print >> self.header_file, "#"
        print >> self.header_file, "# Created with the command: '"," ".join( sys.argv ),"'"
        print >> self.header_file, "#"
        for comment in self._comments:
            print >> self.header_file, "#",comment.replace("\n", "\n# ")
        
        for item in self._changed_header_keys.items():
            toprint = ("\t%s=%r" %item).replace("'",'"')
            if item[0] in self._kw_comments:
                print >> self.header_file,"\t# '%s':"%item[0], self._kw_comments[item[0]].replace("\n", "\n\t# ")
            print >> self.header_file, toprint 
        
        for item in self._to_delete:
            print >> self.header_file, "@del", item
        
        if self.binary == 'stdin':
            self.header_file.write(self.terminate)
        
        self.header_file.flush( )
        
        if not self.packed:
            self.header_file.close( )
        
        if self.env.options.get('dryrun'):
            do_exit = File.__OPENED_HEADER_FILES__ == File.__FINALIZED_FILES__
            if do_exit:
                print >> sys.stderr, "Dryrun exit"
                raise SystemExit( 0 )
        
        if self.binary == 'stdin':
            binary_file = self.header_file
        else:
            mode = self.env.options.setdefault( 'binary_out_mode' , 'w' )
            binary_file = open( self.binary, mode )
        
        self.binary_file = binary_file
        
        dstat = os.fstat(self.binary_file.fileno())
        stat_fifo = stat.S_ISFIFO( dstat.st_mode )
        
        if stat_fifo:
            self.original_tell_pos = -1
        else:
            self.original_tell_pos = self.binary_file.tell()
        
        return self
    
    def __delitem__(self, item ):
        self._to_delete.append(item)
        if item in self._header_keys:
            self._header_keys.__delitem__(item)
        if item in self._changed_header_keys:
            self._changed_header_keys.__delitem__(item)
        
        return 
        
    def items(self):
        return self._header_keys.items( )
    
    def keys(self):
        return  self._header_keys.keys( )

    def values(self):
        return  self._header_keys.values( )
    
    def __getitem__(self,item):
        return self._header_keys[item]
    
    def __setitem__(self,item,value):
        if self.is_input:
            raise Exception( "could not set header value of input file" )
        
        if self.finalized:
            raise Exception( "could not set header value, header is already finalized" )
        
        self._header_keys[item] = value
        self._changed_header_keys[item] = value
        
    def __repr__(self):
        try:
            tag = self.tag
        except:
            tag ='error'
        try:
            shape = self.shape
        except:
            shape ='[error]'
        try:
            type = self.type
        except:
            type ='error'
        
        return "<signal_lab.File tag=%r shape=%r type=%s>" %(tag,shape,type)
    
    def get( self, item, failobj=None ):
        return self._header_keys.get(item,failobj)
    
    def _get_ndim(self):
        ndim = 0
        while "n%s"%(ndim+1) in self.keys():
            ndim+=1 
        return ndim
    
    ndim = property( _get_ndim )
    
    
    def get_sequence(self, id , omit=None ):
        
        x = []
        ndim = 0
        doomit = False
        while id%(ndim+1) in self.keys():
             
            key = id%(ndim+1)
            if doomit and omit is not None and self[key] == omit:
                pass
            else:
                doomit=True
                x.append( self[key] )
            ndim+=1
        
        if self.env.options['order'] == 'C':
            x.reverse( )
        
        return tuple(x)
    
    def set_sequence(self, id , sequence ):

        if self.env.options['order'] == 'C':
            sequence = list(sequence)
            sequence.reverse( )
        
        for i,item in enumerate(sequence):
            key = id %(i+1)
            self[key] = item
        return
    
    def _get_size(self):
        return int(np.prod( self.shape, dtype=np.int64 ))
    
    size = property(_get_size)
    
    def _get_nbytes(self):
        return long(self.esize)*long(self.size)
    
    nbytes = property( _get_nbytes ) 
    
    def leftsize(self,left):
        return np.prod( self.shape[left:], dtype=np.int64 ) 
        
    def _get_shape(self):
        return self.get_sequence( 'n%s' , omit=1 )

    def _set_shape(self, value ):
        return self.set_sequence( 'n%s' , value,  )
    
    shape = property( _get_shape ,_set_shape )

    def _get_origin(self):
        return self.get_sequence( 'o%s' )
    
    def _set_origin( self, value ):
        return self.set_sequence( 'o%s', value )
    
    origin = property( _get_origin, _set_origin )
    
    def _get_step(self ):
        return self.get_sequence( 'd%s' )

    def _set_step(self , value ):
        return self.set_sequence( 'd%s' , value )
    
    step = property( _get_step, _set_step )

    def _get_labels(self ):
        return self.get_sequence( 'label%s' )

    def _set_labels(self, value ):
        return self.set_sequence( 'label%s' ,value)
    
    labels = property( _get_labels, _set_labels )

    def _get_units(self ):
        return self.get_sequence( 'unit%s' )
    
    units = property( _get_units )
    
    def _get_order(self):
        return self.env.options['order']
    
    order = property( _get_order )
    
    def _get_type(self):
        
        _, type = self['data_format'].split('_',1) 
        return type

    def _set_type(self,value):
        
        form , _ = self.get('data_format','native_NONE').split('_',1)
        self['data_format'] = "_".join([form , value])  
        return type
    
    type = property( _get_type, _set_type )

    def _get_form( self ):
        
        form , _  = self['data_format'].split('_',1) 
        return form
    
    
    form = property( _get_form )
    
    def _get_esize(self):
        return self['esize']

    def _set_esize(self,value):
        self['esize'] = value
    
    esize = property( _get_esize,_set_esize )
    
    @classmethod
    def get_open_file_name( cls, open_file ):
        command = 'lsof -a +p %i -Fin'
        
        
        pid = os.getpid()
        st_inode = os.fstat( open_file.fileno() )[1]
        
        
        p0 = subprocess.Popen( command %(pid) , shell=True, stdout=subprocess.PIPE ,stderr=subprocess.PIPE )
        
        err= p0.wait()
        
        if err:
            return os.tmpnam()+'.rsf'
            
        res = p0.stdout.read( ).split( '\n' )
        
        inode = "i%s" %st_inode
        if inode in res:
            of = res[ res.index( "i%s" %st_inode )+1]
            return of[1:]
        else:
            return os.tmpnam()+'.rsf' 
        

    @classmethod    
    def read_header( cls, open_file,env ):
        
        header_keys = {}
        history = []
        
        pop = ''
        
        lineno = 0
        while 1:
            lineno+=1
            pop = open_file.read( 1 )
            if pop == '':
                break
            if pop == '\n':
                continue
            if pop == cls.terminate[0]:
                term = open_file.read( 2 )
                if term != cls.terminate[1:]:
                    raise Exception( 'Header not properly formatted first bit of termination sequence found but not the next two' )
                break 
            
            line = open_file.readline( )
            line = pop + line
            
            line = line.split("#",1)[0]
            history.append( line )
            if '=' in line:
                line = line.strip( )
                key, value = line.split( '=', 1 )
                
                #workaround for non-standard headers like sep *.H files 
                # sets next: in= "*.H"
                key = key.split( )[-1]
                
                try:
                    value_new = eval(value)
                    value = value_new
                except:
                    msg = "SLAB WARNING: could not guess type of header key %s=%s, defaults to string: file '%s': line %i" %( key, value, open_file.name, lineno )
                    print >> sys.stderr, msg
                    
                 
                header_keys[key] = value
            elif "@del" in line:
                words = [word.strip("\t ,") for word in line.split("@del",1)[-1].strip(" ,()\n").split(" ")]
                for word in words:
                    if word in header_keys:
                        del header_keys[word]
                        
#                print "words", words
            
            
        return header_keys,history
    
    def _get_dtype(self):
        typename = self._type_map[self.type][self.esize]
        
        dt = np.dtype(typename)
        
        if self.byteswap:
            dt = dt.newbyteorder('S')
        
        return dt 

    def _set_dtype( self, dtype ):
        
        type,esize = File._dtype_map[str(dtype)]
        
        self.esize = esize
        self['data_format'] = "native_%s" %(type)
    
    def _get_basename(self):
        bname = os.path.basename( self.header )
        return os.path.splitext(bname)[0]
    
    basename = property( _get_basename )
        
        
    dtype = property( _get_dtype, _set_dtype )
    
    def __array__( self , dtype=None ):
        
        if dtype and dtype != self.dtype:
            raise Exception("can not cast memory map to new dtype got %s, expected 'dtype=' None or %s" %(dtype,self.dtype) )
        
        if self.packed:
            raise Exception( 'Can not create numpy.memmap from fifo/packed header and binary' )
        
        
        if self.is_input:
            mode = self.env.options.get( 'binary_in_mode', 'r' )
        else:
            if not self.finalized:
                raise Exception("File.finalize must be called before calling File.__array__ method for output arrays")
            
            mode = self.env.options.get( 'binary_out_mode', 'write' )
            if mode=='w': mode = 'write'
        
        array = np.memmap( self.binary, mode=mode, shape=self.shape, dtype=self.dtype, order=self.order )
        return array

    def to_array( self, error=True ):
        
        array = np.zeros( shape=self.shape, dtype=self.dtype, order=self.order )
        self.into_array(array, error)
        return array
        
    def into_array( self, array, error=True ):
        
        buffer = array.data
        
        nbread = self.binary_file.readinto( buffer )
        
        if error and ( nbread != len(buffer) ):
            raise IOError( "number of bytes read does not equal the number requested ( %s != %s)"  %(nbread, len(buffer)) )
        
        return 
    
    
    def from_array(self,array):
        self.binary_file.write( array.data )
    
    def from_coords(self, value , error=True ):
        
        N = self.shape
        O = self.origin
        D = self.step
        
        result = np.divide(np.subtract(value,O), D).astype(int)
        
        if error:
            greater_zero = np.all( np.greater_equal( result, 0 ) )
            less_N = np.all( np.less( result, N ) )
            if not (greater_zero and less_N):
                raise IndexError("coordinate outside range of data %s" %(result) )
        return result.astype(int)
    
        
    def to_coords(self, value ):
        
        N = self.shape
        O = self.origin
        D = self.step

        result = np.zeros( len(value) )
        np.multiply( value, D , result )
        result = np.add( result, O , result)
        return result
        
        
    def readinto( self, buffer, error=True ):
        
        if hasattr( buffer, 'data' ):
            buffer = buffer.data 
        
        count = len(buffer)
            
        nr = self.binary_file.readinto( buffer )
        
        self.nb_read += nr
        
        if nr != count:  
            msg = "binary file '%s' from header '%s': could not read past %i bytes, expected %i" %(self.binary_abspath,self.header_base,self.nb_read,self.nbytes)
            if error == 'warn':
                warnings.warn( msg , UserWarning )
            if bool(error):
                raise Exception( msg )
            else:
                pass
        
        return nr
    
    def _get_endian(self):
        
        if self.form == 'native':
            return little_endian
        elif  self.form == 'xdr':
            return False
        elif self.form == 'big':
            return False
        else:
            return True
            
    endian = property( _get_endian )
    
    def do_byteswap(self):
        
        return not little_endian == self.endian
    
    
    def _get_byteswap(self):
        if hasattr(self, '_byteswap_data' ):
            return self._byteswap_data
        else:
            return self.do_byteswap( )
        
    def _set_byteswap(self,value):
        self._byteswap_data = bool(value)
            
    byteswap = property( _get_byteswap,_set_byteswap )
    
    def read(self, buffer=None, count=-1, doraise=True ):
        
        return cSlab.read( self.binary_file, buffer=buffer, count=count, esize=self.esize, byteswap=self.byteswap )
            
            
        
            
    
    ## Functions for c api
    def _sl_getint(self,value):
        return int(self[value])
    
    def _sl_getfloat(self,value):
        return float(self[value])
    
    def _sl_getstring(self,value):
        return str(self[value])
    
    
    trace_header_keys = ['tracl', 'tracr', 'fldr', 'tracf', 'ep', 'cdp', 'cdpt', 
                         'trid', 'nvs', 'nhs', 'duse', 'offset', 'gelev', 'selev', 
                         'sdepth', 'gdel', 'sdel', 'swdep', 'gwdep', 'scalel', 
                         'scalco', 'sx', 'sy', 'gx', 'gy', 'counit', 'wevel', 'swevel', 
                         'sut', 'gut', 'sstat', 'gstat', 'tstat', 'laga', 'lagb', 'delrt', 
                         'muts', 'mute', 'ns', 'dt', 'gain', 'igc', 'igi', 'corr', 'sfs', 
                         'sfe', 'slen', 'styp', 'stas', 'stae', 'tatyp', 'afilf', 'afils', 
                         'nofilf', 'nofils', 'lcf', 'hcf', 'lcs', 'hcs', 'year', 'day', 
                         'hour', 'minute', 'sec', 'timbas', 'trwf', 'grnors', 'grnofr', 
                         'grnlof', 'gaps', 'otrav']
    
    @classmethod
    def get_number_keys(cls):
        return len(cls.trace_header_keys)
    @classmethod
    def get_key_index(cls, *p ):
        
        if len(p) < 1 or len(p) > 2:
            raise TypeError("File.get_key_index takes 1 or 2 arguments (got %i)" %len(p) )
        
        key_name = p[0]
        
        
            
        
            
        try:
            idx = cls.trace_header_keys.index( key_name )
        except ValueError:
            if len(p) ==2:
                return p[1]
            else:
                raise ValueError( "Unknown trace header key name '%s'" %(key_name,) )
        
        return idx
    
    def serialize(self):
        
        newd = dict(self.__dict__)
        newd['binary_file'] = None
        newd['header_file'] = None
        
        result = cPickle.dumps( newd )
        
        return result
            
    def unserialize( self, obj ):
        
        newd = cPickle.loads( obj )
        
        self.__dict__.update( newd )
        
    
    def seek_to_trace( self, index ):
        
        bin = self.binary_file
        
        pos = index_to_pos( self.shape, [0]+list(index) )
                
        bin.seek( pos, 0 ) 

        return pos
    
    
    