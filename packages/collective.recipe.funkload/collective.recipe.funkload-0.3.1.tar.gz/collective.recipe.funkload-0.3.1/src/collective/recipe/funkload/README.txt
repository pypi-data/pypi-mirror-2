
collective.recipe.funkload is a nice and simple recipe that allows easy running of funkload tests and generation of reports on them,
running ./bin/funkload bench will run all the funkload tests within the buildout and then autogenerate the html reports for them.
Report generation requires gnuplot, currently there is no way to cleanly disable this.  The reports and supporting xml is stored in
the path pointed to by location in your part (defaults to ./var/funkload).  You may also have the reports generated in a different directory
using report_destination.


Example usage
=============

In order for this to work its magic you need to set a base URL for the tests
to be run on, your buildout part will look something like this:

  >>> write('buildout.cfg',
  ... """
  ... [buildout]
  ... parts = test1
  ... index = http://pypi.python.org/simple
  ... [test1]
  ... recipe = collective.recipe.funkload
  ... url = 127.0.0.1:8080 
  ... """)

Running that buildout gives us the ``funkload`` script:

  >>> print 'start\n', system(buildout) 
  start
  ...
  Generated script '/sample-buildout/bin/funkload'.

Which passes the host through to the subcommand handler in the recipe:

  >>> import os
  >>> script = os.path.join(sample_buildout,'bin','funkload')
  >>> print open(script,'r').read()
  #!...url="127.0.0.1:8080"...

If you don't specify a URL buildout will fail:

  >>> write('buildout.cfg',
  ... """
  ... [buildout]
  ... parts = test1
  ... index = http://pypi.python.org/simple
  ... [test1]
  ... recipe = collective.recipe.funkload
  ... """)

  >>> print 'start\n', system(buildout) 
  start
  ...
  KeyError: 'You must specify an address to test'


Record
------

Since version 0.3 you can now use record to create funkload tests even faster::

    >>> print system('bin/funkload')
    Usage:
    bench:  Launch a FunkLoad unit test as load test. 
    record: Launch a TCPWatch proxy and record activities, then output a 
            FunkLoad script or generates a FunkLoad unit test if test_name is specified.
    report:  Generate a report from the most recent bench result 
    test:  Launch a FunkLoad unit test. 
    <BLANKLINE> 
