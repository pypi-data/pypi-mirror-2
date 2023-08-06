
Test Interpolation
==================

Create a DubbelParser instance::

    >>> from dubbel import DubbelParser
    >>> from cStringIO import StringIO
    >>> parser = DubbelParser()
    >>> parser.readfp(StringIO("""
    ... 
    ... copyright: Jonathon J. Jaffa
    ... date: 32nd Julember 3001
    ... project: worrp
    ... 
    ... [sphinx]
    ... 
    ...     master_doc: contents
    ...     rst_suffix: rst
    ...     default_sidebar: nav.html
    ...     html:
    ...         theme: default
    ...         title: Worrp Documentation
    ... 
    ... [sphinx -> tutorial]
    ... 
    ...     version: 0.5
    ...     master_doc: index
    ...     html:
    ...         sidebars:
    ...             - localtoc.html
    ...             - search.html
    ...             - $default_sidebar
    ... 
    ... [sphinx -> tutorial -> en]
    ... 
    ...     docroot: doc/tutorial/en
    ...     master_doc: master
    ...     html:
    ...         theme: haiku
    ...         title: Worrp Tutorial (version $version)
    ... 
    ... [sphinx -> maindocs]
    ... 
    ...     html:
    ...         theme: scrolls
    ...     version: 1.0
    ...     docroot: doc/maindocs
    ... 
    ... """))
    ...

(Helper)::

    >>> def sprint(key, val, indent=0):
    ...     if hasattr(val, '__iter__'):
    ...         val = sorted(val)
    ...     print("%s%s = %s" % (indent*' ', key, val))
    ...

Interpolate::

    >>> config = parser.fill()

Print::

    >>> for name, node in config.nodes('sphinx'):
    ...     print(name)
    ...     for key in sorted(node.keys()):
    ...         val = node[key]
    ...         if hasattr(val, 'keys'):
    ...             print("    %s:" % key)
    ...             for subkey in sorted(val.keys()):
    ...                 sprint(subkey, val[subkey], 8)
    ...         else:
    ...             sprint(key, node[key], 4)
    ...
    sphinx.tutorial.en
        copyright = Jonathon J. Jaffa
        date = 32nd Julember 3001
        default_sidebar = nav.html
        docroot = doc/tutorial/en
        html:
            sidebars = ['localtoc.html', 'nav.html', 'search.html']
            theme = haiku
            title = Worrp Tutorial (version 0.5)
        master_doc = master
        project = worrp
        rst_suffix = rst
        version = 0.5
    sphinx.maindocs
        copyright = Jonathon J. Jaffa
        date = 32nd Julember 3001
        default_sidebar = nav.html
        docroot = doc/maindocs
        html:
            theme = scrolls
            title = Worrp Documentation
        master_doc = contents
        project = worrp
        rst_suffix = rst
        version = 1.0

