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

using namespace signal_lab;

namespace signal_lab
{


class Store
{
public:
	InFileType& in;
	Store( InFileType& _in ) : in(_in) { }
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
//		return true;
	}


	static void run( Store& store )
	{

		InFile<T> in = store.in;

		InputIterator<T> iter( in );

		unsigned long int endline=1;

		cerr << endl;
		cerr << "type="<<typeid(T).name() << ":" << endl ;
		cerr << endl << "0:    ";
		while ( iter.has_next() )
		{
			cerr << iter.curr() << " ";
			iter.step();

			if (endline%5==0)
				cerr << endl << endline <<":    ";
			endline++;
		}
	}


	static void error( Store& store )
	{
		cerr << sf_environ.prog() << ": can not run with given file type:" << store.in["type"] << endl;
		// no error
	}
};

}

int main( int c, char** v )
{

	sf_init( c, v );

	InFileType file( "in" );

	Store store( file );


//	typedef TypeSet<int,float, double> typeset;
	SLAB_COMPILE_WITH_ALL_TYPES( Store , store );

//	UniversalTypeRunner< Store, TypeSet<float> >::run_all_types( store );

}


