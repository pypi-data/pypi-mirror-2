'''
This file contains a cheatsheet for Dippy. It covers a significant portion
of the library's API, with explanatory comments.  
'''

def test_cheatsheet():
  
  # ----------------------------------------------------------------------------
  # Interface: A set of required names.
  # ----------------------------------------------------------------------------

  from dippy import Interface

  # no attributes specified
  interface = Interface()
  
  # x and y attributes required
  interface = Interface( [ 'a', 'b' ] )
  
  # syntactic sugar
  interface = Interface( 'a, b' )
  
  # ----------------------------------------------------------------------------
  # interface names cannot start with _
  # ----------------------------------------------------------------------------
  
  from dippy import Invalid_name
  try:
    Interface( 'a, _b, c' )    
    raise Exception( 'should not get here' )
  except Invalid_name:
    pass    
  
  # ----------------------------------------------------------------------------
  # Component: An object with attributes fulfilling an Interface.
  # ----------------------------------------------------------------------------
  
  from dippy import Component
  
  component = Component(
    # interface must be passed in positionally
    interface,
    
    # components must have attributes required by the interface
    a = 1,
    b = 2,
    
    # components can have more attributes than the interface knows about
    c = 3,
  )
  
  # this helper function will be reused below
  def verify_component( component ):  
    # components have __interface__ attribute
    assert component.__interface__ is interface
    
    # dotted access to a component's attributes
    assert component.a == 1
    assert component.b == 2
    assert component.c == 3
  
  # verify
  verify_component( component )
  
  # ----------------------------------------------------------------------------
  # a component must fulfill it's interface
  # ----------------------------------------------------------------------------
  
  from dippy import Interface_not_fulfilled
  try:
    Component(
      interface,
      a = 1,
      # b is required by interface, but not provided
      c = 3,
    )

    raise Exception( 'should not get here' )
  except Interface_not_fulfilled:
    pass
  
  # ----------------------------------------------------------------------------
  # Library: A function that generates components with a specific Interface.
  # ----------------------------------------------------------------------------
  
  from dippy import Library
  
  # raw function
  def fn( x, y ):
    
    # return a dict of the generated components attributes
    return dict(
      a = x,
      b = y,
      c = x + y,
    )
  
  # create a library by wrapping fn
  library = Library(   
    # library wraps this function
    fn = fn,

    # generated components will fulfill this interface
    interface = interface,
  )

  # this helper will be reused below
  def verify_library( library ):
  
    # libraries have __interface__ attribute
    assert library.__interface__ is interface
    
    # call library to generate component
    component = library( x = 1, y = 2 )
  
    # component is the same as the one above
    verify_component( component )

  # verify
  verify_library( library )
  
  # ----------------------------------------------------------------------------
  # @lib: A decorator providing easier syntax for library writing.
  # ----------------------------------------------------------------------------

  from dippy import lib
  
  @lib(
    interface # interface is optionally passed in as the only positional arg
  )
  def library( x, y ):  # this function is the same as fn above
    return dict(
      a = x,
      b = y,
      c = x + y,
    )

  # library is the same as the one above
  verify_library( library )
  
  # ----------------------------------------------------------------------------
  # if an interface isn't passed into @lib, a default empty interface will be generated 
  # ----------------------------------------------------------------------------

  @lib()
  def library_with_default_interface():
    return dict(
      whatever = 'i want',
    )
    
  assert library_with_default_interface.__interface__ is not interface

  # ----------------------------------------------------------------------------
  # Env: A mapping from interface -> component
  # ----------------------------------------------------------------------------
  
  from dippy import empty_env

  # fails to find the interface in the env
  try:
    empty_env( interface )
    raise Exception( 'should not get here' )
  except empty_env.Missing_interface:
    pass
  
  # ----------------------------------------------------------------------------
  # adding a component to an env
  #   env_2 = env_1 + component
  # ----------------------------------------------------------------------------
  
  # env's are immutable (like strings), so adding a component returns a new env
  env = empty_env + component
  
  # += is convenient syntax provided by python
  env = empty_env
  env += component

  # now we can find the component in the env via interface
  assert interface is component.__interface__
  assert component is env( interface )
  
  # we can also conveniently traverse into the matching component
  assert component.a is env( interface.a )
  
  # env's cannot contain 2 components that implement the same interface
  component_with_same_interface = Component( interface, a = 0, b = 0 )
  try:
    env + component_with_same_interface
    raise Exception( 'should not get here' )
  except  env.Interface_conflict:
    pass
  
  # ----------------------------------------------------------------------------
  # adding two envs 
  #   env_3 = env_1 + env_2
  # ----------------------------------------------------------------------------
  
  # setup a different env with a different component
  component_2 = Component( Interface() )
  env_2 = empty_env + component_2
  assert component_2 is env_2( component_2.__interface__ )
  
  # add the two env's together
  env_3 = env + env_2
  
  # both components are in the resulting env
  assert component is env_3( component.__interface__ )
  assert component_2 is env_3( component_2.__interface__ )
  
  # ----------------------------------------------------------------------------
  # adding env's together can result in a conflict
  # ----------------------------------------------------------------------------
  
  env_with_same_interface = empty_env + component_with_same_interface
  try:
    env + env_with_same_interface
    raise Exception( 'should not get here' )
  except env.Interface_conflict:
    pass
  
  # ----------------------------------------------------------------------------
  # adding a library to an env, calls the library, and adds the resulting component to the env
  #   env_2 = env_1 + library
  # ----------------------------------------------------------------------------
  
  @lib()
  def library_with_no_inputs():
    return dict(
      message = 'hello',
    )
    
  # notice, didn't pass an interface into @lib(), so one will be generated
  message_interface = library_with_no_inputs.__interface__
  
  # env + component (same usage as above)
  message_component = library_with_no_inputs()
  message_env = empty_env + message_component
  assert 'hello' == message_env( message_interface.message ) 
  
  # env + library (this calls the library, and adds the resulting component to the env)
  env = empty_env + library_with_no_inputs
  assert 'hello' == message_env( message_interface.message )
    
  # ----------------------------------------------------------------------------
  # dependency annotation: dependening on an interface
  # ----------------------------------------------------------------------------

  # library 1 has no dependencies
  @lib()
  def library_1():
    return dict()

  interface_1 = library_1.__interface__
  component_1 = library_1()
  
  # library_2 dependends on interface_1 
  @lib(
    dependency = interface_1
  )
  def library_2( dependency ):
    return dict(
      message = 'howdy',
      dependency = dependency,  # export the dependency, so we can verify it
    )

  interface_2 = library_2.__interface__
    
  # manually provide dependency (pass component_1 into the library manually)
  component_2 = library_2( dependency = component_1 )
  assert component_2.dependency is component_1
  
  # setup an env containing the dependency
  env = empty_env + component_1
  assert env( interface_1 ) is component_1
  
  # call library_2 without manually providing its dependency, instead pass env
  # in as a positional argument
  # - library_2 will find its dependency using env( interface_1 )
  component_2 = library_2( env )
  assert component_2.dependency is component_1
  # note: the above line is basically the main goal of Dippy. The client doesn't
  # have to collect library_2's dependencies and pass them in. Instead, he just needs
  # to get an env that contains them.
  
  # ----------------------------------------------------------------------------
  # when you add a library_2 to env, it actually calls library_2( env )
  # ----------------------------------------------------------------------------
  
  # same as: env_2 = env + library_2( env ) 
  env_2 = env + library_2
  
  # find component_2 in env_2, via interface
  component_2 = env_2( interface_2 )
  assert 'howdy' == env_2( interface_2.message ) # notice the dotted traversal
  assert component_1 is env_2( interface_2.dependency ) # notice the dotted traversal
  
  # ----------------------------------------------------------------------------
  # using a library in place of its interface (for convenience)
  # ----------------------------------------------------------------------------
 
  # we've seen finding a component in an env via interface
  assert component_2 is env_2( library_2.__interface__ )
  assert 'howdy' == env_2( library_2.__interface__.message )
  
  # a shorter way of writing this omits the .__interface__
  assert component_2 is env_2( library_2 )
  assert 'howdy' == env_2( library_2.message )
  
  # we've also seen depending on an interface
  @lib(
    dependency = library_2.__interface__
  )
  def l( dependency ):
    return dict()
  
  # you can also omit the .__interface here
  @lib(
    dependency = library_2
  )
  def l( dependency ):
    return dict()
      
  # ----------------------------------------------------------------------------
  # @lazy_env: trees of functions that generate env's (for unit tests)
  # ----------------------------------------------------------------------------

  from dippy import lazy_env
  
  # ------------------------------------
  # create an lazy env tree
  # ------------------------------------
  
  # use dict here, because python closures cannot redefine local variables
  counts = dict(
    lazy_1 = 0,
    lazy_2 = 0,
    lazy_3 = 0,
  )

  @lazy_env() # lazy_1 doesn't depend on any other lazy envs
  def lazy_1():
    counts[ 'lazy_1' ] += 1
    return empty_env + component_1
  
  @lazy_env() # lazy_1 doesn't depend on any other lazy envs
  def lazy_2():
    counts[ 'lazy_2' ] += 1
    return empty_env + Component( Interface() )
        
  @lazy_env( lazy_1, lazy_2 ) # lazy_3 depends on lazy_1 and lazy_2
  def lazy_3( parent_env ):   # parent_env is a normal env. it will contain 
    counts[ 'lazy_3' ] += 1
    return parent_env + library_2 
  
  # ------------------------------------
  # unit tests depending on lazy_3
  # ------------------------------------
   
  @lazy_3.depend(
    dependency = library_2.dependency
  )
  def unit_test_a( dependency ):
    assert dependency is component_1

  @lazy_3.depend(
    message = library_2.message
  )
  def unit_test_b( message ):
    assert message == 'howdy'
    
  # ------------------------------------
  # each unit test call creates a new env
  # ------------------------------------

  unit_test_a()
  for count in counts.values(): assert count == 1
  
  unit_test_b()
  for count in counts.values(): assert count == 2
  
  unit_test_b()
  for count in counts.values(): assert count == 3

