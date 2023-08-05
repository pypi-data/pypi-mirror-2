
from dippy import lazy_env, empty_env

from render_vertical import component

# ------------------------------------------------------------------------------
# env
# ------------------------------------------------------------------------------

@lazy_env()
def env():
  return empty_env + component

