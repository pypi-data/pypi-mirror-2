Overview
========

This recipe normalizes any option value for the part it manages if said
option value begins with 'path.' -- such options are assumed to be 
paths.  This recipe replaces relative paths of all sorts with real, 
full system path to files or directories.

This recipe is useful as a replacement for using non-part sections for
holding path configuration; instead, use a part with this recipe, and 
both relative and absolute paths can be stored for use by other parts
in your buildout.


Usage
=====

Let's create a buildout with a single part containing the configuration
options we want to either preserve or normalize:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = 
    ...     paths
    ... 
    ... [paths]
    ... recipe = collective.recipe.realpath
    ... notpath.here = something else
    ... path.parent = ${buildout:directory}/..
    ... path.to.nowhere = /dev/null
    ... path.var = ${buildout:directory}/var
    ... """)
    
We run this buildout...

    >>> print 'start', system(buildout) # doctest:+ELLIPSIS
    start...
    Installing paths.
   
We can see that (only) the necesssary options have normalized path
values:

    >>> from os.path import dirname, realpath
    >>> builddir = dirname(dirname(buildout))
    >>> buildout_parent = realpath('%s/..'% builddir)
    >>> cat('.installed.cfg') # doctest: +ELLIPSIS
    [buildout]
    ...
    [paths]
    ...
    notpath.here = something else
    path.parent = ...
    path.to.nowhere = /dev/null
    path.var = /sample-buildout/var
    ...


LICENSE / CREDITS
=================

MIT-style license -- See docs/COPYING.txt
Author: Sean Upton / University of Utah / upiq.org
Upstream:

- https://teamspace.upiq.org/trac

- http://dev.plone.org/collective/

