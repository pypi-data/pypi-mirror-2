
Root level defaults
-------------------

Create a parser::

    >>> from dubbel import DubbelParser
    >>> config = DubbelParser()
    >>> config.read('examples/root_level_defaults.yaml')
    ['examples/root_level_defaults.yaml']

Defaults::

    >>> for key in sorted(config.defaults().keys()):
    ...     print(key)
    ...
    copyright
    date

All sections have these defaults::

    >>> for section in sorted(config.sections()):
    ...     assert config.has_option(section, 'copyright'), section
    ...     assert config.has_option(section, 'date'), section
    ...

options::

    >>> sorted(config.options('jekyll'))
    ['copyright', 'date', 'days']
    >>> sorted(config.options('sphinx.tutorial.fr')) #doctest: +ELLIPSIS
    ['copyright', 'date', 'docroot', 'html_theme', ...]

items::

    >>> sorted(config.items('jekyll'))
    [('copyright', 'Jonathon J. Jaffa'), ('date', '32nd Julember 3001'), ('days', 100)]
    >>> for item in sorted(config.items('sphinx.tutorial.en')):
    ...     print item
    ('copyright', 'Jonathon J. Jaffa')
    ('date', '32nd Julember 3001')
    ('docroot', 'doc/tutorial/en')
    ('html_theme', 'default')
    ('master_doc', 'index')
    ('project', 'Worrp Tutorial')
    ('rst_suffix', 'rst')
    ('version', 0.5)

get::

    >>> config.get('jekyll', 'copyright')
    'Jonathon J. Jaffa'
    >>> config.get('sphinx.tutorial.en', 'copyright')
    'Jonathon J. Jaffa'
    >>> config.get('sphinx.maindocs', 'copyright')
    'Jonathon J. Jaffa'

cannot remove option from section directly::

    >>> config.remove_option('sphinx.maindocs', 'copyright')
    False
    >>> config.get('sphinx.maindocs', 'copyright')
    'Jonathon J. Jaffa'

must remove from root level defaults::

    >>> config.remove_option('', 'copyright')
    True
    >>> config.get('sphinx.maindocs', 'copyright')
    Traceback (most recent call last):
        ...
    NoOptionError: No option 'copyright' in section: 'sphinx'

add it back::

    >>> config.set('', 'copyright', 'Jonathon J. Jaffa')
    >>> config.get('sphinx.maindocs', 'copyright')
    'Jonathon J. Jaffa'


Defaults are preserved when rewritten::

    >>> import sys
    >>> config.write(sys.stdout)
    copyright: Jonathon J. Jaffa
    date: 32nd Julember 3001
    <BLANKLINE>
    [jekyll]
    days: 100
    <BLANKLINE>
    [sphinx]
    html_theme: default
    master_doc: contents
    rst_suffix: rst
    <BLANKLINE>
    [sphinx -> maindocs]
    docroot: doc/maindocs
    html_theme: scrolls
    project: Worrp Documentation
    version: 1.0
    <BLANKLINE>
    [sphinx -> tutorial]
    master_doc: index
    version: 0.5
    <BLANKLINE>
    [sphinx -> tutorial -> en]
    docroot: doc/tutorial/en
    project: Worrp Tutorial
    <BLANKLINE>
    [sphinx -> tutorial -> fr]
    docroot: doc/tutorial/fr
    html_theme: haiku
    master_doc: master
    project: "Worrp Tutori\xE9l"
    <BLANKLINE>
    [yuidoc]
    main_title: API Documentation
    <BLANKLINE>




