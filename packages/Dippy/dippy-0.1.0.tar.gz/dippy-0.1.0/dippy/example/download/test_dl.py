
from dl_mock import library

def test_dl_mock():
  doc = 'hello'
  url = 'http://www.google.com'
  
  component = library( doc = doc )
  
  assert doc == component.url__doc( doc )

