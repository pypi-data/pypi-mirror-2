
Dependency inversion is essential for writing testable, modular and reusable
libraries.

Dippy makes dependency inversion easier in Python.  

--------------------------------------------------------------------------------
links
--------------------------------------------------------------------------------

dippy website:
  http://code.google.com/p/dippy/

about dependency inversion:
  http://stevewedig.com/dependency_inversion

--------------------------------------------------------------------------------
overview
--------------------------------------------------------------------------------

Interface
  A set of required attribute names.

Component
  An object fulfilling a specific Interface.
  
Library
  A function that generates Components fulfilling a specific Interface.
  (A Library's inputs are its dependencies, much like a module's static imports) 

Env
  A unique mapping from Interface to Component.

Dependency Interface Annotation
  Specifying the expected Interface for each of a library's dependencies. 

Dependency Adaptation
  If a library's dependency interfaces are annotated, then instead of manually 
  passing the dependencies into the library, a client can provide an Env that
  contains components matching those interfaces. This relieves the client of 
  knowing how to manually gather all of the dependencies.  

--------------------------------------------------------------------------------
examples
-------------------------------------------------------------------------------- 
    
1) a thoroughly commented unit test running through most of Dippy's API:
  dippy/dippy/test_cheatsheet.py

2) an example image search project structured with Dippy:
  dippy/dippy/example/example.txt

3) the rest of Dippy's unit tests document expected behavior

--------------------------------------------------------------------------------
project conventions
--------------------------------------------------------------------------------

s instead of self
x__y is a mapping from x to y
underscore, not camel case
2 spaces for indentation
spaces around operators
space after ([{, and before )]}
