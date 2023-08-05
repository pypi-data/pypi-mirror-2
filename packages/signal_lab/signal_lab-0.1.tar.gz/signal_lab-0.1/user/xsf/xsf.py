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
This is the main
"""
from subprocess import Popen, PIPE
from threading import Thread
from xml.dom.minidom import parse
import  numpy
import re 
import sys


class Worker( Thread ):
    """
    Thread to run commands
    """
    def __init__( self, rank, nodename, command ,verbose=False ):
        self.rank = rank
        self.nodename = nodename
        self.command = command
        self.err = 0
        self.verbose = verbose
        Thread.__init__( self, name="%s:%s" %(rank, nodename) )
        
    def run( self ):
        if self.verbose: print >> sys.stderr, "%(nodename)s,%(rank)s:" %(self.__dict__),  self.command 
        p0 = Popen( self.command , shell=True )
        self.err = p0.wait( )


class Xfile( object ):
    
    _data_dict = {}
    local_files = {}
    def __init__( self, filename ):
        if type(filename) is str:
            file = open( filename )
        else:
            file = filename
            
        for line in file:
                if "=" in line:
                    key,value = line.split("=",1)
                    key = key.strip().strip("\'\"")
                    value= value.strip()
                    try:
                        newvalue = eval(value)
                    except:
                        newvalue = value
                    self._data_dict[key] = newvalue
    
    def __getitem__( self, item ):
        return self._data_dict[item]
    
    def form( self ):
        pars = []
        for key,value in self._data_dict.iteritems():
            if key in ['in']:
                pass
            else:
                pars.append( "%s=%s" %(key,value) )
        return pars
        
    def readXML(self):

        dom = parse( self._data_dict['in'] )
        for sub_header in dom.firstChild.getElementsByTagName( 'sub_header' ):
            rf = RFile( )
            rf.fill( sub_header )
            self.local_files[rf.comm_world_rank] = rf
        return
    
    def toXML(self ):
        pass
    
    def get_rank_map(self):
        rmap = {}
        for rfile in self.local_files.itervalues():
            map = rmap.setdefault(rfile.comm_world_rank, {} )
            map['comm_private_rank'] = rfile.comm_private_rank
#            map['filename'] = rfile.comm_private_rank
            map['nodename'] = rfile.nodename
        return rmap 
    

def all_same( somthings ):
    
    initial = somthings[0]
    for thing in somthings:
        if initial != thing: return False
    return True
        
    
def assert_even_dist( xfiles ):
    """
    makes sure that the files are on an distributed the same
    """
    if not all_same( [ len( loc ) for loc in  xfiles.local_files ]):
        raise Exception( "differet distibution patterns exist within meta headers" )
    
        
    
    
class RFile( object ):
    comm_world_rank = None
    comm_private_rank = None
    nodename = None
    filename = None
    _data_dict = { }
    
    def fill(self, sub_header):
        
        cwr = sub_header.getAttribute('comm_world_rank')
        self.comm_world_rank = int(cwr)
        
        filename= sub_header.getElementsByTagName('filename')[0]
        self.filename = filename.firstChild.wholeText

        nodename= sub_header.getElementsByTagName('nodename')[0]
        self.nodename = nodename.firstChild.wholeText

        comm_private_rank= sub_header.getElementsByTagName('comm_private_rank')[0]
        self.comm_private_rank = int(comm_private_rank.firstChild.wholeText)
        
        simtab = sub_header.getElementsByTagName('simtab')[0]
        for element in simtab.childNodes:
            if not hasattr( element, 'tagName' ):
                continue
            key = element.tagName
            value = element.firstChild.wholeText
            self._data_dict[key] = value
    
    def __repr__(self):
        return ("RFile( comm_world_rank=%(comm_world_rank)s, "
               "comm_private_rank=%(comm_private_rank)s, "
               "nodename=%(nodename)r, "
               "filename=%(filename)r )" %self.__dict__) 
    
    
    
    