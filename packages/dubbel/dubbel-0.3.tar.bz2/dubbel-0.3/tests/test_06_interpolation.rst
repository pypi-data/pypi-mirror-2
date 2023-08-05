
Interpolating Parser
====================

Import DubbelParser::

    >>> from dubbel import InterpolatingDubbelParser

Create a parser instance with defaults::

    >>> defaults = {}
    >>> defaults['VERSION'] = '0.1'
    >>> defaults['AUTHOR'] = '${APPELLATION} Jonah J. Jameson'
    >>> defaults['APPELLATION'] = 'Mr.'
    >>> config = InterpolatingDubbelParser(defaults)

add a section::

    >>> config.add_section('main')

add an option to the section::

    >>> config.set('main', 'title', 'Document v${VERSION} by ${AUTHOR}')
    >>> config.set('main', 'description', '$title - includes latest findings')

write the result::

    >>> import sys
    >>> config.write(sys.stdout)
    APPELLATION: Mr.
    AUTHOR: ${APPELLATION} Jonah J. Jameson
    VERSION: '0.1'
    <BLANKLINE>
    [main]
    description: $title - includes latest findings
    title: Document v${VERSION} by ${AUTHOR}
    <BLANKLINE>

Interpolation of values::

    >>> config.get('main', 'title')
    'Document v0.1 by Mr. Jonah J. Jameson'
    >>> config.get('main', 'description')
    'Document v0.1 by Mr. Jonah J. Jameson - includes latest findings'

Update values::

    >>> config.set('', 'VERSION', '0.2')
    >>> config.set('main', 'description', 'All about funambulators by $AUTHOR')
    >>> config.write(sys.stdout)
    APPELLATION: Mr.
    AUTHOR: ${APPELLATION} Jonah J. Jameson
    VERSION: '0.2'
    <BLANKLINE>
    [main]
    description: All about funambulators by $AUTHOR
    title: Document v${VERSION} by ${AUTHOR}
    <BLANKLINE>

and the derived values are also updated::

    >>> config.get('main', 'title')
    'Document v0.2 by Mr. Jonah J. Jameson'
    >>> config.get('main', 'description')
    'All about funambulators by Mr. Jonah J. Jameson'

Items
-----

Items are correctly interpolated::

    >>> for item in sorted(config.items('main')):
    ...     print("%s -> %s" % item)
    ...
    APPELLATION -> Mr.
    AUTHOR -> Mr. Jonah J. Jameson
    VERSION -> 0.2
    description -> All about funambulators by Mr. Jonah J. Jameson
    title -> Document v0.2 by Mr. Jonah J. Jameson

with no effect on underlying data::

    >>> config.write(sys.stdout)
    APPELLATION: Mr.
    AUTHOR: ${APPELLATION} Jonah J. Jameson
    VERSION: '0.2'
    <BLANKLINE>
    [main]
    description: All about funambulators by $AUTHOR
    title: Document v${VERSION} by ${AUTHOR}
    <BLANKLINE>
