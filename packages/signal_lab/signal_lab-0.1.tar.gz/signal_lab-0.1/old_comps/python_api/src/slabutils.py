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

from numpy import dtype,empty,memmap

def get_dtype( slfile ):
    
    typename = _type_map[slfile.type][slfile.esize]
    return dtype(typename)
    

def toarray( slfile ):
    
    shape = list(slfile.shape)
    
    while shape[-1] == 1:
        shape.pop() 
            
    dtype=get_dtype( slfile )
    
    arry = empty( shape, dtype=dtype , order='F' )
    slfile.readinto( arry.data )
    return arry

def to_memmap( slfile ):
    
    xin = slfile['in']
    xdtype = get_dtype( slfile )
    xshape = slfile.shape
    
    
    if slfile.is_input:
        mode='r'
    else:
        mode='w'
            
    return memmap(xin,dtype=xdtype, mode=mode,shape=xshape, order='F' ) 
    
    
    
    