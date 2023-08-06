.. contents:: **Table of contents**

Main idea
=========

Old `Zope2`__  products were heavily based on *skins* resources. A lot of additional information for those
resources are taken from ``.metadata`` file, so commonly if you have a::

    my_icon.gif

...you will want to have also a::

    my_icon.gif.metadata

In old Zope/Plone installation (let me say "before Varnish begin to be a Plone standard") you can use those
metadata for performing associations with *HttpCache* objects, making the user browser to perform some
cache of resources::

    [default]
    title=my_icon.gif
    cache=HTTPCache

__ http://zope.org/

zopemetadatamaker
=================

This product will install for you a new executable: ``zopemetadatamaker``. Using this you can automatically create
your ``.metadata`` files. when you have a lot of static images, css and javascript files this can save you some times,
for example: you downloaded a big Javascript library with a lot of sub-directories inside and other related resources.

How to use
----------

The basic use of the command is something like this::

    zopemetadatamaker *.gif

This will create for you all ".metadata" related to all gif file found in the current directory. You need to know that:

* you must provide at least one filter patters
* the directory where files are searched is the current working directory (but you can customize this, see below).

Complete list of options
------------------------

Here the full documentation::

    Usage: zopemetadatamaker [options] pattern [patterns]

    Bulk creation of .metadata files for Zope skins resources

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -c METADATA, --content=METADATA
                            choose a metadata text different from default; use
                            quoting for multiline input
      -d, --default         print default metadata (if --content is not provided),
                            then exit
      -p PATHS, --path=PATHS
                            directories path where to look for metadata. You can
                            use this multiple times. Default is the current
                            working directory
      --dry-run             dry run, simply print what I would like to do
      -f, --force           force .metadata creation; if another one exists it
                            will be replaced
      -r, --recursive       search and create recursively inside subdirs

What to put in the .metadata content
------------------------------------

The default metadata content is like this::

    [default]
    title=%(filename)s
    cache=HTTPCache

The ``%(filename)s`` section will be replaced with the original file name. You can use this, or omit it, when
defining you custom ``.metadata``.

I use this default content because it is the minimal "cache" information for `Plone CMS`__ static resouces.

__ http://plone.org/

