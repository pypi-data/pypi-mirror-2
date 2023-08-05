'''
Here is the motivation for lazy envioronments:

1) Multiple unit tests need the same environment setup.

2) Each test wants a fresh environment which is unaffected by other tests.

3) This leads to a shared env creation function. Each test calls this function to
get a fresh env, and then pulls its dependencies from the env.

4A) However, this leads to boilerplate at the top of each test, so lazy_env's provide
a move convenient @env.depend() syntax.

4B) Also, if multiple libraries depend on the same parent, we have the same diamond
problem from multiple inheritance. In this case, we only want (and can only have) 1
instance of each library in the env. Lazy env's also solve this problem, by knowing
a dependency tree, and only instantiating each env once.

'''

from dippy.util import wraps

from dippy.dependency import depend

from env import empty_env

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

class Lazy_env( object ):
  
  def __init__( s, get_env, *dependencies ):
    s._get_env = get_env
    
    for d in dependencies:
      assert isinstance( d, Lazy_env ), 'lazy envs can only depend on lazy envs'
    
    s._dependencies = dependencies
  
  # ------------------------------------
  # ------------------------------------
  
  @property
  def has_dependencies( s ):
    return len( s._dependencies ) > 0

  # ------------------------------------
  # ------------------------------------
  
  def __call__( s ):
    return s._add_self( existing_env = empty_env, already_added = set() )

  def _add_self( s, existing_env, already_added ):    
    if s.has_dependencies:
      for d in s._dependencies:
        if d in already_added:
          continue

        already_added.add( d )
        existing_env = d._add_self( existing_env = existing_env, already_added = already_added )
        
      return s._get_env( existing_env ) # parent_env
    else:
      self = s._get_env()
      return existing_env + self
  
  # ------------------------------------
  # ------------------------------------
  
  def depend( s, *a, **kw ):
    def wrap( test ):
      
      fn = depend( *a, **kw )( test )
      
      @wraps( test )
      def outer():
        env = s()
        fn( env )

      return outer
      
    return wrap

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def lazy_env( *dependencies ):
  '''
  lazy_env is a decorator providing friendly syntax
  '''
  
  def wrap( get_env ):
    return Lazy_env( get_env, *dependencies )
  return wrap

