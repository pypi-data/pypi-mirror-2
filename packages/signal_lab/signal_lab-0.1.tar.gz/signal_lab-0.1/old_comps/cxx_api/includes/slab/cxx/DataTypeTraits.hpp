/*
  Copyright (C) 2008 Gilles Hennenfent and Sean Ross-Ross

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

/*! Classes to define behavior of any types
 *
 * \addtogroup core_comp_gp
 * @{
 */

#ifndef _SLAB_DATA_TYPE_TRAITS_HPP
#define _SLAB_DATA_TYPE_TRAITS_HPP

#include <iostream>


namespace signal_lab
{

	//! c++ Traits class defines operations on data
	/*!
	 * \tparam datatype type to operate on
	 * \note This is a static class ment to be specialized for
	 * non-standard data types.
	 */
	template< class datatype >
	class DataTraits
	{
	public:
		//! Returns the size of each element
		static int esize( )
		{
			return sizeof( datatype );
		}

		//! Name of data
		static string type_name( )
		{
			return typeid(datatype).name();
		}


	};

	template<  >
	class DataTraits<double>
	{
	public:
		//! Returns the size of each element
		static int esize( )
		{ return sizeof( double ); }

		//! Name of data
		static string type_name( )
		{
			return "double";
		}
	};
	
	template<  >
	class DataTraits<float>
	{
	public:
		//! Returns the size of each element
		static int esize( )
		{ return sizeof( float ); }

		//! Name of data
		static string type_name( )
		{
			return "float";
		}
	};

	template<  >
	class DataTraits<int>
	{
	public:
		//! Returns the size of each element
		static int esize( )
		{ return sizeof( int ); }

		//! Name of data
		static string type_name( )
		{
			return "int";
		}
	};
	

	template<  >
	class DataTraits<complex<float>>
	{
	public:
		//! Returns the size of each element
		static int esize( )
		{ return sizeof( complex<float> ); }

		//! Name of data
		static string type_name( )
		{
			return "complex";
		}
	};
	
	
	

}


#endif // _SLAB_DATA_TYPE_TRAITS_HPP

