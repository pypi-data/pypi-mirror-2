#  Copyright (C) 2008 Gilles Hennenfent and Sean Ross-Ross
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

from slab import *
from slabutils import get_dtype

from numpy import empty,prod
#from sys import argv

e = Environment( )


#clip = float( e.kw['clip'] )
i = sl_file(  'f.rsf', env=e )
#o = sl_file(  'out', input=i, env=e )
#
#o.finalize( )
#
#n1 = i.shape[:1]
#nleft = i.shape[1:]
#a = empty( n1, dtype=get_dtype(i) )
#
#for right in range( prod(nleft) ):
#    
#    i.readinto( a.data )
#    
#    b = a.clip(min=-clip,max=clip)
#
#    o.write( b.data )


