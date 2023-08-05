
from urllib2 import urlopen as url__lines

from dippy import Component

from dl_interface import interface

# ------------------------------------------------------------------------------
# url__doc
# ------------------------------------------------------------------------------

def url__doc( url ):
  lines = url__lines( url )
  doc = ''.join( lines )
  return doc

# ------------------------------------------------------------------------------
# component
# ------------------------------------------------------------------------------

component = Component(
  interface,
  url__doc = url__doc,
)
