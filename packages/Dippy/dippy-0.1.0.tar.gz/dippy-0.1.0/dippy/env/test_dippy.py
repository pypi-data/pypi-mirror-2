'''
dippy integration tests
'''

from dippy.util import raises

from dippy import lib, empty_env

# ------------------------------------------------------------------------------
# lib
# ------------------------------------------------------------------------------

def test_lib():
  
  @lib()
  def Double( x ):
    return dict(
      y = x * 2,
    )
  
  double = Double( x = 5 )
  assert double.y == 10
  
def test_cannot_export_underscore():
  pass
  
# ------------------------------------------------------------------------------
# env adapt
# ------------------------------------------------------------------------------

def test_env_adapt():
  
  A, B, C = sample_libs()

  # ------------------------------------
  
  a = A( x = 2 )
  assert a.double == 4
  
  b = B( a_lib = a )
  assert b.quad == 8

  c = C( double = a.double )
  assert c.single == 2

  # ------------------------------------

  env = empty_env + a
  assert a is env( A )
  
  b_2 = B( env )
  assert b_2.quad == 8
  
  c_2 = C( env )
  assert c_2.single == 2  

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

#def test_env_create():
#  
#  A, B, C = sample_libs()
#  env = empty_env
#
#  a = A( x = 2 )
#  assert a.double == 4
#  
#  env = env.add( a )
#  env = env.create( B )
#  b = env.adapt_to( B )
#  assert b is env.adapt_to( B )
#  assert b.quad == 8

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def sample_libs():
  @lib()
  def A( x ):
    return dict(
      double = x * 2
    )
  
  # lib dependency
  @lib( a_lib = A )
  def B( a_lib ):
    return dict(
      quad = a_lib.double * 2
    )
    
  # lib.attr dependency
  @lib( double = A.double )
  def C( double ):
    return dict(
      single = double / 2
    )
  
  return A, B, C

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def test_lib_only_takes_1_positional():
    
  @lib()
  def A( x, y ):
    return dict()
  
  # only 1 positional can be passed in (the env)
  raises( AssertionError, A, 1, 2 )


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def test_paths():
  
  @lib()
  def Lib():
    class C( object ):
      b = dict(
        c = 2
      )
      
    return dict(
      a = C(),
    )
  
  component = Lib()
  env = empty_env + component

  assert 2 == component.a.b[ 'c' ]
  
  path = Lib.a.b[ 'c' ]

  assert 2 == env( path )
  

  
