'''
...

this example is written for clarity, so there is no error checking
'''


from dippy import lib

from dippy.example.json.json_interface import interface as json_interface

from api_interface import interface

# ------------------------------------------------------------------------------
# library
# ------------------------------------------------------------------------------

@lib(
  interface,
   json__obj = json_interface.json__obj 
)
def library( json__obj ):
  
  def doc__images( json ):
    obj = json__obj( json )
    return obj__images( obj )
  
  return dict(
    topic__url = topic__url,
    doc__images = doc__images,
  )

# ------------------------------------------------------------------------------
# obj__images
# ------------------------------------------------------------------------------

def obj__images( obj ):
  results = obj__results( obj )
  images = results__images( results )
  return images

# ------------------------------------------------------------------------------
# json__results
# ------------------------------------------------------------------------------

def obj__results( obj ):
  results = obj[ 'responseData' ][ 'results' ]
  return results

# ------------------------------------------------------------------------------
# results__images
# ------------------------------------------------------------------------------

def results__images( results ):
  images = []
  
  for result in results:
    image = dict(
      url = result[ 'url' ],
      title = result[ 'title' ],
    )
    images.append( image )

  return images

# ------------------------------------------------------------------------------
# topic__url
# ------------------------------------------------------------------------------

def topic__url( topic ):
  return api_url_template % dict( topic = topic )

api_key = 'ABQIAAAA0hBN_e4XHbgeCGsAICczJxRvKsJ_v0SeGr5x17BErgd0djNAphRx7pdUBMI1jejS9TCsWeswxHAPJg'

api_url_template = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%(topic)s&key=' + api_key

