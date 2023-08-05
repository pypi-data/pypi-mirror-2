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

from os.path import split,join,isfile
from sconfig.autotoolgen import ToolCreator


def do_missing_tool( env, ex_tool ):
    tool_name = split(ex_tool)[-1]
    if not (env.GetOption('clean') or env.GetOption('help') ):
        print  "    | Tool: '%s' (disabled)" %(tool_name)
    default_py = join( ex_tool,"default")
    default_py_d = {}
    tools_to_create = []
    if isfile(default_py):
        try:
            exec open(default_py) in default_py_d
            tools_to_create.extend( default_py_d.get('tools') )
        except:
            pass 
    if not tools_to_create:
        tools_to_create.append( tool_name )
        
    for tool_to_create in tools_to_create:
        print "Writing empty tool template for '%s', exists ... no" %(tool_to_create)
        tc = ToolCreator( tool_to_create, ex_tool )
        tc.CreateTool(env)
        
    
        
    

def do_missing_component( env, comp ):
    
    comp_name = split(comp)[-1]
    if not (env.GetOption('clean') or env.GetOption('help') ):
        print  "    | Component: '%s' (disabled)" %(comp_name)
    tool_dir = join( comp,"tools")
    default_py = join( tool_dir,"default")
    default_py_d = {}
    tools_to_create = []
    if isfile(default_py):
        try:
            exec open(default_py) in default_py_d
            tools_to_create.extend( default_py_d.get('tools') )
        except:
            pass 
    for tool_to_create in tools_to_create:
        print "Writing empty tool template for '%s', esists ... no" %(tool_to_create)
        tc = ToolCreator( tool_to_create, tool_dir )
        tc.CreateTool(env)


