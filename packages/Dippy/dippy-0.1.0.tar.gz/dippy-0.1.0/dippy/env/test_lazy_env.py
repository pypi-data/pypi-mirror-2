
from dippy.library import lib

from _INTERFACE import empty_env, lazy_env

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def test_diamond():
    
  @lib()
  def a_lib():
    return {}
  
  @lib( a = a_lib )
  def b_lib( a ):
    return {}
  
  @lib( a = a_lib )
  def c_lib( a ):
    return {}
  
  @lib( b = b_lib, c = c_lib )
  def d_lib( b, c ):
    return {}
  
  # ------------------------------------
  
  @lazy_env()
  def a_env():
    return empty_env._add_library( a_lib )
  
  @lazy_env( a_env )
  def b_env( parent ):
    return parent._add_library( b_lib )
  
  @lazy_env( a_env )
  def c_env( parent ):
    return parent._add_library( c_lib )
  
  @lazy_env( b_env, c_env )
  def d_env( parent ):
    return parent._add_library( d_lib )
  
  # ------------------------------------
  
  env = d_env()
  
  env( a_lib )
  env( b_lib )
  env( c_lib )
  env( d_lib )

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def test_simplest():
  
  @lib()
  def a_lib():
    return {}
  
  @lib( a = a_lib )
  def b_lib( a ):
    return {}
  
  # ------------------------------------
  
  @lazy_env()
  def a_env():
    return empty_env._add_library( a_lib )
  
  @lazy_env( a_env )
  def b_env( parent ):
    return parent._add_library( b_lib )
  
  env = b_env()
  
  env( a_lib )
  env( b_lib )

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def test_was_broken():  
  
  @lib()
  def e_lib():
    return {}
  
  @lib()
  def b_lib():
    return {}
  
  @lib( b = b_lib, e = e_lib )
  def d_lib( b, e ):
    return {}
  
  # ------------------------------------
  
  @lazy_env()
  def e_env():
    return empty_env._add_library( e_lib )
  
  @lazy_env()
  def b_env():
    return empty_env._add_library( b_lib )
  
  @lazy_env( b_env, e_env )
  def d_env( parent ):
    return parent._add_library( d_lib )
  
  # ------------------------------------
  
  env = d_env()
  
  env( b_lib )
  env( d_lib )
