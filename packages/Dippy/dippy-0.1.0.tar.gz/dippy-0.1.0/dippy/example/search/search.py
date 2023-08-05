
from dippy import lib

from dippy.example.download.dl_interface import interface as dl_interface
from dippy.example.api.api_interface import interface as api_interface
from dippy.example.render.render_interface import interface as render_interface

# ------------------------------------------------------------------------------
# library
# ------------------------------------------------------------------------------

@lib(
  api = api_interface,
  url__doc = dl_interface.url__doc,
  images__gallery = render_interface.images__gallery,
)
def library( url__doc, images__gallery, api ):
  
  def topic__gallery( topic ):
    url = api.topic__url( topic )
    doc = url__doc( url )
    images = api.doc__images( doc )
    gallery = images__gallery( images )
    return gallery
  
  return dict(
    topic__gallery = topic__gallery,
  )

