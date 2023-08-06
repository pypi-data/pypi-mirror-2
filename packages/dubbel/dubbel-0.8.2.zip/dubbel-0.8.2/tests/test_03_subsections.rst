
Parsing Subsections
===================


Import::

    >>> from dubbel import DubbelParser

Create a parser instance::

    >>> config = DubbelParser()

add a section::

    >>> config.add_section('sphinx.en')

An empty default section has been implicitly added::

    >>> config.has_section('sphinx')
    True

Add an option to the section::

    >>> config.set('sphinx.en', 'x', '3')

write the result::

    >>> import sys
    >>> config.write(sys.stdout)
    [sphinx -> en]
    x: '3'
    <BLANKLINE>

Defaults
--------

Add default options::

    >>> config.set('sphinx', 'y', '7')
    >>> config.set('sphinx', 'x', '7')

Subsection can access default::

    >>> config.has_option('sphinx.en', 'y')
    True
    >>> config.get('sphinx.en', 'y')
    '7'

but overidden value is intact::

    >>> config.get('sphinx.en', 'x')
    '3'

write the result::

    >>> config.write(sys.stdout)
    [sphinx]
    x: '7'
    y: '7'
    <BLANKLINE>
    [sphinx -> en]
    x: '3'
    <BLANKLINE>

Sections::

    >>> sorted(config.sections())
    ['sphinx', 'sphinx.en']

Options::

    >>> sorted(config.options('sphinx'))
    ['x', 'y']
    >>> sorted(config.options('sphinx.en'))
    ['x', 'y']

Items::

    >>> for item in sorted(config.items('sphinx')):
    ...     print item
    ...
    ('x', '7')
    ('y', '7')
    >>> for item in sorted(config.items('sphinx.en')):
    ...     print item
    ...
    ('x', '3')
    ('y', '7')

Subsections::

    >>> config.subsections('sphinx')
    ['sphinx.en']


File Example
------------

Create a parser::

    >>> config = DubbelParser()
    >>> config.read('examples/with_subsections.yaml')
    ['examples/with_subsections.yaml']

Create a dict from each subsection::

    >>> for document in sorted(config.subsections('sphinx')):
    ...     d = dict(config.items(document))
    ...     print d['project'], d['version']
    ...     print '   ', d['docroot']
    ...     print '   ', d['html_theme']
    ...     print '   ', d['master_doc']
    ...     print
    ...
    Worrp Documentation 1.0
        doc/maindocs
        scrolls
        contents
    <BLANKLINE>
    Worrp Tutorial 0.5
        doc/tutorial
        default
        index
    <BLANKLINE>


Nodes
-----

Leaf elements::

    >>> for key, data in sorted(config.nodes()):
    ...     print(key)
    ...     for item in sorted(data.iteritems()):
    ...         print('    %s = %s' % item)
    jekyll
        copyright = Jonathon J. Jaffa
        days = 100
    sphinx.maindocs
        docroot = doc/maindocs
        html_theme = scrolls
        master_doc = contents
        project = Worrp Documentation
        rst_suffix = rst
        version = 1.0
    sphinx.tutorial
        docroot = doc/tutorial
        html_theme = default
        master_doc = index
        project = Worrp Tutorial
        rst_suffix = rst
        version = 0.5

    >>> for key, data in sorted(config.nodes('sphinx')):
    ...     print(key)
    ...     for item in sorted(data.iteritems()):
    ...         print('    %s = %s' % item)
    sphinx.maindocs
        docroot = doc/maindocs
        html_theme = scrolls
        master_doc = contents
        project = Worrp Documentation
        rst_suffix = rst
        version = 1.0
    sphinx.tutorial
        docroot = doc/tutorial
        html_theme = default
        master_doc = index
        project = Worrp Tutorial
        rst_suffix = rst
        version = 0.5




