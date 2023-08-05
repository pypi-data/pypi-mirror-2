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

from sconfig import *
from SCons.Script import Help
from os.path import dirname as _dname, join as _join


Help("""
+--------------------------------------------------------+
+  Signal Processing Lab (SLAB)                          +
+  Version - 0.0.0.0.0.0.0.0.0.0.0.1                     +
+  Copyright 2008 Gilles Hennenfent & Sean Ross-Ross     +
+--------------------------------------------------------+

""")
 


from SLABConfigureStd import AddSLABOptions
from SLABConfigureStd import AddSLABVariables
from SLABConfigureStd import standard_component_config
#from SLABConfigureStd import standard_tools_config
#from SLABConfigureStd import LoadConfigFile
from SLABConfigureStd import CommandLineToolPath
from SLABConfigureStd import StdInstall

from SLABBuildStd import Install_Tools
from SLABBuildStd import SLABBuild_components
from SLABBuildStd import SLABBuild_user

_this_path = _dname(__file__)
slab_toolpath = _join( _this_path, 'slab_tools' )

add_to_default_toolpath(slab_toolpath)
add_to_default_tools( 'sfcore' )


