
def get_only_positional( positional, optional ):

  n = len( positional )
  
  if n >= 2:
    raise AssertionError( 'only one positional input is allowed' )
  elif n == 1:
    input = positional[ 0 ]
  elif not optional:
    raise AssertionError( 'positional input is expected' )
  else:
    input = None
  
  return input


def wraps( inner ):
  def wrap( outer ):
    outer.__name__ = inner.__name__
    return outer
  return wrap

