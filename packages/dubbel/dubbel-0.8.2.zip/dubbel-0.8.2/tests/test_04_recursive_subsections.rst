
Recursive defaults
------------------

Create a parser::

    >>> from dubbel import DubbelParser
    >>> config = DubbelParser()
    >>> config.read('examples/with_subsubsections.yaml')
    ['examples/with_subsubsections.yaml']

Which nodes::

    >>> for key, data in sorted(config.nodes()):
    ...     print(key)
    ...     for k, v in sorted(data.iteritems()):
    ...         try:
    ...             v = v.encode('utf-8')
    ...         except AttributeError:
    ...             #not a string
    ...             pass
    ...         print('    %s = %s' % (k,v))
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
    sphinx.tutorial.en
        docroot = doc/tutorial/en
        html_theme = default
        master_doc = index
        project = Worrp Tutorial
        rst_suffix = rst
        version = 0.5
    sphinx.tutorial.fr
        docroot = doc/tutorial/fr
        html_theme = haiku
        master_doc = master
        project = Worrp Tutoriél
        rst_suffix = rst
        version = 0.5
    yuidoc
        main_title = API Documentation

    >>> for key, data in sorted(config.nodes('sphinx')):
    ...     print(key)
    ...     for k, v in sorted(data.iteritems()):
    ...         try:
    ...             v = v.encode('utf-8')
    ...         except AttributeError:
    ...             #not a string
    ...             pass
    ...         print('    %s = %s' % (k,v))
    sphinx.maindocs
        docroot = doc/maindocs
        html_theme = scrolls
        master_doc = contents
        project = Worrp Documentation
        rst_suffix = rst
        version = 1.0
    sphinx.tutorial.en
        docroot = doc/tutorial/en
        html_theme = default
        master_doc = index
        project = Worrp Tutorial
        rst_suffix = rst
        version = 0.5
    sphinx.tutorial.fr
        docroot = doc/tutorial/fr
        html_theme = haiku
        master_doc = master
        project = Worrp Tutoriél
        rst_suffix = rst
        version = 0.5

    >>> config.has_option('sphinx.tutorial.en', 'master_doc')
    True
    >>> config.has_option('sphinx.tutorial.en', 'rst_suffix')
    True

    >>> sorted(config.options('sphinx.tutorial.en'))
    ['docroot', 'html_theme', 'master_doc', 'project', 'rst_suffix', 'version']

    >>> config.get('sphinx.tutorial.en', 'rst_suffix')
    'rst'
    >>> config.get('sphinx.tutorial.en', 'html_theme')
    'default'
    >>> config.get('sphinx.tutorial.en', 'does_not_exist')
    Traceback (most recent call last):
        ...
    NoOptionError: No option 'does_not_exist' in section: 'sphinx'

    >>> for key, d in sorted(config.nodes('sphinx')):
    ...     print d['project'].encode('utf-8'), d['version']
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
        doc/tutorial/en
        default
        index
    <BLANKLINE>
    Worrp Tutoriél 0.5
        doc/tutorial/fr
        haiku
        master
    <BLANKLINE>



