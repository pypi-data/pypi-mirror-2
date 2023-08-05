
import re
commas = re.compile( r'\s*,\s*' )

# ------------------------------------------------------------------------------
# validate_names
# ------------------------------------------------------------------------------

class Invalid_name( Exception ): pass

# --------------------------------------

def validate_names( names ):
  for name in names:
    validate_name( name )

# --------------------------------------

def validate_name( name ):    
  if name.startswith( '_' ):
    m = 'dippy names cannot start with "_", found "%s"' % name
    raise Invalid_name( m )

  if len( name ) == 0:
    raise Invalid_name( 'dippy names cannot be length 0' )
  
  if ' ' in name:
    m = 'dippy names cannot contain spaces, found "%s"' % name
    raise Invalid_name( m )

# ------------------------------------------------------------------------------
# input__names
# ------------------------------------------------------------------------------

def input__names( names ):
  
  if isinstance( names, basestring ):
    names = names.strip()
    names = commas.split( names )
  
  names = frozenset( names )
  validate_names( names )
  
  return names
