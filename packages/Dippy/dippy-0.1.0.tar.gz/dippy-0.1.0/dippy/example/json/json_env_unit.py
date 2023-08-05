
from dippy import empty_env, lazy_env

# if you have cjson
from json_cjson import component

# if you have simplejson
#from json_simple import component

@lazy_env()
def env():
  return empty_env + component
