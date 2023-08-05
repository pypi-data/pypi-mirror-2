
# ------------------------------------------------------------------------------
# cjson
# ------------------------------------------------------------------------------

def test_cjson():
  try:
    import cjson
  except ImportError:
    return
  
  from json_cjson import component
  verify_component( component )

# ------------------------------------------------------------------------------
# simplejson
# ------------------------------------------------------------------------------

def test_simplejson():
  try:
    import simplejson
  except ImportError:
    return

  from json_simplejson import component  
  verify_component( component )

# ------------------------------------------------------------------------------
# verify_component
# ------------------------------------------------------------------------------

def verify_component( component ):
  assert component.obj__json( obj ) == json
  assert component.json__obj( json ) == obj 

# --------------------------------------

json = '[1, true]'

obj = [ 1, True ]

