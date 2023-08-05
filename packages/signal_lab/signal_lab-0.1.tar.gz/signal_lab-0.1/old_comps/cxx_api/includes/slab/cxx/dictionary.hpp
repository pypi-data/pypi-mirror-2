
#include<string>

namespace signal_lab
{

namespace slabc
{
#include <slab/Dictionary.h>
} // end namespace file

class dict : public slabc::Dictionary
{
	public: 
	dict()
	{    
		this->flag  =0;
		this->pair = 0;
		this->dict_next = 0;
	}
	
	bool has_key( std::string key );
	
	template<class T >
	T get( std::string key, T def )
	{
		return slabc::slab_dict_get( (slabc::Dictionary)*this, key.c_str(), def );
	}
	
	
};

} // end namespace file
