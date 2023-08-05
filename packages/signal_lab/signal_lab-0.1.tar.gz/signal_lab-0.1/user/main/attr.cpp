/* Display dataset attributes.
   
Sample output from "sfspike n1=100 | sfbandpass fhi=60 | sfattr"
******************************************* 
rms = 0.992354 
mean value = 0.987576 
2-norm value = 9.92354 
variance = 0.00955481 
standard deviation = 0.0977487 
maximum value = 1.12735 at 97 
minimum value = 0.151392 at 100 
number of nonzero samples = 100 
total number of samples = 100 
******************************************* 

rms                = sqrt[ sum(data^2) / n ]
mean               = sum(data) / n
norm               = sum(abs(data)^lval)^(1/lval)
variance           = [ sum(data^2) - n*mean^2 ] / [ n-1 ]
standard deviation = sqrt [ variance ]
*/
/*
  Copyright (C) 2004 University of Texas at Austin
  
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
using namespace std;

template< class dtype, class otype >
void attr_printer( string want,
		int lval,
		ScalarType<dtype> rms,
	    ScalarType<dtype> mean,
	    ScalarType<dtype> norm,
	    ScalarType<dtype> var,
	    ScalarType<dtype> stddev,
	    
//	    ScalarType<dtype> max,
//	    ScalarType<dtype> min,
	    ScalarType<otype> nnz,
	    ScalarType<otype> size
	    )
			  
{
	bool all = want == "all";
    if(all)
    {
    	cerr << "******************************************* \n";
//    	if( rms.is_complex )
//    		cerr << "   rms, mean, norm, var, and std refer to amplitude\n\n";
    }
    if( all || want == "rms")
    	cerr << "rms = " << rms << endl;
    if( all || want == "mean" )
    	cerr << "mean value = "<<  mean << endl;
    if( all || want == "norm")
    	cerr << lval << "-norm value = " << norm << endl;
    if( all || want == "var")
    	cerr << "variance = " << var << endl;
    if( all || want == "std" )
    	cerr << "standard deviation = " << stddev << endl;
    if( all || want == "nonzero" )
    	cerr << "number of nonzero samples = " << nnz << endl ;
    if( all || want ==  "samples")
    	cerr << "total number of samples = " << size << endl;
    if( all ) 
    {
    	cerr << "******************************************* \n" ;
    }



}



template< class dtype >
void iterate( InFile< dtype > in , string want, int lval )
{
	typedef ScalarTraits<dtype> ST;
	typedef typename ST::magnitude magnitude;
	typedef ScalarType<dtype> Scalar;
	typedef ScalarType<int> Ordinal;
	typedef ScalarTraits<magnitude> MT;
	typedef ScalarType<magnitude> Magnitude;
	
	
	magnitude zero= MT::zero();
	magnitude msum=zero, msqr=zero, mnorm=zero;
	
	int nsiz, nzero=0;
	
	nsiz = in.leftsize();
	
	InputIterator<dtype> iter( in );
	while ( iter.has_next() )
	{
		magnitude m = ST::Abs( iter.curr() );
		
		MT::Inc( msum, m );
		MT::Inc( msqr , MT::Pow(m,2) );
		MT::Inc( mnorm, MT::Pow( m, lval ) );
		
		if ( !MT::Eq( m, zero ) ) // f != 0
	    	nzero++;
	    
		iter.step();
	}
	
	/**
	 * ####################################
	 * End Iterations, Begin math
	 * #################################### 
	 */
	
	// Define abstract scalar classes
	Magnitude mean, rms, var, stddev;
//	Scalar max,min;
	Magnitude norm =mnorm;
	Magnitude sum = msum;
	Magnitude sqr = msqr;
	
	Ordinal nnz= nzero;
	Ordinal size =nsiz ;
	
	Magnitude one = MT::one();

	mean = sum/size;
    
    if ( lval == 0 ) 
    	norm = (size - nnz);
    else              
    	norm = Pow<magnitude>( norm, 1. / lval );
    
    rms = Sqrt<magnitude>( sqr / size  );
    
    if ( size > 1 ) 
    {
    	Magnitude m2 = Pow<magnitude>(mean,2);
    	var = ( sqr-size*mean*mean )/( size-one );
    }
    else          
    	var = zero;
    
    stddev = Sqrt<magnitude>( var );
    
	/**
	 * ####################################
	 * Print Result
	 * #################################### 
	 */
    attr_printer<magnitude, int>( want,lval, rms, mean, norm, var, stddev, /*max,min*/ nnz, size);
}


	/* 'all'(default),'rms','mean','norm','var','std','max','min','nonzero','samples','short' 
        want=   'rms' displays the root mean square
        want=   'norm' displays the square norm, otherwise specified by lval.
        want=   'var' displays the variance
        want=   'std' displays the standard deviation
        want=   'nonzero' displays number of nonzero samples
        want=   'samples' displays total number of samples
        want=   'short' displays a short one-line version
     */ 



int main(int argc, char* argv[])
{
    InFileType in;
    int lval;
    string want;
    
    
    sf_init (argc,argv);
    
	want = sf_getdefault(string, "want", "all" );
    
	lval = sf_getdefault( int, "lval", 2 );
	
 
    in = InFileType("user/main/y.rsf");
    
    if ( in.is_type< float>() )
    {
    	InFile<float> fin = in; 
    	iterate<float>( fin , want , lval );
    }
    else if ( in.is_type< complex<float> >( ) )
    {
    	InFile< complex<float> > fin = in; 
    	iterate<complex<float> >( fin , want , lval );
    }
    

}
