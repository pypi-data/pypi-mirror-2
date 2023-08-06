Chicken and egg python zc.buildout extension
============================================

This extensions for zc.buildout is created to solve chicken and egg problem
while working with buildout and when some exact version of python, which is
provided by buildout shall be used to *execute* this buildout itself.

Usage
-----

Part to build python is required. By convention slapos.rebootstrap will try to
find python executable in:

  special.parts.directory/partname/bin/partname

But when needed python-path parameter can be used to point rebootstrap to find
python in:

  special.parts.directory/partname/python-path

Add slapos.rebootstrap to extensions and set rebooter-section to above section.

Use whatever python to bootstrap and run buildout. If reboot will detect that
sys.executable used to run buildout is different then executable provided in
python section it will try to find this executable. If it does not exists it
will install this section and then reinstall buildout using new python
executable. Later buildout run will continue using new python.

Because external buildout is used to provide buildout version parameter is
introduced to being able to upgrade not in place python part. This parameter
is required and becomes part of suffix.

Whenever developer-mode is set to true no cleanup will be done in case of
failure. Then user is responsible to cleanup directories.

Example profile and invocation
------------------------------
::

  [buildout]
  extensions = slapos.rebootstrap
  
  parts =
    realrun
  
  [rebootstrap]
  section = slapospython
  version = 1

  [slapospython]
  recipe = plone.recipe.command
  stop-on-error = true
  command = mkdir -p ${buildout:parts-directory}/${:__section_name__}/bin &&
    cp -f /usr/bin/python ${:executable}
  
  [realrun]
  recipe = plone.recipe.command
  command =
    echo Running with python ${buildout:executable}
  update-command = ${:command}

After bootstrapping and running this buildout it will print:

Running with python /path/to/buildout/parts.rebootstrap.1/slapospython/bin/slapospython

Running tests
-------------

Test for this package can be run as simple as:

 $ python setup.py test

Please keep in mind that clean python environment is required -- the best one is
provided by buildout or virtualenv *WITHOUT* site packages.
