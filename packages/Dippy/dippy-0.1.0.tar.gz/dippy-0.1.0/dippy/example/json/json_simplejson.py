
from simplejson import JSONDecoder, JSONEncoder

from dippy import Component
from json_interface import interface

# no dynamic dependencies, so can just be a leaf component (rather than a library)
component = Component(
  interface,
  json__obj = JSONDecoder().decode,
  obj__json = JSONEncoder().encode,
)

