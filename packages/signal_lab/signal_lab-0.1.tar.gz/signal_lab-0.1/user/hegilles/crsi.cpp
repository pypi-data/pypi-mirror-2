

#include <slim.hpp>
#include <slim/algorithms.hpp>
#include <slim/curvelab.hpp>
#include <slim/curvelab/rsf.hpp>

#include <iostream>


using namespace slim;
using namespace slim::test;
using namespace slim::traits;
using namespace slim::LinearOperators;
using namespace slim::algorithms;


typedef rsf::VectorUtils<CpxNumMat> 		RU;   // rsf utilities

typedef DiagonalWeight<CpxNumMat > 		 	Diag; // Diagonal weight operator
typedef traits::LinearOperator< ifdct2 >  			IT;   // Profiler for ifdct2
typedef traits::LinearOperator< Diag > 	 			OTP;  // Profiler for Diag
typedef CompoundOperator< Diag, ifdct2 > 	Compound; // Compound Operator


int main( int argc, char** argv )
{

	typedef traits::LinearOperator<Compound> 			OT;   // Profiler for Comp
	typedef OT::DVT 							DVT;  // Domain Vector Traits
	typedef OT::RVT 							RVT;  // Range Vector Traits

	typedef Thresh< OT::domain_type, DVT >     	Threshold; // Threshold type
	typedef LogCooling< OT::domain_type, DVT >  LogCoolingCL; // Log cooling class for cell array
	typedef landweber< Compound, LogCoolingCL , OT > Landweber; // landweber class


  /* Input and output files */
  sf_file in, out,fmask;

  /* Initialize RSF */
  sf_init(argc,argv);

  /* standard input */
  in = sf_input("in");

  fmask = sf_input("mask");

  /* standard output */
  out = sf_output("out");

  int n[SF_MAX_DIM];
  int n1,n2;
  sf_filedims( in, n );
  n1 = n[0];
  n2 = n[1];

  // Define Variables
  float lmax,lmin;
  int nout, nin;
  int dot;
  int num_slices, mask_slices;

  // Get command line ops
  if ( !sf_getfloat( "lmax" , &lmax ) )  lmax=0.01;
  if ( !sf_getfloat( "lmin" , &lmin ) )  lmin=0.99;

  if ( !sf_getint( "nout" , &nout ) ) nout=1;
  if ( !sf_getint( "nin" , &nin ) ) nin=1;

  if ( !sf_getint( "dottest" , &dot) ) dot=0;

  // Define Vectors
  CpxNumMat array(n1,n2);
  CpxNumMat mask(n1,n2);

  OT::domain_type cell;
  OT::domain_type x0;

  // Read in to input
  num_slices = RU::ReadInto( in, array );
  mask_slices = RU::ReadInto( fmask, mask );

  AssertEqual(  mask_slices , num_slices );


  // Make Logging class
  MyLog& log = MyLog::get_instance();
  log.time_it(  );

  cerr << "Starting solver, looping over dims > 2" << endl;
  cerr << "......................................" << endl;
  while ( num_slices-- )
  {
	  cerr << "++solving for slice "<< mask_slices - num_slices<< endl;
	  cerr << "----------------------- "<< mask_slices - num_slices<< endl;
	  // Create Diagonal Weighting operator
	  Diag diag( mask );

	  // Create 2d curvelet Operator
	  ifdct2 A( array.m(), array.n(), 4, 16, 1 );

	  // Create Compound of Diagonal and Curvelet
	  Compound C( diag, A );

	  // Dot testing
	  if( dot )
	  {
		  cerr << "Dottest" << endl;
		  DotTester< Compound > tester( & C );
		  tester.test( );
		  cerr << endl;
		  return 0;
	  }

	  // zero x0 (and make its shape to cell array)
	  OT::DomainZeros( C, x0 );

	  // get the coefs for thresh to sort
	  IT::ApplyAdj( A, array, cell );

	  // create threshold object
	  LogCoolingCL thresh( lmax, lmin,  nout ,nin,cell );

	  // create solver object
	  Landweber lsolver( nout, nin, thresh );

	  // solve problem
	  lsolver.solve( C, array , x0 );

	  // bring result back to data domain
	  IT::Apply( A, x0, array );


	  // write the result
	  RU::WriteFrom( array, out );

	  if (num_slices)
	  {
		  // write the result
		  RU::ReadInto( in, array );
		  RU::ReadInto( fmask, mask );
	  }

  }
  // end the timer
  log.done( "landweber" );
  // print statistics
  log.print_ops();
}

