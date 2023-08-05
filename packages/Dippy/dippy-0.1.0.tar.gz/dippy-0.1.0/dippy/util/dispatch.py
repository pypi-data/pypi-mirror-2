
# ------------------------------------------------------------------------------
# Dispatch
# ------------------------------------------------------------------------------

class Dispatch( object ):
  
  def __init__( s, get_key ):
    s.get_key = get_key
    s.key__fn = {}
  
  # ------------------------------------
  
  def add( s, key, fn ):
    if key in s.key__fn:
      raise Exception
    
    s.key__fn[ key ] = fn
  
  # ------------------------------------
  
  def __call__( s, *a, **kw ):
    key = s.get_key( *a, **kw )
    
    if key not in s.key__fn:
      m = 'dispatch does not have key: %s, keys = %s' % (
        key,
        s.key__fn.keys()
      )
        
      raise Exception( m )
    
    fn = s.key__fn[ key ]
    
    return fn( *a, **kw )

