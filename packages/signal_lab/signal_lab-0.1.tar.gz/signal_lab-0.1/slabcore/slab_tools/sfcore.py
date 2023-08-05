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
"""
 \page sconstools SConstruct Tools
 \arg \subpage coretool
 
 \page coretool sfcore
    Core functionality such as slab root
    @sa @ref sf_install_main
    @sa @ref sf_install_libs
    @sa @ref sf_install_inc
    
    @xrefitem compiletools "Compile Tools" "Compile Time Tools" 
    
"""

from sconfig.confighelper import Get
## Genereat the rsf compile time environment 
# this 
def generate(env):
    """
    Generate 
    """
    
    env[ 'disable_components' ] = Get( 'config','disable_components',[] )
    env[ 'disable_users' ] =    Get( 'config','disable_users',[] )
    
    env['DOXYGEN'] =            Get( 'config', 'DOXYGEN', env.WhereIs('doxygen') )
    env['WARNINGS'] =           Get( 'config','WARNINGS', True )
    
        
    CXX = Get( 'config','CXX' )
    
    if CXX:
        env['CXX'] = CXX
        
    env[ 'PROGPREFIX' ] = "sf"
#    env[ 'OLDLIBPREFIX' ] = env.get('LIBPREFIX','')
#    env[ 'LIBPREFIX' ] = env[ 'OLDLIBPREFIX' ]+"slab_"
#    env.Append(LIBPREFIXES=[env[ 'OLDLIBPREFIX' ],env[ 'LIBPREFIX' ]])
         
    return

## Returns true if this tool exists  in the env \a env
# \return always True
def exists(env):
    """
    always True
    """
    return 1

