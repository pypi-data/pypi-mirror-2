
DubbelParser Basics
===================

Import DubbelParser::

    >>> from dubbel import DubbelParser

Creating
--------

Create a parser instance::

    >>> config = DubbelParser()

add a section::

    >>> config.add_section('main')

add an option to the section::

    >>> config.set('main', 'x', '1')

write the result::

    >>> import sys
    >>> config.write(sys.stdout)
    [main]
    x: '1'
    <BLANKLINE>

Reading
-------

Create a parser instance::

    >>> config = DubbelParser()

read from a stream::

    >>> from cStringIO import StringIO
    >>> config.readfp(StringIO("""
    ... [main]
    ... y : two
    ... """))
    ...

write the result::

    >>> config.write(sys.stdout)
    [main]
    y: two
    <BLANKLINE>


Updating
--------

Add further option::

    >>> config.set('main', 'x', 1)

write the result::

    >>> config.write(sys.stdout)
    [main]
    x: 1
    y: two
    <BLANKLINE>

Update existing option::

    >>> config.get('main', 'y')
    'two'
    >>> config.set('main', 'y', 'three')
    >>> config.get('main', 'y')
    'three'

write the result::

    >>> config.write(sys.stdout)
    [main]
    x: 1
    y: three
    <BLANKLINE>


Complex Example
---------------

Input::

    >>> example = StringIO("""
    ...
    ... [character-01]
    ...
    ...     name: Vorlin Laruknuzum
    ...     sex: Male
    ...     class: Priest
    ...     title: Acolyte
    ...     hp: [32, 71]
    ...     sp: [1, 13]
    ...     gold: 423
    ...     inventory:
    ...     - a Holy Book of Prayers (Words of Wisdom)
    ...     - an Azure Potion of Cure Light Wounds
    ...     - a Silver Wand of Wonder
    ...
    ... [character-02]
    ...
    ...     name: Rumpel Stilskin
    ...     sex: Male
    ...     class: Wizard
    ...     title: Dr. R. Stilskin MPhil Phd
    ...     hp: [12, 33]
    ...     sp: [15, 15]
    ...     gold: 1423
    ...     inventory:
    ...     - this
    ...     - that
    ...     - the other
    ...     spells:
    ...         level1:
    ...         - Knock
    ...         - Wizard's eye
    ...         level2:
    ...         - Find Trap
    ...         - Shield
    ...
    ... """)
    ...

Create an instance::

    >>> config = DubbelParser()

read input::

    >>> config.readfp(example)

write the result::

    >>> config.write(sys.stdout)
    [character-01]
    class: Priest
    gold: 423
    hp:
    - 32
    - 71
    inventory:
    - a Holy Book of Prayers (Words of Wisdom)
    - an Azure Potion of Cure Light Wounds
    - a Silver Wand of Wonder
    name: Vorlin Laruknuzum
    sex: Male
    sp:
    - 1
    - 13
    title: Acolyte
    <BLANKLINE>
    [character-02]
    class: Wizard
    gold: 1423
    hp:
    - 12
    - 33
    inventory:
    - this
    - that
    - the other
    name: Rumpel Stilskin
    sex: Male
    sp:
    - 15
    - 15
    spells:
      level1:
      - Knock
      - Wizard's eye
      level2:
      - Find Trap
      - Shield
    title: Dr. R. Stilskin MPhil Phd
    <BLANKLINE>

Update nested property::

    >>> config.get('character-01', 'hp')
    [32, 71]
    >>> config.get('character-01', 'hp')[0] = 42
    >>> config.get('character-01', 'hp')[1] = 42
    >>> config.get('character-01', 'hp')
    [42, 42]
    >>> config.get('character-02', 'spells')['level2'][0]
    'Find Trap'
    >>> config.get('character-02', 'spells')['level2'][0] = 'Fireball'
    >>> config.get('character-02', 'spells')['level2'][0]
    'Fireball'

write the result::

    >>> config.write(sys.stdout)
    [character-01]
    class: Priest
    gold: 423
    hp:
    - 42
    - 42
    inventory:
    - a Holy Book of Prayers (Words of Wisdom)
    - an Azure Potion of Cure Light Wounds
    - a Silver Wand of Wonder
    name: Vorlin Laruknuzum
    sex: Male
    sp:
    - 1
    - 13
    title: Acolyte
    <BLANKLINE>
    [character-02]
    class: Wizard
    gold: 1423
    hp:
    - 12
    - 33
    inventory:
    - this
    - that
    - the other
    name: Rumpel Stilskin
    sex: Male
    sp:
    - 15
    - 15
    spells:
      level1:
      - Knock
      - Wizard's eye
      level2:
      - Fireball
      - Shield
    title: Dr. R. Stilskin MPhil Phd
    <BLANKLINE>

