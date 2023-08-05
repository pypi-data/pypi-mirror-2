
#ifndef _SLAB_CXX_FILE_HPP__
#define _SLAB_CXX_FILE_HPP__

#include <string>
#include <algorithm>
#include <vector>

#include <slab/cxx/environ.hpp>
#include <slab/cxx/DataTypeTraits.hpp>


namespace signal_lab
{

typedef  unsigned long long ulli;

namespace slabc{ 
#include <slab/file.h> 
#include <slab/header_utils.h> 
#include <slab/SLIO.h> 
//#include <slab/error.h> 
} // end namespace slabc

class slfile: public slabc::SLFileStruct
{
public:
	
	slfile( environ &env )
	{
		 slabc::slab_file_init( this, &env );
	}

	slfile( )
	{
//		 slabc::slab_file_init( this, &env );
	}
	
	
	virtual ~slfile( )
	{
		slabc::slab_file_delete(this);
	}
	
	void input( std::string name )
	{
		read_header( name );
		open_binary( );
	}


	
	slfile( const slabc::SLFileStruct &file )
	{
		fromfile( file );
	}
	
	void fromfile( const slabc::SLFileStruct &file )
	{
		this->is_input = file.is_input;
		this->fifo = file.fifo;
		this->pack = file.pack;
		this->finalized = file.finalized;
		
		this->header_stream = file.header_stream;
		this->binary_stream = file.binary_stream;
		
		this->env = slabc::slab_env_copy( file.env );
		
		this->header_values = slab_dict_copy( file.header_values );
		this->changed_header_values = slab_dict_copy( file.changed_header_values );
		
		this->history = (char*) malloc( strlen(file.history) );
		
		strcpy(this->open_mode, file.open_mode);
		strcpy(this->history,file.history);
		strcpy(this->header_name,file.header_name);
		strcpy(this->binary_name,file.binary_name);
		
	}
	void swap(  slfile& b )
	{
		std::swap( this->is_input, b.is_input ); 
		std::swap( this->fifo, b.fifo ); 
		std::swap( this->pack, b.pack ); 
		std::swap( this->finalized, b.finalized ); 

		std::swap( this->header_stream, b.header_stream ); 
		std::swap( this->binary_stream, b.binary_stream ); 

		std::swap( this->env, b.env ); 

		std::swap( this->header_values, b.header_values ); 
		std::swap( this->changed_header_values, b.changed_header_values ); 

		std::swap( this->history, b.history ); 
		
		std::swap(this->history,b.history);
		
		char open_mode[10];
		char header_name[FS_STRLEN];
		char binary_name[FS_STRLEN];

		strcpy(open_mode,   b.open_mode );
		strcpy(header_name, b.header_name );
		strcpy(binary_name, b.binary_name );

		strcpy(b.open_mode, this->open_mode );
		strcpy( b.header_name, this->header_name );
		strcpy(b.binary_name, this->binary_name );

		strcpy( this->open_mode, open_mode );
		strcpy( this->header_name,header_name );
		strcpy(this->binary_name, binary_name );
		
		return;
	}

	slfile& operator=( const slabc::SLFileStruct &file )
	{
		if(this != &file)
		{
			slfile other(file);
			this->swap( other );
		}
		return *this;
	}
	
	
	void read_header( std::string name )
	{
		if ( !slab_read_header_file( this, name.c_str() ) )
			throw slab_exception( );
	}
	
	void open_binary( )
	{
		if (!sl_open_binary_file(this))
			throw slab_exception( );
	}

	void close( )
	{
		slab_file_close( this );
	}
	
	template<class T>
	T get( std::string key, T* def=0 )
	{
		char* res = slabc::slab_file_get( this , key.c_str() );
		if (!res)
		{
			if (!def)
				throw slab_exception( );
			else
				return *def;
		}
		T result;
		StringConvert<T>::from_string(result,res);
		return result;

	}

	template<class T>
	void set( std::string key, T& value )
	{
		std::string val = StringConvert<T>::to_string(value);
		
		if (!slabc::slab_file_set( this , key.c_str(), val.c_str() ) )
				throw slab_exception( );
	}
	
	void finalize( )
	{
		if (!slabc::slab_finalize_output(this))
			throw slab_exception( );
	}
	
	
	int esize( )
	{
		int res = slabc::slab_file_esize( this );
		if (!res)
			throw slab_exception( );
		return res;
	}

	void set_esize( int esize_ )
	{
		int res = slabc::slab_file_set_esize( this, esize_ );
		if (!res)
			throw slab_exception( );
	}
	
	std::string dtype( )
	{
		char* res = slabc::slab_file_dtype( this );
		if (!res)
			throw slab_exception( );
		return res;
	}

	void  set_dtype( std::string dd )
	{
		int res = slabc::slab_file_set_dtype( this, dd.c_str() );
		if (!res)
			throw slab_exception( );
	}
	
	int ndim( )
	{
		int _ndim = slabc::slab_file_ndim( this );
		if (!_ndim)
			throw slab_exception( );
		return _ndim;
	}
	vector<ulli> dims()
	{
		int _ndim = ndim( );
		
		ulli* start = slabc::slab_file_dims( this );
		
		if (!start)
			throw slab_exception( );
			
		ulli* end = start+_ndim;
		
		vector<ulli> x( start, end );
		
		free(start);
		return x;
	}

	void set_dims( vector<ulli> vec )
	{
		ulli* _dims = slabc::slab_dims_create( vec.size() );
		
		for (unsigned int i=0;i<vec.size();i++)
			{ _dims[i] = vec[i]; }
		
		if (!slabc::slab_file_set_dims( this, _dims ))
			throw slab_exception( );
		
		return;
	}
	
	template<class datatype>
	bool istype( )
	{
		if ( DataTraits<datatype>::esize( ) != esize() )
			return false;
		if ( DataTraits<datatype>::type_name( ) != dtype() )
			return false;
		return true;
	}
	
	
	ulli left_size( int dim )
	{
		return slabc::slab_file_left_size( this , dim );
	}

	ulli right_size( int dim )
	{
		return slabc::slab_file_right_size( this , dim );
	}
	
	ulli size( )
	{
		return slabc::slab_file_left_size( this , 0 );
	}
	
	template<class datatype>
	void assert_type( )
	{
		if ( !this->istype<datatype>( ) )
		{
			  ostringstream oss;
			  oss << "slfile: Wrong datatype, need type '";
			  oss << DataTraits<datatype>::type_name( ) << "' got '";
			  oss << dtype().c_str();
			  oss << "' in file '" << get<std::string>("in").c_str() << "'" ;
			  
			throw Exception(oss.str( )); 
		}
	}
//	template<class T>
//	ulli read( )
//	{
//		slabc::slab_read( this, );
//	}
	
};

template<class datatype>
class sltypedfile: public slfile
{	
public:
	sltypedfile(  )
	{
		
	}

	
	sltypedfile( slfile &f )
	{
		f.assert_type<datatype>();
		
		this->fromfile( f );
	}

	void output( std::string name )
	{
		this->finalized = 0;
		this->is_input=0;
		
		if (!slabc::slab_file_output(this,name.c_str() ) )
			throw slab_exception( );
		
		this->set_esize( DataTraits<datatype>::esize( ) );
		this->set_dtype( DataTraits<datatype>::type_name( ) );
	}

	void output( const std::string name, const slfile &input, environ &env )
	{
		
		fromfile( input );
		this->env = env.copy();
		
		this->output( name );
	}

	ulli readinto( datatype* _buffer , ulli _size )
	{
//		ulli slab_read( SLFile slfile, char* buffer, ulli count )
		ulli nrd = slabc::slab_read( this, (char*) _buffer, _size * DataTraits<datatype>::esize( ) );
		
		if (slabc::slab_error_occured() )
			throw slab_exception( );
		
		return nrd;
	}

	ulli write( datatype* _buffer , ulli _size )
	{
		ulli nrd = slabc::slab_write( this, (char*) _buffer, _size * DataTraits<datatype>::esize( ) );
		
		if (slabc::slab_error_occured() )
			throw slab_exception( );
		
		return nrd;
	}

};
	

} // end namespace signal_lab


#endif // _SLAB_CXX_FILE_HPP__
