
from dippy.util import eq, raises

from name import Invalid_name
from interface import Interface, Interface_not_fulfilled, assert_fulfills, fulfills

# ------------------------------------------------------------------------------
# basic
# ------------------------------------------------------------------------------

def test_interface():
  interface = Interface( 'a, b, c' )
  str( interface )

# ------------------------------------------------------------------------------
# names
# ------------------------------------------------------------------------------

def test_names():

  i2 = Interface( 'a b c d e'.split() )
  
  i3 = Interface( 'a,b, c ,d , e' )
    
  eq( i2._expected_names, i3._expected_names )

# --------------------------------------

def test_invalid_name():
  
  raises( Invalid_name, Interface, 'a, _b, c' )
  
  # leading _
  raises(
    Invalid_name,
    Interface,
    'a, _b, c'.split( ', ' )
  )
  
  # blank name
  raises(
    Invalid_name,
    Interface,
    'a, , c'.split( ', ' )
  )

  # space in name
  raises(
    Invalid_name,
    Interface,
    'a, b c, c'.split( ', ' )
  )


# ------------------------------------------------------------------------------
# fulfills
# ------------------------------------------------------------------------------

def test_fulfills():
  
  # ------------------------------------
  # normal interface
  # ------------------------------------
  
  interface = Interface( 'a, b' )
  
  # exact
  assert_fulfills( dict( a = 1, b = 2 ), interface )
  
  # extra
  assert_fulfills( dict( a = 1, b = 2, c = 3 ), interface )
  
  # missing
  assert not fulfills( dict( a = 1, c = 3 ), interface )
  
  # all missing
  assert not fulfills( dict(), interface )

  # ------------------------------------
  # empty interface
  # ------------------------------------
  
  interface = Interface()
  
  # exact
  assert_fulfills( dict(), interface )
  
  # extra
  assert_fulfills( dict( a = 1 ), interface )
  
