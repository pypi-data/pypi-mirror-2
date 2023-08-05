


from signal_lab import *

blocks_par = Parameter( 'blocks', (lambda args: tuple(eval(args)),'tuple'), help='topology to scatter files to' )
overlap_par = Parameter( 'overlap', (lambda args: tuple(eval(args)),'tuple'), help='overlap in each dimention' ,default="(0,)" )

user_arguments = [blocks_par,overlap_par]

#import pdb; pdb.set_trace()
env = Environment( sys.argv,
                            help=__doc__,
                            use_stdin=True,use_stdout=True,
                            user_arguments=user_arguments 
                            )


##print env.options
##
##raise SystemExit
#x = File( env.kw['x'], env=env )
#
#print env.options
#print env.kw
#print "args", env.args
#
##print x._header_keys
#
##print x._header_keys
#print "ndim", x.ndim
#print "shape", x.shape
#print "origin", x.origin
#print "step", x.step
#print "labels", x.labels
#print "units", x.units
#
#y = File( env.kw['y'], input=x ,datapath='.' )
#
#print y.is_input
#y.shape= [64,64]
#
#y.finalize(  )
#
#print >>sys.stderr, y.header
#print >>sys.stderr,  y.binary
#
