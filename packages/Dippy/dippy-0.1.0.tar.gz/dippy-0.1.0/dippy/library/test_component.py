
from dippy.util import raises, eq

from name import Invalid_name
from interface import Interface, Interface_not_fulfilled
from component import Component

# ------------------------------------------------------------------------------
# basic
# ------------------------------------------------------------------------------

def test_component():
  interface = Interface()
  
  a = 1
  b = 2
  component = Component( interface, a = a, b = b )
    
  eq( a, component.a )
  eq( b, component.b )

  raises( AttributeError, lambda: component.c )

# ------------------------------------------------------------------------------
# invalid name
# ------------------------------------------------------------------------------

def test_invalid_name():
  
  interface = Interface()
  raises( Invalid_name, Component, interface, _a = 1 )

# ------------------------------------------------------------------------------
# fulfills
# ------------------------------------------------------------------------------

def test_fulfills():
  
  interface = Interface( 'a, b' )
  
  # exact
  component = Component( interface, a = 1, b = 2 )
  
  # extra
  component = Component( interface, a = 1, b = 2, c = 3 )
  
  # extra + missing
  raises( Interface_not_fulfilled, Component, interface, a = 1, c = 3 )
  
  # all missing
  raises( Interface_not_fulfilled, Component, interface )
  
