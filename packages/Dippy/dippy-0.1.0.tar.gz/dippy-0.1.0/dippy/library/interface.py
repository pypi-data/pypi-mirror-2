
from dippy.dependency import Dependency, adapt

from name import input__names

# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------

class Interface( Dependency ):

  def __init__( s, names = frozenset(), module = None ):
    s._expected_names = input__names( names )  
    s._module = module

  # ------------------------------------
  # __str__
  # ------------------------------------
  
  def __str__( s ):
    
    string = 'names = [ %s ]' % ', '.join( s._expected_names )
    
    if s._module:
      string += ', module = %s' % s._module
    
    return 'Interface( %s )' % string

# ------------------------------------------------------------------------------
# assert_fulfills
# ------------------------------------------------------------------------------

class Interface_not_fulfilled( Exception ): pass

def assert_fulfills( name__attr, interface ):
  provided_names = frozenset( name__attr.keys() )
  
  for expected in interface._expected_names:
    if expected not in provided_names:
      m = '"%(expected)s" name is expected by %(interface)s, only %(provided_names)s were provided' % dict(
        expected = expected,
        provided_names = provided_names,
        interface = interface,
      )      
      raise Interface_not_fulfilled( m )

# ------------------------------------------------------------------------------
# fulfills
# ------------------------------------------------------------------------------
  
def fulfills( *a, **kw ):
  try:
    assert_fulfills( *a, **kw )
    return True
  
  except Interface_not_fulfilled:
    return False

# ------------------------------------------------------------------------------
# adapt registration
# ------------------------------------------------------------------------------

def adapt_interface( env, interface ):
  return env.interface__component( interface )

# --------------------------------------

adapt.add( Interface, adapt_interface )
