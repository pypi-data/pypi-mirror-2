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

import slab

env = slab.Environment( )

if env.kw.has_key('nodefile'):
    nodefile = env.kw['nodefile']
    nodelist = open(nodefile).readlines( )
else:
    nodelist = env.args[:]

datapath = env.kw['datapath']
for node in nodelist:
    pass

out = slab.sl_file( 'out' , intput=False, env=env )

binary_name = out.binary_name

binary_name+"_create_"



