
Interpolation
=============

Import dubbelParser::

    >>> from dubbel import DubbelParser

Create a parser instance with defaults::

    >>> defaults = {}
    >>> defaults['VERSION'] = '0.1'
    >>> defaults['AUTHOR'] = '${APPELLATION} Jonah J. Jameson'
    >>> defaults['APPELLATION'] = 'Mr.'
    >>> parser = DubbelParser(defaults)

add a section::

    >>> parser.add_section('main')

add an option to the section::

    >>> parser.set('main', 'title', 'Document v${VERSION} by ${AUTHOR}')
    >>> parser.set('main', 'description', '$title - includes latest findings')

write the result::

    >>> import sys
    >>> parser.write(sys.stdout)
    APPELLATION: Mr.
    AUTHOR: ${APPELLATION} Jonah J. Jameson
    VERSION: '0.1'
    <BLANKLINE>
    [main]
    description: $title - includes latest findings
    title: Document v${VERSION} by ${AUTHOR}
    <BLANKLINE>

Interpolate::

    >>> cfg = parser.fill()

New values::

    >>> cfg.get('main', 'title')
    'Document v0.1 by Mr. Jonah J. Jameson'
    >>> cfg.get('main', 'description')
    'Document v0.1 by Mr. Jonah J. Jameson - includes latest findings'

Update values::

    >>> parser.set('', 'VERSION', '0.2')
    >>> parser.set('main', 'description', 'All about funambulators by $AUTHOR')

Interpolate::

    >>> cfg = parser.fill(APPELLATION='Dr')

New values::

    >>> cfg.write(sys.stdout)
    APPELLATION: Dr
    AUTHOR: Dr Jonah J. Jameson
    VERSION: '0.2'
    <BLANKLINE>
    [main]
    description: All about funambulators by Dr Jonah J. Jameson
    title: Document v0.2 by Dr Jonah J. Jameson
    <BLANKLINE>

and the derived values are also updated::

    >>> cfg.get('main', 'title')
    'Document v0.2 by Dr Jonah J. Jameson'
    >>> cfg.get('main', 'description')
    'All about funambulators by Dr Jonah J. Jameson'

Items
-----

Items are correctly interpolated::

    >>> for item in sorted(cfg.items('main')):
    ...     print("%s -> %s" % item)
    ...
    APPELLATION -> Dr
    AUTHOR -> Dr Jonah J. Jameson
    VERSION -> 0.2
    description -> All about funambulators by Dr Jonah J. Jameson
    title -> Document v0.2 by Dr Jonah J. Jameson

with no effect on original data::

    >>> parser.write(sys.stdout)
    APPELLATION: Mr.
    AUTHOR: ${APPELLATION} Jonah J. Jameson
    VERSION: '0.2'
    <BLANKLINE>
    [main]
    description: All about funambulators by $AUTHOR
    title: Document v${VERSION} by ${AUTHOR}
    <BLANKLINE>
