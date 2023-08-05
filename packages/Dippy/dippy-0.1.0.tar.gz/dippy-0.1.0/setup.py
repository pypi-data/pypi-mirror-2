
from distutils.core import setup

package_str = '''
dippy
dippy.dependency
dippy.env
dippy.library
dippy.util

dippy.example
dippy.example.api
dippy.example.download
dippy.example.json
dippy.example.render
dippy.example.search
'''

packages = tuple(
  path.strip() for path in package_str.split()
) 

setup(
  name = 'dippy',
  version = '0.1.0',
  author = 'Steve Wedig',
  author_email = 'stevewedig@gmail.com',
  url = 'http://code.google.com/p/dippy/',
  license = 'LICENSE.txt',
  description = 'Dependency Inversion Principle in Python',
  long_description = open( 'README.txt' ).read(),
  packages = packages,
)

