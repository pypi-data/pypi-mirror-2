
#ifndef _SLAB_CXX_ENVIRON_HPP__
#define _SLAB_CXX_ENVIRON_HPP__

#include<string>

#include<slab/cxx/error.hpp>
#include<slab/cxx/string_converter.hpp>

namespace signal_lab
{

namespace slabc
{
#include <slab/environment.h>
} // end namespace slabc

class environ: public slabc::SLEnvironment
{
public:
	environ( )
	{
		slabc::slab_env_init_( this );
	}

	environ( slabc::SLEnvironment &env )
	{
		this->options =  slabc::slab_dict_copy(env.options);
		this->kw  = slabc::slab_dict_copy(env.kw);
		this->par = slabc::CopyStringList(env.par);
	}
	
	
	environ& operator=( const slabc::SLEnvironment &env )
	{
		if(this != &env)
		{
			this->options =  slabc::slab_dict_copy(env.options);
			this->kw  = slabc::slab_dict_copy(env.kw);
			this->par = slabc::CopyStringList(env.par);
		}
		return *this;
	}
	
	void init( int argc, char** argv, slabc::OptionsList lopts )
	{
		slab_environ_init( this, argc, argv, lopts );
	}
	
	template<class T>
	T get( std::string key, T* def=0 )
	{
		char* res = slabc::slab_env_get( this , key.c_str() );
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
	T get_opt( std::string key, T* def=0 )
	{
		char* res = slabc::slab_env_get_opt( this , key.c_str() );
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
	
	slabc::SLEnvironment* copy( )
	{
		
		return slabc::slab_env_copy( this );
	}

//	template<class T>
//	T get_opt( std::string key, T* def=0 )
//	{
//		char* res = slabc::slab_env_get_opt( this , key.c_str() );
//		if (!res)
//		{
//			if (!def)
//				throw slab_exception( );
//			else
//				return *def;
//		}
//		T result;
//		StringConvert<T>::from_string(result,res);
//		return result;
//	}
//

};

} // end namespace file

#endif // _SLAB_CXX_ENVIRON_HPP__