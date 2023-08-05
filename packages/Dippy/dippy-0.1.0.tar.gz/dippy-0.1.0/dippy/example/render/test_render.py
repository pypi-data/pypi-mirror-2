
from render_vertical import component as vertical
from render_horizontal import component as horizontal

from dippy.example.api.test_google import sample_images

# ------------------------------------------------------------------------------
# vertical
# ------------------------------------------------------------------------------

def test_vertical():
  verify_component( vertical )
  
# ------------------------------------------------------------------------------
# horizontal
# ------------------------------------------------------------------------------

def test_horizontal():
  verify_component( horizontal )
  
# ------------------------------------------------------------------------------
# verify
# ------------------------------------------------------------------------------

def verify_component( component ):
  gallery = component.images__gallery( sample_images )
  verify_gallery( gallery, sample_images )

def verify_gallery( gallery, images ):
  for image in images:
    assert image[ 'url' ] in gallery
    assert image[ 'title' ] in gallery

