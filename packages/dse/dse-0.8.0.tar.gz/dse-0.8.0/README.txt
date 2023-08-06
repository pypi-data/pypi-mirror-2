=DSE - Delayed SQL Executor=

Version : 0.8.0
Author : Thomas Weholt <thomas@weholt.org>
License : GPL v3.0
Status : Beta
Url : https://bitbucket.org/weholt/dse
Docs at http://readthedocs.org/docs/dse/en/latest/index.html

==Background==

DSE is concept of caching SQL-statements, both inserts and updates, and executing them when a specified
number of statements has been prepared. This is done using DB API cursor.executemany(list of cached statements)
and this is way faster than executing SQL-statements in sequence.

DSE also is a way to solve a recurring problem when using the Django ORM; how to insert or update a bunch of
records without the huge performance hit of using the ORM to do it, for instance when you want to
scan a filesystem and add or update a record for each file found.

It has been designed to be used outside Django as well, but the main focus is good Django integration.

==Release notes==

0.8.0 : - fixed crash when more than one database connection has been configured. No ModelFactory will be triggered.

0.7.0 : - don`t remember.

0.6.0 : - added support for the with-statement.
        - added an ModelDelayedExecutor-instance to each model, so you can do Model.dse.add_item
          instead of dse.ModelFactory.Model.add_item.
        - renamed dse.modelfactory to dse.ModelFactory to be more style-compliant.

0.5.1 : just some notes on transaction handling.

0.5.0 :
    - added modelfactory. Upon first import a modelfactory will be created in the DSE module. It`s basically just a
    helper-class containing ModelDelayedExecutor-instances for all models in all apps found in INSTALLED_APPS in
    settings.py.
    - to change the default item limit before automatic execution of cached SQL statements to 10000 instead of the default 1000::

    import dse
    dse.ITEM_LIMIT = 10000

0.4.0 :
    - fixed serious bug when using mass updates. Using cursor.executemany is only possible when values
    for all columns are specified. If only values for a subset of the columns is specified that will be
    executed as a seperate SQL-call. NOTE! Using dex.get_items() or Djangos Model.objects.values() will give you
    all the fields.
    - code clean-up.
    - added custom exceptions; UpdateManyException, UpdateOneException and InsertManyException.
