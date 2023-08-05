
from dippy.util import raises

from dippy.dependency import depend, adapt
from dippy.library import Interface, Component

from _INTERFACE import empty_env
 
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def test_depend():
  A = Interface()
  B = Interface()
  
  a_1 = Component( A ) 
  b_1 = Component( B )
  
  env = empty_env
  env += a_1
  env += b_1

  @depend( a_2 = A, b_2 = B )
  def f( a_2, b_2, c ):
    assert a_2 is a_1
    assert b_2 is b_2
    assert c == 'c'
  
  # none
  f( a_2 = a_1, b_2 = b_1, c = 'c' )
  
  # all
  f( env, c = 'c' )
  
  # some
  f( env, a_2 = a_1, c = 'c' )

