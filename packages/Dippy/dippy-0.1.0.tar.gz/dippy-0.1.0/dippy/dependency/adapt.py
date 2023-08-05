
from dippy.util import Dispatch

from dependency import Get_attr, Get_item

# ------------------------------------------------------------------------------
# adapt dispatch function
# ------------------------------------------------------------------------------

def get_key( env, interface ):
  return type( interface )

adapt = Dispatch( get_key = get_key )

# ------------------------------------------------------------------------------
# get_attr registration
# ------------------------------------------------------------------------------

def adapt_get_attr( env, get_attr ):  
  src = adapt( env, get_attr.src )
  return getattr( src, get_attr.name )
  
# --------------------------------------

adapt.add( Get_attr, adapt_get_attr )

# ------------------------------------------------------------------------------
# get_item registration
# ------------------------------------------------------------------------------

def adapt_get_item( env, get_item ):  
  src = adapt( env, get_item.src )
  return src[ get_item.name ]

# --------------------------------------

adapt.add( Get_item, adapt_get_item )


# ------------------------------------------------------------------------------
# other registrations...
# - interface in interface.py
# - library in library.py
# ------------------------------------------------------------------------------
