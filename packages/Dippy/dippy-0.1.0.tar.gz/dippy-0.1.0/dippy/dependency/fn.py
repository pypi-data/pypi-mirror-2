
from dippy.util import get_only_positional

from adapt import adapt

# ------------------------------------------------------------------------------
# depend
# ------------------------------------------------------------------------------

def depend( **name__dependency ):
  def wrap( fn ):
    return Fn( fn = fn, name__dependency = name__dependency )
  return wrap

# ------------------------------------------------------------------------------
# Fn
# ------------------------------------------------------------------------------

class Fn( object ):
  
  def __init__( s, fn, name__dependency ):
    
    assert not isinstance( fn, Fn ), 'double wrapping a Fn is not allowed, because it is probably an accident'
    
    s._fn = fn
    s._name__dependency = name__dependency
  
  def __call__( s, *positional, **name__input ):

    env = get_only_positional( positional, optional = True )

    if env:
      add_missing_inputs( name__input, s._name__dependency, env )

    return s._fn( **name__input )

# ------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------
 
def add_missing_inputs( name__input, name__dependency, env ):
  for name, dependency in name__dependency.iteritems():
    if name in name__input:
      continue
    
    input = adapt( env, dependency )
    name__input[ name ] = input

