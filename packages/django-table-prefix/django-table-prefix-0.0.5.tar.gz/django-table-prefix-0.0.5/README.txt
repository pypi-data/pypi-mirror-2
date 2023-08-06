===========
django-table-prefix
===========

django-table-prefix provides experimental ability to set your own
database table prefixes for django project this app is included in
Include this app into your project's settings.py, provide table prefix
name and list of models (optional) for ommiting prefix usage::

    INSTALLED_APPS = (
        ... # your regular stuff
        'table_prefix',
    )

    # table prefix name
    DB_PREFIX = 'nifty_prefix'

    # omit prefixing tables for these models
    OMIT_MODELS = (
        '<app_name>.<model class name>',
    )
