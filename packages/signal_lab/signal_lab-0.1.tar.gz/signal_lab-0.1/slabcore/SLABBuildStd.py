

from sconfig.sort_components import components_cmp

from glob import glob
from os.path import isdir,abspath,join,isfile,split
from sconfig import add_to_default_toolpath

from SCons.Script import SConscript
_sconscript = lambda path: isfile(path) and SConscript( path )


def Install_Tools( env ):
    
    external_tools = [ cnt for cnt in glob( "external_tools/*" ) if isdir(cnt) ]
#    components = [ cnt for cnt in glob( "components/*" ) if isdir(cnt) ]
    
    external_tools.sort( components_cmp )
    
    #===============================================================================
    # Install tools from external tools
    #     note: tools from components are installed from the function 
    #        SLABBuild_components below
    #===============================================================================            
    for ex_tool in external_tools:
        add_to_default_toolpath( abspath( ex_tool ) )
        if ex_tool in env.get('disable_tools',[]):
            pass
        else:
            py_src = env.Glob( join(ex_tool,"*.py") )
#            toolinstall = env.Install( env["tool_dest"], source=py_src )
#            env.Alias( ['tool','install'], toolinstall )
    return
               
               
def SLABBuild_user( env):
    
#    global HAVE_FATAL_OPTION
#    if not HAVE_FATAL_OPTION:
#        AddOption( '--fatal-error',
#           dest="fatal",
#           action='store_true',
#           help='do not ignore errors' )
#        HAVE_FATAL_OPTION = True

    
    for user in glob("user/*"):
        user_name = split(user)[-1]
        
        if user_name in env['disable_users']:
            if env['WARNINGS'] and not env.GetOption('clean'):
                print "WARNING: Not compiling user folder %(user)s" %vars()
        else:
            if isdir(user):
                try:
                    env.VariantDir( join("build",user), user, duplicate=0 )
                    SConscript( join("build",user,"SConstruct") )
#                    SConscript( join(user,"SConstruct") )
                except Exception, e:
                    if env.GetOption('fatal'):
                        raise
    
                    print "***********************************************************"
                    print "ERROR: Not including user folder '%(user)s' got exception" %vars()
                    print "EnvironmentError: %(e)s" %vars()
                    print "This may make the slab package unstable"
                    print "     To be safe use the option 'disable_users=%(user)s'" %vars()
                    print "     also you can use the '--fatal-error' command line option to "
                    print "     see the full error message"
                    print "***********************************************************"

def my_install_inc( env, comp_includes, sub ="" ):
    import pdb
#    pdb.set_trace()
    inc_dirs = [ str(dirs) for dirs in comp_includes if dirs.isdir( ) ]
    inc_files = [ str(dirs) for dirs in comp_includes if dirs.isfile( ) ]
    
    sub_incs = []
    for  dir in inc_dirs:
        xsub = join(sub,split(dir)[-1])
        new_dir = join(dir,"*")
#        print "call - my_install_inc"
        xsub_incs = my_install_inc( env, env.Glob(new_dir), xsub )
        sub_incs.append(xsub_incs)
#    print
#    print [str(x) for x in comp_includes]
#    print "installing ", inc_files,"- -",sub
    includes = env.Install(  join(env['include_prefix'],sub) , source=inc_files )
    env.Alias( ["install","include"], includes )
    env.Depends(includes, sub_incs )
    return includes

def SLABBuild_components( env ):
#    global HAVE_FATAL_OPTION
#    if not HAVE_FATAL_OPTION:
#        AddOption( '--fatal-error',
#           dest="fatal",
#           action='store_true',
#           help='do not ignore errors' )
#        HAVE_FATAL_OPTION = True

    components = [ cnt for cnt in glob( "components/*" ) if isdir(cnt) ]
    
    components.sort( components_cmp )
    
    #===============================================================================
    # Install components
    #===============================================================================
    for component in components:
        
        add_to_default_toolpath( abspath( join( component,"tools") ) )
        component_name = split(component)[-1]

        if component_name in env.get('disable_components',[]):
            pass
        else:
            try:
#                src_dir = join(component)
                varient_dir =  join( "build", component )
                sspt = join( varient_dir, "src","SConstruct")
#                if not isfile(sspt):
#                    sspt = join(component,"src","SConstruct")
                env.VariantDir( varient_dir, component, duplicate=0 )
                SConscript( sspt )
                
                comp_inc = join(component,'includes')
                if isdir( comp_inc ):
                    comp_includes = env.Glob( join( comp_inc,"*") )

                    my_install_inc( env, comp_includes )
                    
#                toolsdir = join( component ,'tools' )
#                if isdir( toolsdir ):
#                    core_tools = glob( join( toolsdir, "*.py" ) )
#                    intools = env.Install(  env['tool_dest'] , source=core_tools )
#                    env.Alias( "lib", intools )
            
                _sconscript( join(component,"doc","SConstruct") )
                _sconscript( join(component,"test","SConstruct") )
            except Exception ,e:
                if env.GetOption( 'fatal' ):
                    raise
                else:
                    print "***********************************************************"
                    print "ERROR: Not including component '%(component)s': got exception" %vars()
                    print "Exception: %(e)s" %vars()
                    print "This may make the slab package unstable"
                    print "     To be safe use the option 'disable_component=%(component)s'" %vars()
                    print "     also you can use the '--fatal-error' command line option to "
                    print "     see the full error message"
    
                    print "***********************************************************"
    