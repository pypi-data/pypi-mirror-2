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


class Store{};

template< class T>
class UniversalFunction< T, Store >
{
public:

	static bool check( Store& store )
	{
		return true;
	}


	static void run( Store& store )
	{

		string spacer;
		string dname = demangle( typeid(T).name() );
		string sfname = DataTraits<T>::type_name( );
		unsigned int size = dname.size();
		spacer = string( 29-size, ' ' );

		int esize = DataTraits<T>::esize( );

		cerr << " "  << dname  << spacer;

		spacer = string( 17-sfname.size(), ' ' );

		cerr << "| " << sfname << spacer;
		cerr << "| " << esize  << endl;
	}

	static void error( Store& store )
	{
		// no error
	}
};

}

using namespace signal_lab;
int main( int argc, char* argv[] )
{

//	typedef LastType<> LT;
//	cerr << typeid( LT::type ).name() << endl;
	cerr << "********************************************************\n";
	cerr << " Type                         | rsf name         | esize            \n";
	cerr << "--------------------------------------------------------\n";

	Store store;
	UniversalTypeRunner< Store >::run_all_types( store, false );

//	RUN_WITH_ALL_TYPES(Ty)

	cerr << "\n********************************************************\n";

}
