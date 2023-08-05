
from dippy.util import raises
from dippy.library import Interface, Component

from _INTERFACE import empty_env

# ------------------------------------------------------------------------------
# env
# ------------------------------------------------------------------------------

def test_env():
  
  A = Interface()
  B = Interface()
  
  a_1 = Component( A )
  a_2 = Component( A )
  
  b = Component( B )
   
  env = empty_env
 
  # ------------------------------------
  # a
  # ------------------------------------
 
  raises( env.Missing_interface, env.__call__, A )
  
  # add then get
  env += a_1
  assert a_1 is env( A )  # adapt
 
  # add same component
  raises( env.Interface_conflict, env.__add__, a_1 )  # technically, this is safe, but potentially sloppy
  
  # add different component with same interface
  raises( env.Interface_conflict, env.__add__, a_2 )
  
  # ------------------------------------
  # b
  # ------------------------------------
  
  # next interface is missing
  raises( env.Missing_interface, env.__call__, B )
  
  env += b
  
  assert a_1 is env( A )
  assert b is env( B )
  
  