
Test additional methods of underlying RawConfigParser
-----------------------------------------------------

Import::

    >>> from dubbel import DubbelParser

Filename read::

    >>> config = DubbelParser()
    >>> config.read('does-not-exist.yaml')
    []
    >>> config.read('examples/test.yaml')
    ['examples/test.yaml']

Sections::

    >>> sorted(config.sections())
    ['jekyll', 'sphinx']

Options::

    >>> sorted(config.options('jekyll'))
    ['copyright', 'days']
    >>> sorted(config.options('sphinx'))
    ['html_title', 'rst_suffix']
    >>> config.has_option('jekyll', 'copyright')
    True

Items::

    >>> for item in sorted(config.items('jekyll')):
    ...     print item
    ...
    ('copyright', 'Jonathon J. Jaffa')
    ('days', 100)


Non-strings are not interpolated::

    >>> config.get('jekyll', 'days')
    100

Nodes::

    >>> for key, data in sorted(config.nodes()):
    ...     print(key)
    ...     for item in sorted(data.iteritems()):
    ...         print('    %s -> %s' % item)
    jekyll
        copyright -> Jonathon J. Jaffa
        days -> 100
    sphinx
        html_title -> My Document
        rst_suffix -> rst




