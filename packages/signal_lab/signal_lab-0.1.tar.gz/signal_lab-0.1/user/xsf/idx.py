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
import slabutils
import numpy

import sys


env=slab.Environment( )


args = env.args

rsfarray = slab.sl_file( args[0], env=env )

dtype = slabutils.get_dtype(rsfarray )
esize = rsfarray.esize

idx = int(args[1])

size = rsfarray.size
 
if idx < 0:
   idx = size + idx
elif idx >= size:
    raise IndexError( "The index is out of range. This file is lenght %i" %size )
    
if idx:
    rsfarray.binary.seek( esize * (idx) )
    

data = rsfarray.read( esize )

a = numpy.frombuffer( data, dtype=dtype )


print a[0] 