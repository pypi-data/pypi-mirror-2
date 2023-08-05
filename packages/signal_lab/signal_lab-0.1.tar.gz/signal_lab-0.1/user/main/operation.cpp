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

int main( int c, char** v )
{



	sf_init( c, v );

	InFileType file( "in" );

	InFile<float,double> in = file;

	OutFile<double> out( in, "out" );

	int n1 = in.sf_hist<int>( "n1" );

	int n2 = in.leftsize(1);

	double *trace = sf_alloc( double , n1 );


	float clip = sf_get( double , "clip" );

    /* loop over traces */
    for ( int i2=0; i2 < n2; i2++ )
    {

		/*read a trace */
		in.read( trace, n1 );

		/* loop over samples */
		for (int i1=0; i1 < n1; i1++) {
		    if      (trace[i1] >  clip) trace[i1]= clip;
		    else if (trace[i1] < -clip) trace[i1]=-clip;
		}

		/* write a trace */
		out.write( trace, n1 );
    }

}


