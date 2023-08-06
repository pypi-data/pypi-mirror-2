
Parsing a pure YAML file
========================

Create DubbelParser::

    >>> from dubbel import DubbelParser
    >>> config = DubbelParser()

Read from existing YAML::

    >>> fp = open('examples/strict_yaml.yaml')
    >>> try:
    ...     config.readfp(fp)
    ... finally:
    ...     fp.close()
    ...

Inspect::

    >>> config.sections()
    []

    >>> sorted(config.options())
    ['class', 'gold', 'hp', 'inventory', 'name', 'sex', 'sp', 'spells', 'title']

    >>> for item in sorted(config.items()):
    ...     print(item)
    ...
    ('class', 'Wizard')
    ('gold', 1423)
    ('hp', [12, 33])
    ('inventory', ['this', 'that', 'the other'])
    ('name', 'Rumpel Stilskin')
    ('sex', 'Male')
    ('sp', [15, 15])
    ('spells', {'level1': ['Knock', "Wizard's eye"], 'level2': ['Find Trap', 'Shield']})
    ('title', 'Dr. R. Stilskin MPhil Phd')

    >>> nodes = list(config.nodes())
    >>> len(nodes)
    1
    >>> key, info = nodes[0]
    >>> key
    ''
    >>> for item in sorted(info.iteritems()):
    ...     print('%s -> %s' % item)
    class -> Wizard
    gold -> 1423
    hp -> [12, 33]
    inventory -> ['this', 'that', 'the other']
    name -> Rumpel Stilskin
    sex -> Male
    sp -> [15, 15]
    spells -> {'level1': ['Knock', "Wizard's eye"], 'level2': ['Find Trap', 'Shield']}
    title -> Dr. R. Stilskin MPhil Phd

