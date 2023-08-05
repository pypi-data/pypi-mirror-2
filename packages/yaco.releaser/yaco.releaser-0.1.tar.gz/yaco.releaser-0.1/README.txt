zest.releaser addon
===================

http://pypi.python.org/pypi/zest.releaser is collection of command-line programs to help you
automate the task of releasing a software project which can be used for
non-Python projects too like buildouts.

yaco.releaser is a very simple extension which allow append extra text to the default commit messages.

It's usefull for us because in Yaco is mandatory to mention a ticket to commit to a project.

.. contents::

Installation
------------
Just a simple ``easy_install yaco.releaser`` is enough.

Alternatively, buildout users can install yaco.releaser as part of a
specific project's buildout, by having a buildout configuration such as::

    [buildout]
    parts = releaser

    [releaser]
    recipe = zc.recipe.egg
    eggs = yaco.releaser

Usage
-----
Follow http://pypi.python.org/pypi/zest.releaser documentation

In the process of ``prerelease`` or ``postrealease`` you will be wondered about adding
extra text to the commit message.

**Warning**: The ``release`` (so fullrelease neither) are not supported yet, ie. you cannot add and extra
to the message when creating the new tag.


Development notes
-----------------
The svn source can be found at
https://svn.plone.org/svn/collective/yaco.releaser/trunk . If you have access
to the collective, you can fix bugs right away. Bigger changes on a branch please and mail pcaro_yaco.es about it :-)

TODO
----
* Add tests.
* Support for release and fullrelease commands.
* Do less interative. Maybe reading for enviroment.


Credits
-------
* `Pablo Caro Revuelta <http://pablocaro.es>`_ (Yaco Sistemeas) is the
  originator and main author.
