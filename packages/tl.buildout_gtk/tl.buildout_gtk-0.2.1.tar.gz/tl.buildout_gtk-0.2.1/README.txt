===============
tl.buildout_gtk
===============

A `zc.buildout`_ recipe for installing pygtk, including pygobject and pycairo,
and optionally pywebkitgtk.

This recipe concerns itself with the Python bindings to the named projects. It
assumes that the C libraries are available on the system already, along with
their header files. The bindings' versions built by default require Python 2.6
or greater.

This recipe appears to be reliable, but the feature set is basically
determined by the author's immediate needs. Don't hesitate to send questions,
bug reports, suggestions, or patches to <thomas@thomas-lotze.de>.


Options
=======

Configuration options:
    :shared:
        Configure shared builds like with the `zc.recipe.cmmi`_ recipe.
        Defaults to using automatically located shared builds.

    :pycairo-url:
        URL of the pycairo source code archive.

    :pycairo-md5sum:
        MD5 checksum of the pycairo source code archive.

    :pygobject:
        Set to ``false`` in order not to build pygobject. If pygtk is to be
        built, pygobject will be built regardless of this option.

    :pygobject-url:
        URL of the pygobject source code archive.

    :pygobject-md5sum:
        MD5 checksum of the pygobject source code archive.

    :pygtk:
        Set to ``false`` in order not to build pygtk. If pywebkitgtk is to be
        built, pygtk will be built regardless of this option.

    :pygtk-url:
        URL of the pygtk source code archive.

    :pygtk-md5sum:
        MD5 checksum of the pygtk source code archive.

    :pywebkitgtk:
        Set to ``true`` in order to build pywebkitgtk. Doing so will cause
        pygtk and pygobject to be built.

    :pywebkitgtk-url:
        URL of the pywebkitgtk source code archive.

    :pywebkitgtk-md5sum:
        MD5 checksum of the pywebkitgtk source code archive.

    The default values of these options correspond to recent project versions
    at the time the recipe was released.

Exported options:
    :location:
        Location of the buildout part containing the compiled Python bindings.

    :path:
        Filesystem path to be added to the Python path in order for the
        bindings to be importable. This may be included in a zc.recipe.egg
        part's ``extra-paths`` option, for example.


Background
==========

There are two reasons for the existence of this recipe: setting up the build
environment for pygtk & friends, and tying together the build instructions of
the related projects for convenience.

The pywebitgtk, pygtk, pygobject and pycairo projects are built using a
standard configure/make/make install procedure. The recipe sets up the build
environment such that the bindings are built for the right Python installation
and against the right builds of each other.


.. _`zc.buildout`: http://www.zope.org/DevHome/Buildout/

.. _`zc.recipe.cmmi`: http://pypi.python.org/pypi/zc.recipe.cmmi


.. Local Variables:
.. mode: rst
.. End:
