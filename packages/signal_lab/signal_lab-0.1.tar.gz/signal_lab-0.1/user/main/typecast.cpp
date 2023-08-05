/*
  Copyright (C) 2008 The University of British Columbia

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

#include <signal_lab.hpp>

namespace signal_lab
{

//typedef TypeSet<int,complex<float>,complex<double> > typeset;
//typedef TypeSet< float > typeset;

class Store
{
public:
	InFileType in;
	string out_type_name;
	Store( InFileType& _in, string name ) :
		in(_in),
		out_type_name(name)
	{	}

};

template<class InType>
class Store2
{
public:
	InFile<InType> in;
	string out_type_name;
	Store2( InFile<InType>& _in, string  name ) :
		in(_in),
		out_type_name(name)
	{	}

	Store2( Store& store )
	{
		in = store.in;
		out_type_name =store.out_type_name;
	}

};

template< bool err, class FromType, class ToType>
class DoIfCanCast
{
public:
	static void run( Store2<FromType>& store )
	{

		OutFile<ToType> out( store.in, "out" );

		InputIterator<FromType> iiter( store.in );

		OutputIterator<ToType> oiter( out );

		while ( iiter.has_next() )
		{
			oiter.curr() = ScalarCast<FromType,ToType>::Cast( iiter.curr() );

			iiter.step();
			oiter.step();
		}
	}

	static bool check( Store2<FromType>& store )
	{
		return store.out_type_name == DataTraits<ToType>::type_name();
//		return TypeCheck<ToType>::is_type( store.in );
	}

};
template< class FromType, class ToType >
class DoIfCanCast<true,FromType, ToType>
{
public:
	static void run( Store2<FromType>& store )
	{

	}

	static bool check( Store2<FromType>& store )
	{
		return false;
	}
};

template< class T>
class UniversalFunction< T, Store >
{
public:
	typedef ScalarTraits< T > ST;
	typedef typename ST::magnitude magnitude;
	typedef ScalarTraits< magnitude > MT;

	static bool check( Store& store )
	{
		return store.in.is_type<T>();
	}

	static void run( Store& store )
	{
		typedef Store2<T> TypedStore;

		TypedStore tstore( store );

//		UniversalTypeRunner< TypedStore ,typeset >::run_all_types( tstore );
		UniversalTypeRunner< TypedStore  >::run_all_types( tstore );
	}

	static void error( Store& store )
	{
		cerr << sf_environ.prog() << ": can not run with given file type" << endl;
	}
};

template< class T1, class T2 >
class UniversalFunction< T1, Store2<T2> >
{
public:
	static bool check( Store2<T2>& store )
	{
		return DoIfCanCast< UpCast<T1,T2>::err, T2, T1 >::check( store );
	}

	static void run( Store2<T2>& store )
	{
		DoIfCanCast< UpCast<T1,T2>::err, T2, T1 >::run( store );
	}

	static void error( Store2<T2>& store )
	{
		cerr << sf_environ.prog() << ": can not convert to file type " << store.out_type_name << endl;
	}
};



}

using namespace signal_lab;

int main( int c, char** v )
{

	sf_init( c, v );

	InFileType file( "user/main/y.rsf" );
	string  name = sf_get( string, "totype" );

	Store store( file, name );

//	SLAB_COMPILE_WITH_TYPES( Store , store ,typeset );
	SLAB_COMPILE_WITH_ALL_TYPES( Store , store );
}


