
from dippy.dependency import adapt
from dippy.library import Component, Library

# ------------------------------------------------------------------------------
# Env
# ------------------------------------------------------------------------------

class Env( object ):

  def __init__( s, interface__component ):
    s._interface__component = interface__component  # ideally cast to a frozendict

  # ------------------------------------
  # adapt
  # ------------------------------------
  
  def __call__( s, dependency ):
    '''
    component = env( dependency )
    
    is syntactic sugar for
    
    component = adapt( env, dependency )
    '''
    
    return adapt( s, dependency )
  
  # ------------------------------------
  # helpers
  # ------------------------------------
  
  @property
  def components( s ):
    return set(
      s._interface__component.values()
    )
  
  def __contains__( s, interface ):    
    return interface in s._interface__component
    
  # ------------------------------------
  # interface__component
  # ------------------------------------
  
  class Missing_interface( Exception ): pass
    
  def interface__component( s, interface ):

    if interface not in s._interface__component:
      m = '%(interface)s not in %(env)s' % dict(
        interface = interface,
        env = s,
      )
        
      raise s.Missing_interface( m )
    
    return s._interface__component[ interface ]
  
  # ------------------------------------
  # conflict
  # ------------------------------------
  
  class Interface_conflict( Exception ): pass
  
  def _conflict_check( s, interface ):
    if interface in s:
      m = 'env conflict for %s' % interface 
      raise s.Interface_conflict( m )

  # ------------------------------------
  # add
  # ------------------------------------

  def __add__( s, x ):
    if isinstance( x, Component ):
      return s._add_component( x )
    elif isinstance( x, Library ):
      return s._add_library( x )
    elif isinstance( x, Env ):
      return s._add_env( x )
    else:
      m = 'unexpected obj added to env: %s' % x
      raise Exception( m )

  # ------------------------------------
  # add_component
  # ------------------------------------

  def _add_component( s, component ):    

    interface = component.__interface__
    
    # conflicts
    s._conflict_check( interface )

    # add the new component
    interface__component = dict( s._interface__component )
    interface__component[ interface ] = component

    return Env( interface__component )
  
  # ------------------------------------
  # add_library
  # ------------------------------------
  
  def _add_library( s, library ):
    # call library, assuming all library dependencies are already in self
    component = library( s )
    
    # add component
    return s + component  

  # ------------------------------------
  # add_env
  # ------------------------------------
  
  def _add_env( s, other ):
    output = s
    for component in other.components:
      try:
        output += component
      except s.Interface_conflict:
        other_component = s.interface__component( component.__interface__ )
        
        if component is not other_component:
          raise
        
    return output
  
# ------------------------------------------------------------------------------
# empty_env
# ------------------------------------------------------------------------------

empty_env = Env( {} )
