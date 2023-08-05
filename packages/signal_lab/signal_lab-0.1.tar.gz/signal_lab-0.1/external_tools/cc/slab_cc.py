
"""
This Tool was automatically generated, do not edit!
"""


def generate( env ):
    env.Tool('slab_cc_option')
    SLABCCOPTS = env.get('SLABCCOPTS', None )
    
    if SLABCCOPTS == 'debug':
        env.Tool( 'slab_cc_debug' )
    if SLABCCOPTS == 'opt':
        env.Tool( 'slab_cc_opt' )

def exists( env ):
    return 1

