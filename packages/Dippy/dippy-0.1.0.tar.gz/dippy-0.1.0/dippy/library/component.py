
from dippy.util import get_only_positional

from name import validate_names
from interface import assert_fulfills

# ------------------------------------------------------------------------------
# Component
# ------------------------------------------------------------------------------

class Component( object ):

  def __init__( s, *positional, **name__attr ):
    
    # validate names
    names = frozenset( name__attr.keys() )   
    validate_names( names )
    
    # fulfills interface
    interface = get_only_positional( positional, optional = False )    
    assert_fulfills( name__attr, interface )
    
    # set
    s.__interface__ = interface
    s._names = names
    s._name__attr = name__attr
  
  # ------------------------------------

  def __getattr__( s, name ):
    if name not in s._names:
      m = '"%(name)s" attr name not in %(component)s' % dict(
        name = name,
        component = s,
      )
      raise AttributeError( m )
    
    return s._name__attr[ name ]
  
  # ------------------------------------

  def __str__( s ):    
    return 'Component( interface = %(interface)s, names = %(names)s )' % dict(
      interface = s.__interface__,
      names = ', '.join( s._names ),
    )

