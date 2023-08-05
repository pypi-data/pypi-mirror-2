
from dippy import lazy_env

from dippy.example.json.json_env_unit import env as json_env

from api_google import library as google_lib

# ------------------------------------------------------------------------------
# env
# ------------------------------------------------------------------------------

# google_lib depends on the json_lib
@lazy_env( json_env )
def env( env ):
  env += google_lib
  return env

