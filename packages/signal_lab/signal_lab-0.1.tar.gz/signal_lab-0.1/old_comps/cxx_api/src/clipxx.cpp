

#include <signal_lab2.hpp>
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
		
	signal_lab::environ env = *signal_lab::slabc::slab_env_init(argc,argv);

	float clip = env.get<float>("clip");
	
	cout <<"clip=" << clip << endl;
	
	
	signal_lab::slfile file(env);
	file.input( "f.rsf" );
	
	cout << "n1 = "<< file.get<int>( "n1" ) << endl;
	
	signal_lab::sltypedfile<float> in( file );
	
	signal_lab::sltypedfile<double> out;
	out.output( "f2.rsf", in, env);
	
	out.finalize( );

	float f;
	double d;
	in.readinto( &f, 1 );
	
	d =f ;
	out.write( &d, 1 );
	
	cout << "f = '" << f << "'" << endl;
	return 1;
}

