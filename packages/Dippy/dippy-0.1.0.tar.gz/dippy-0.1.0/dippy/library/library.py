
from dippy.util import get_only_positional

from dippy.dependency import Dependency, adapt, Fn

from interface import Interface
from component import Component

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

class Library_did_not_return_dict( Exception ): pass

# ------------------------------------------------------------------------------
# Library
# ------------------------------------------------------------------------------

class Library( Dependency ):
        
  def __init__( s, fn, interface = None, name__dependency = None ):

    if interface is None:
      interface = Interface( module = fn.__module__ )
    
    if name__dependency is None:
      name__dependency = {}
    
    s.__interface__ = interface
    s._fn = Fn( fn, name__dependency )
  
  # ------------------------------------
  # call
  # ------------------------------------

  def __call__( s, *a, **kw ):
    
    # component attr
    component_attr = s._fn( *a, **kw )

    # libraries expect the wrapped function to return a dict
    if not isinstance( component_attr, dict ):
      m = '%s returned %s' % ( s, component_attr )
      raise Library_did_not_return_dict( m )
          
    # create component
    return Component(
      s.__interface__,
      **component_attr
    )

# ------------------------------------------------------------------------------
# @lib
# ------------------------------------------------------------------------------

def lib( *positional, **name__dependency ):
  '''
  this is a decorator providing friendly syntax for library creation
  '''
  
  interface = get_only_positional( positional, optional = True )

  def fn__library( fn ):    
    return Library( 
      fn = fn,
      interface = interface,
      name__dependency = name__dependency,
    )
    
  return fn__library


# ------------------------------------------------------------------------------
# adapt registration
# ------------------------------------------------------------------------------

def adapt_library( env, library ):
  return adapt( env, library.__interface__ )
  
adapt.add( Library, adapt_library )

