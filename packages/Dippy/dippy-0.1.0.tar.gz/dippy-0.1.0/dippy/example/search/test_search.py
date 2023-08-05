
from dippy import lazy_env

# donwload
from dippy.example.download.dl_mock import library as download_lib

# gallery
from dippy.example.render.render_unit_env import env as render_env
from dippy.example.render.test_render import verify_gallery

# api
from dippy.example.api.api_google_unit_env import env as api_env
from dippy.example.api.test_google import sample_json, sample_topic, sample_images

# search
from search import library as search_lib

# ------------------------------------------------------------------------------
# env
# ------------------------------------------------------------------------------

# search depends on api and render
@lazy_env( api_env, render_env )
def env( env ):
  
  # search also depends on download
  dl_component = download_lib( doc = sample_json )
  env += dl_component
  
  # create search component using env, and add to env
  env += search_lib
  return env


# ------------------------------------------------------------------------------
# test_search
# ------------------------------------------------------------------------------


@env.depend(
  topic__gallery = search_lib.topic__gallery,
)
def test_search( topic__gallery ):
  gallery = topic__gallery( sample_topic )
  verify_gallery( gallery, sample_images )