
def raises( Expected, fn, *a, **kw ):
  
  assert Expected is not Exception, 'raises() requires Expected to be more specific than Exception'

  assert issubclass( Expected, Exception ), 'in raises(), Expected was not a type of Exception, got %s' % ( Expected, )
   
  try:
    fn( *a, **kw )
  except Expected:
    return
  except Exception, e:
    raise

  m = 'in raises(): fn did not raise an error, expected %s' %  Expected
  raise AssertionError( m )

def eq( x, y ):
  if x != y:
    m = 'eq failed, %s != %s' % ( x, y )
    raise AssertionError( m )
