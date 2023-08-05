
from dippy import lib

from dl_interface import interface

# ------------------------------------------------------------------------------
# library
# ------------------------------------------------------------------------------

@lib( interface )
def library( doc ):
  
  def url__doc( url ):
    return doc
  
  return dict(
    url__doc = url__doc,
  )

