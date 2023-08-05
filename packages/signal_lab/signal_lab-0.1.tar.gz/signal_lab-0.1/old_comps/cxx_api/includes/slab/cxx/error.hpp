
#ifndef _SLAB_CXX_ERROR_HPP_
#define _SLAB_CXX_ERROR_HPP_
#include <exception> 
#include <string> 

namespace signal_lab
{

namespace slabc
{
#include <slab/error.h>
} // end namespace slabc

void clear_error( )
	{ slabc::slab_error_clear(); }

class slab_exception : public std::exception
{
public:
	std::string msg;
	slab_exception() throw( ) 
	{
		char *r = (char *) malloc( 1000 );
		sprintf( r, "SLAB error [%d]: %s, From file \"%s\", line %i\n", 
				slabc::SLAB_ERROR_STACK->slab_err,slabc::SLAB_ERROR_STACK->slab_err_msg,
				slabc::SLAB_ERROR_STACK->slab_err_file,slabc::SLAB_ERROR_STACK->slab_err_line);
		msg =r;

		clear_error( );
	}
	
	virtual ~slab_exception() throw( ){} 

	virtual const char* what( void ) const throw( )
	{
		return msg.c_str();
	}
	
	
};

class Exception : public std::exception
{
public:
	
	std::string msg;
	Exception( std::string _msg ) : msg(_msg)
	{  }
	
	virtual ~Exception() throw( ) {}
	virtual const char* what( void ) const throw( )
	{
		return msg.c_str();
	}
	
	
};

}

#endif //_SLAB_CXX_ERROR_HPP_

