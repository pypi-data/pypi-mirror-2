
from dippy import Component

from render_interface import interface
from render_util import image__html, body__page

# ------------------------------------------------------------------------------
# images__gallery
# ------------------------------------------------------------------------------

def images__gallery( images ):
  body = images__body( images )
  page = body__page( body )
  return page

# ------------------------------------------------------------------------------
# images__body
# ------------------------------------------------------------------------------

def images__body( images ):
  
  tds = u''.join(
    image__td( image ) for image in images
  )
  
  return u'''
  <table>
    <tr>
      %s
    </tr>
  </table>
  ''' % tds

# ------------------------------------------------------------------------------
# image__td
# ------------------------------------------------------------------------------

def image__td( image ):
  return u'''
  <td>
  %s
  </td>
  ''' % image__html( image )

# ------------------------------------------------------------------------------
# component
# ------------------------------------------------------------------------------

# no dynamic dependencies, so can just be a leaf component (rather than a library)
component = Component(
  interface,
  images__gallery = images__gallery,
)

