Introduction
============

get the FastmemberpropertiesTool
-----------------------------------

    fmp_tool = queryUtility(IFastmemberpropertiesTool, 'fastmemberproperties_tool')


get a list of all memberproperties
----------------------------------

    member_props = fmp_tool.get_all_memberproperties()


    >>> props = fmp_tool.get_all_memberproperties()
    >>> props
    <persistent.dict.PersistentDict object at 0xd9f8e6c>

    >>> props.items()
    [('maik', <persistent.dict.PersistentDict object at 0xd9fe56c>)]

    >>> props.keys()
    ['maik']

    >>> props['maik']
    <persistent.dict.PersistentDict object at 0xd9fe56c>

    >>> pp(props['maik'].items())
    [('visible_ids', 0),
     ('last_login_time', DateTime('2000/01/01')),
     ('language', ''),
     ('home_page', ''),
     ('listed', 'on'),
     ('wysiwyg_editor', 'Kupu'),
     ('error_log_update', 0.0),
     ('location', ''),
     ('portal_skin', ''),
     ('fullname', 'Maik Derstappen 2'),
     ('login_time', DateTime('2000/01/01')),
     ('email', 'maik.derstappen@derstappen-it.de'),
     ('ext_editor', ''),
     ('description', '')]


or get properties for one member by id
--------------------------------------

    member_props = fmp_tool.get_properties_for_member('example_member')

