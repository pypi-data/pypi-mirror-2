
import os
import new
from xml.dom.minidom import parse,parseString
from xml.dom.minidom import Document
import xml.dom.minidom as minidom

import signal_lab as slab

def CreateBlankDocument( env, mpisize, slfile ):
    
    doc = Document( )
    root = doc.createElement( "RSF" )
    doc.appendChild(root)
    
    for i in range( mpisize ):
        sub_header = doc.createElement( "sub_header" )
        
        sub_header.setAttribute('comm_world_rank', str(i) )
        efilename = doc.createElement( "filename" )
        
        efilename.appendChild(doc.createTextNode("mpi%03i_%s.rsf" %(i,slfile.basename)))
        
        esimtab = doc.createElement( "simtab" )
        
        for key,value in slfile._header_keys.items():
            ekey = doc.createElement( key )
            ekey.appendChild( doc.createTextNode( str(value) ) )
            esimtab.appendChild( ekey )
        
        sub_header.appendChild(efilename)
        sub_header.appendChild(esimtab)
        
        root.appendChild(sub_header)
        
    
    return doc


def sFile( comm, tag, env=None, input=True, **options ):
    
    if comm.rank() == 0:
        return slab.File( tag, env=env, input=input, **options  )
    else:
        return None
    
class DistributedFile( slab.File ):
    
    def __init__(self, comm, tag, env=None, input=True, **options ):
        
        self.comm = comm
        
        if self.comm:
            mpirank = self.comm.rank(  )
            mpisize = self.comm.size(  )
        else:
            mpirank =0
            mpisize =1
        
        
        if mpirank == 0:
            options['pack']=True
            slab.File.__init__( self, tag, input=input, env=env, **options )
            
            comm = self.comm
            if comm:
                self.comm = None
                
                comm.bcast( self.serialize(), 0 )
                
                self.comm = comm
        else:
            comm = self.comm
            if comm:
                self.unserialize( comm.bcast( None, 0 ) )
                self.comm = comm            
        
        self.mpirank = mpirank
        self.mpisize = mpisize
        
        if self.is_input:
            self.mpi_init_input( )
        else:
            self.mpi_init_output( input )
            
            
#    def mpi_init_input( self ):
#        
#        rank = self.comm.rank(  )
#        
#        if rank == 0:
#            if self.type != 'xml':
#                raise Exception("DistributedFile requires data type to be 'xml' not '%s' " %self.type )
#            
#            self.xmldom = parse( self.binary_file )
#            
#            for sub_header in self.xmldom.firstChild.getElementsByTagName( 'sub_header' ):
#                cwr = int(sub_header.getAttribute('comm_world_rank'))
#                comm_private_rank = int(sub_header.getElementsByTagName('comm_private_rank')[0])
#                filename = sub_header.getElementsByTagName('filename')[0].firstChild.wholeText
#                
#                if cwr != rank: 
#                    mpi.send( comm_private_rank, cwr ,0, self.comm )
#                    mpi.send( filename, cwr ,0, self.comm )
#                else:
#                    self.comm_private_rank = comm_private_rank
#                    self.filename = filename
#                    
#        else:
#            self.meta_slfile = None
#            self.xmldom
#            self.comm_private_rank = mpi.receive( 0 ,0, self.comm )
#            self.filename = mpi.receive( 0 ,0, self.comm )
#        
#        
#        self.private_comm = mpi.comm_split( self.comm, 0, self.comm_private_rank )
#        self.local = File( filename, input=True, env=env )
    
    def mpi_init_output(self, input=None ):
        
        if isinstance(input,DistributedFile):
            self.input_type = "xsf_input"
        else:
            self.input_type = "rsf_input"

        self._input = input
        if self.input_type == 'xsf_input':
            #self.mpi_init_xsf_output(input)
            self._local_input = input.local
            self.xmldom = parseString( input.xmldom.toxml() )
        else:
            
            if input == False:
                self._local_input = False
            else:
                
                if self.comm:
                    self._local_input = slab.File.__new__( slab.File ) 
                    
                    if self.mpirank ==0:
                        self._local_input.unserialize( self.comm.bcast( input.serialize( ) , 0) )
                    else:
                        self._local_input.unserialize( self.comm.bcast( None , 0 ) )
                else:
                    self._local_input = input
            
                
                    
            self.type = 'xml'
            self.esize = 1
    
    def finalize_metaheader( self ):
        
        slab.File.finalize( self )
        
        opts = self.env.options
        
        localtmpdir = opts.get( 'localtmpdir',opts.get('datapath','/tmp') )
        
        
        local_fname = os.path.join(localtmpdir,self.header_filebase + ".%03i.rsf"%self.mpirank ) 
        
        
        pack = True
        fifo = False
#        fifo = self.header == 'file:sys.stdout' or not is_reg
            
        self.local = slab.File( local_fname, env=self.env, input=self._local_input, pack=pack, fifo=fifo )
        
        if self.input_type == 'rsf_input':
            if self._local_input is False:
                self.xmldom = CreateBlankDocument( self.env, self.mpisize, self )
            else:
                self.xmldom = CreateBlankDocument( self.env, self.mpisize, self._local_input )
            
        return self
        
    
    def dom_get_sub_header(self,rank):
        esub_headers =  self.xmldom.firstChild.getElementsByTagName( 'sub_header' )
        
        for sub_header in esub_headers:
            cwr = int(sub_header.getAttribute('comm_world_rank'))
            if cwr == rank:
                return sub_header
        raise Exception("no sub_header with rank='%s'" %rank ) 

    def dom_get_sub_header_fname(self,rank):

        sub_header = self.dom_get_sub_header(rank)
        return sub_header.getElementsByTagName('filename')[0].firstChild.wholeText        
    
    
    def finalize( self ):
        
        self.local.finalize( )
        
        if self.mpirank == 0:
            
            self.update_dom( self.local._header_keys, 0,filename=self.local.header_abspath)
            
            #print "self.local._header_keys",self.local._header_keys
            
            for i in range( 1, self.mpisize ):
                
                hkeys = self.comm.recv( i, 0 )
                
                self.update_dom(hkeys, i,filename=self.local.header_abspath )
            
                
            self.xmldom.writexml( self.binary_file, indent='  ', addindent='  ', newl='\n' )
            self.binary_file.close( )
        else:
            
            
            self.comm.send( self.local._header_keys, 0, 0 )
        
        
        
    def update_dom(self,hkeys,rank,filename=None):
        esub_header = self.dom_get_sub_header( rank )
        
        if filename is not None:
            efilename = esub_header.getElementsByTagName( 'filename' )[0]
            esub_header.removeChild( efilename )
            
            efilename = self.xmldom.createElement( "filename" )
            efilename.appendChild( self.xmldom.createTextNode( filename ) )
            esub_header.appendChild( efilename )
            
        esimtab = esub_header.getElementsByTagName( 'simtab' )[0]
        
        esub_header.removeChild( esimtab )
        esimtab = self.xmldom.createElement( 'simtab' )
        esub_header.appendChild( esimtab )
        
        for key,value in hkeys.items():
            ekey = self.xmldom.createElement( key )
            ekey.appendChild( self.xmldom.createTextNode( str(value) ) )
            esimtab.appendChild( ekey )
        return 
    
