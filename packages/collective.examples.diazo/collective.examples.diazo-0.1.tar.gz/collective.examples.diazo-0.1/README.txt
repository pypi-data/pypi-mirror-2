Introduction
============

This package shows how you might use collective.xdv / Diazo in a Plone site. It
aims to be more verbose (and probably more redundant) than xdv-worked-example_.

It's aimed towards developers, and it focuses especially on adding worked
examples of more complex XSLT.  Eventually we're hoping to get the code
examples in the xdv package itself, as they're not specific to Plone.

.. contents:: Contents

Installation
------------

Include collective.examples.diazo in your buildout.

There's a buildout on
https://svn.plone.org/svn/collective/collective.examples.diazo/trunk/buildout.
It won't work on Mac...yet.  But you can install collective.xdv on a Mac using
statically compiled lxml, don't use the buildout contained here, but use the
collective.examples.diazo by checking out the source to your /src directory
and updating your own buildout.cfg and re-running buildout -N.

Examples in this package
------------------------

We do not have a single `static` directory. Instead, we have directories 
for each theme.

Themes:

`collective-xdv-example`: the example from the collective.xdv product.

Credits / Who to bug 
--------------------

Package created during the sprint after the Plone Conference 2010.

Team:

    - Jamie Lentin
    - Ken Wasetis
    - Laurence Rowe
    - Peter Uittenbroek
    - Kees Hink

.. _xdv-worked-example: http://pypi.python.org/pypi/collective.xdv#a-worked-example
