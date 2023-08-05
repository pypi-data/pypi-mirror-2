
from dippy import Component

from cjson import decode, encode

from json_interface import interface

# no dynamic dependencies, so can just be a leaf component (rather than a library)
component = Component(
  interface,
  json__obj = decode,
  obj__json = encode,
)

