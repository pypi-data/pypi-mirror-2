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

from SCons.Script import AddOption,SConscript,Environment
from glob import glob 
from os.path import join,isfile,isdir,abspath
from os.path import split
from sconfig import add_to_default_toolpath
from sconfig.autotoolgen import ToolCreator
from sconfig import DoConfig
import distutils.sysconfig
from slabcore.SLABConfigError import do_missing_component,do_missing_tool
from sconfig.sort_components import ComponentsCmp

HAVE_CONFIGFILE_OPT = False
CONFIGFILE_OPT = {}

def StdInstall( env, toolname, dest ):

#    env.Help( """Local Options:
#    --prefix=/path/to/install/dir
#        default: '/usr/local'
#        
#    
#    --lib-prefix=prefix/lib
#
#    --bin-prefix=prefix/bin
#
#    --python-prefix=[std python installation]
#
#    --include-prefix=prefix/include
#    
#    --no-std-python-install
#        default: False
#        if true installs python modules to prefix/lib instead 
#        of the standard python place.
#    """ )

    AddOption( '--prefix',
           dest='prefix',
           nargs=1, type='string',
           action='store',
           metavar='DIR',
           default='/usr/local',
           help='installation prefix' )

    AddOption( '--lib-prefix',
           dest='lib_prefix',
           nargs=1, type='string',
           action='store',
           metavar='DIR',
           help='installation prefix' )

    AddOption( '--bin-prefix',
           dest='bin_prefix',
           nargs=1, type='string',
           action='store',
           metavar='DIR',
           help='installation prefix' )

    AddOption( '--python-prefix',
           dest='python_prefix',
           nargs=1, type='string',
           action='store',
           metavar='DIR',
           help='installation prefix' )

    AddOption( '--include-prefix',
           dest='include_prefix',
           nargs=1, type='string',
           action='store',
           metavar='DIR',
           help='installation prefix' )

    AddOption( '--no-std-python-install',
           dest='std_python',
           action='store_false',
           metavar='DIR',
           default=True,
           help='install python modules to /prefix/lib instead of standard location' )
    
    tc = ToolCreator( toolname, dest )
    
    PREFIX = distutils.sysconfig.PREFIX
    INSTALL_PREFIX = abspath(env.GetOption('prefix') or PREFIX )
    lib_prefix = env.GetOption('lib_prefix') or join(INSTALL_PREFIX ,'lib' )
    bin_prefix = env.GetOption('bin_prefix') or join(INSTALL_PREFIX ,'bin')
    include_prefix = env.GetOption('include_prefix') or join(INSTALL_PREFIX, 'include' )
    
    
    std_python = env.GetOption('std_python')

    if not std_python:
        python_prefix = join(INSTALL_PREFIX, 'lib' )
    else:
        python_prefix = distutils.sysconfig.get_python_lib( prefix=INSTALL_PREFIX )
        if  not python_prefix.startswith(INSTALL_PREFIX):
            py_vers = distutils.sysconfig.get_python_version()
            python_prefix = join ( INSTALL_PREFIX, "lib/python%s/site-packages"  %(py_vers) ) 
            
        
    
    python_prefix = env.GetOption('python_prefix') or python_prefix
    
    tc.Replace( INSTALL_PREFIX=INSTALL_PREFIX,
                lib_prefix=lib_prefix,
                bin_prefix=bin_prefix,
                python_prefix=python_prefix,
                include_prefix=include_prefix,
                tool_dest = dest
                )
    tc.Exists(True)
    
    tc.CreateTool( env )
#    env.Install( dest, "%s.py" %toolname )

HAVE_TOOLPATH_OPT = False

def CommandLineToolPath( env ):
    global HAVE_TOOLPATH_OPT
    
    if not HAVE_TOOLPATH_OPT:
        AddOption( '--local-toolpath',
               dest='local_toolpath',
               nargs=1, type='string',
               action='store',
               metavar='DIR',
               help='configuration defaults' )
        
        HAVE_TOOLPATH_OPT = True
   
    
    local_toolpath = env.GetOption( 'local_toolpath' )
    
    if local_toolpath:
        local_toolpath = local_toolpath.split(":")
    else:
        local_toolpath = []
        
    for toolpath in local_toolpath:
        add_to_default_toolpath(toolpath)
    
    return
    
    

def LoadConfigFile( nenv ):
    
    global HAVE_CONFIGFILE_OPT
    if not HAVE_CONFIGFILE_OPT:
        
        AddOption( '--config-file',
               dest='config_file',
               nargs=1, type='string',
               action='store',
               metavar='DIR',
               default=None,
               help='configuration defaults' )
        
        HAVE_CONFIGFILE_OPT = True
    
        config_file = nenv.GetOption( 'config_file' )
        
        if config_file:
            config_file = abspath(config_file)
            exec open(config_file) in CONFIGFILE_OPT
    
    nenv.Replace( **CONFIGFILE_OPT )
    
    return






#===============================================================================
# Local variables and functions
#===============================================================================

_sconscript = lambda path: isfile(path) and SConscript( path )

def add_list(env,name):
    
    disable_ = env.GetOption(name)
    if not disable_:
        disable_ = []
    else:
        disable_ = disable_.split(",")
        
    return disable_

def AddSLABVariables( vars ):
    
    
    pass

def AddSLABOptions( env=None ):
    
#    AddOption( '--fatal-error',
#           dest='fatal',
#           action='store_true',
#           default=False,
#           help='do not ignore errors' )

    AddOption( '--disable-users',
           dest='disable_users',
           action='store',
           default="",
           help='do not configure users folders' )
    
    AddOption( '--disable-components',
           dest='disable_components',
           action='store',
           default="",
           help='do not configure or run components' )
    
    AddOption( '--disable-tools',
           dest='disable_tools',
           action='store',
           default="",
           help='do not configure specified external tools' )
    
    if env:
        
#        env['fatal_error'] = env.GetOption('fatal') or False
                    
        env['disable_users'] = add_list(env,'disable_users')
        env['disable_components'] = add_list(env,'disable_components')
        env['disable_tools'] = add_list(env,'disable_tools')

    return 


def standard_tools_config( env=None ):
    """
    """
    
    if env is None:
        env = Environment( )

    external_tools = [ cnt for cnt in glob( "external_tools/*" ) if isdir(cnt) ]
    
    if DoConfig( env ):
        print "    +-------------------------------+"
        print "    |        Configure Tools        |"
        print "    +-------------------------------+"
    
    ccmp = ComponentsCmp( external_tools, None )
    external_tools.sort( ccmp )
    external_tools.sort( ccmp )
    for ex_tool in external_tools:
        tool_name = split(ex_tool)[-1]
        if tool_name in env.get('disable_tools',[]):
            do_missing_tool( env, ex_tool )
        else:
            if not (env.GetOption('clean') or env.GetOption('help') ):
#                print  "+ Configuring external tool:", ex_tool
                print  "    | Tool: '%s'" %(tool_name)
            try:
                _sconscript( join(ex_tool,"SConfig") )
                add_to_default_toolpath( abspath( ex_tool ) ) 
            except Exception, e:
                if env.GetOption('fatal'):
                    raise
                print "***********************************************************"
                print "ERROR: Not including component '%(ex_tool)s': got exception in %(ex_tool)s" %vars()
                print "Exception: %(e)s" %vars()
                print "This may make the slab package unstable"
                print "     To be safe use the option 'disable_component=%(ex_tool)s'" %vars()
                print "     also you can use the '--fatal-error' command line option to "
                print "     see the full error message"
                print "***********************************************************"
                do_missing_tool( env, ex_tool )

    return 
 

def standard_component_config( env=None ):
    """
    
    """
    
    if env is None:
        env = Environment( )
    
    components = [ cnt for cnt in glob( "components/*" ) if isdir(cnt) ]
    if DoConfig( env ):
        print "    +-------------------------------+"
        print "    |      Configure Components     |"
        print "    +-------------------------------+"

    #===============================================================================
    # Configure Everything First
    #===============================================================================
#    SConscript( join(core_components,"configure","SConfig") )
#    add_to_default_toolpath( abspath( join(core_components,"tools") ) )
    ccmp = ComponentsCmp( components, 'configure' )
    components.sort( ccmp )
    for component in components:
        component_name = split(component)[-1]
        comp_sconfig = join(component,"configure","SConfig")
        have_comp_sconfig = isfile(comp_sconfig)
        if component_name in env.get('disable_components',[]):
            do_missing_component( env, component )
        else:
            if not (env.GetOption('clean') or env.GetOption('help') ):
                print  "    | Component: '%s'" %(component_name),
                if have_comp_sconfig:
                    print
                else:
                    print "... (no configure script) yes"
            try:
                _sconscript( comp_sconfig )
                add_to_default_toolpath( abspath( join( component,"tools") ) )
            except Exception, e:
                if env.GetOption('fatal'):
                    raise
                print "***********************************************************"
                print "* ERROR: Not including component '%(component)s': got exception in %(component)s" %vars()
                print "* Exception: %(e)s" %vars()
                print "* This may make the slab package unstable"
                print "*      To be safe use the option 'disable_component=%(component)s'" %vars()
                print "*      also you can use the '--fatal-error' command line option to "
                print "*      see the full error message"
                print "***********************************************************"
                do_missing_component( env, component )
#        elif env['WARNINGS'] and not env.GetOption('clean'):
#            
#            print "WARNING: Not Configuring component: '%(component)s'" %vars()
            
    if DoConfig( env ):
        print "    +-------------------------------+"
        print "    |              DONE             |"
        print "    +-------------------------------+"
    return 
 