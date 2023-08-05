
from dippy import empty_env

# ------------------------------------------------------------------------------
# import implementations
# ------------------------------------------------------------------------------

# json
from dippy.example.json.json_cjson import component as json
#from dippy.example.json.json_simplejson import component as json

# api
from dippy.example.api.api_google import library as api

# download
from dippy.example.download.dl_urllib2 import component as dl

# gallery
from dippy.example.render.render_vertical import component as render
#from dippy.example.render.render_horizontal import component as render

# search
from dippy.example.search.search import library as search_lib

# ------------------------------------------------------------------------------
# build implementations
# ------------------------------------------------------------------------------

# Notice, due to adaptation, the client (this file), doesn't need to
# manually route all dependencies. The client only needs to ensure that a
# library's dependencies must be in the env before that library can be added.
# - So, the client only knows the toplogical sort of the dependency DAG (directed-acyclic graph)

env = empty_env

env += json

# api depends on: json
env += api

env += dl

env += render

# search depends on: api, download, gallery
env += search_lib

# ------------------------------------------------------------------------------
# export topic__gallery
# ------------------------------------------------------------------------------

# Clients of this build file can statically import topic__gallery from here.
# So they don't need to know anything about dippy, env's, etc.

topic__gallery = env( search_lib.topic__gallery )

# ------------------------------------------------------------------------------
# run (for viewing results without a web server running)
# ------------------------------------------------------------------------------

def run( topic ):
  '''
  import dippy.example.build as b; reload( b ); b.run( 'clinton' )
  '''

  gallery = topic__gallery( topic )
  
  file_name = '%s.html' % topic
  handle = open( file_name, 'w' )
  print >>handle, gallery.encode( 'utf-8' )
  
  handle.close()

