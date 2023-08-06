==========================
DSE - Delayed SQL Executor
==========================

Version : 0.3.1
Author : Thomas Weholt <thomas@weholt.org>
License : GPL v3.0
Status : Beta

Background
==========

DSE is concept of caching SQL-statements, both inserts and updates, and executing them when a specified 
number of statements has been prepared. This is done using DB API cursor.executemany(list of cached statements)
and this is way faster than executing SQL-statements in sequence.

DSE also is a way to solve a recurring problem when using the Django ORM; how to insert or update a bunch of
records without the huge performance hit of using the ORM to do it, for instance when you want to
scan a filesystem and add or update a record for each file found.

It has been designed to be used outside Django as well, but the main focus is good Django integration.

A prepared parameter based SQL-statement is built based on the structure/schema of the table in the database 
 or the model when using Django. To update or insert a record you add a plain dictionary with keys 
corresponding to fields in a table/model to DSE using the add_item()-method. You only add values you want 
to update and/or values for any required field. DSE also handles getting any defined default value from a model.

If a key in the dictionary is similar to the primary key of the table it will result in an update being executed, 
ie. in most cases using Django, if the dictionary contains a key called "id", it will be interpreted as an update.

When calling add_item(dict) you put the dict in a cache. When the cache reaches a specified number of elements
or close()/flush() is called a cursor.executemany(cache) will be called and the cache will be cleared. 

By default no SQL-statements will be executed until 1000 elements are cached or the flush/close-method is called.
You can use another cache limit when you create a DSE instance, like so ::

    import dse
    dex = dse.ModelDelayedExecutor(djangomodel, item_limit = 5000)

NOTE! This is still more of a proof-of-concept type of code and I`d like to get comments, warnings and
suggestions on how to improve it. It has been tested on Sqlite3 so far without problems. The code needs
clean-up and documentation. I`ve got a testsuite running, but haven`t found a way to get it included in the
setup.py file. I`ll try to add it in the next release.

Example usage
=============

You got a model called foobar in an app called someapp, looking like::

    #!/usr/bin/env python
    class foobar(models.Model):
        name = models.CharField(max_length = 200)
        age = models.IntegerField(default = 20)
        sex = models.CharField(max_length = 1, choices = (('F', 'F'), ('M', 'M')), default = "M")

    import dse
    from someapp.models import foobar

    # Constructing a DSE-object based in the foobar-model:
    dex = dse.ModelDelayedExecutor(foobar)

    # Adding a new item, just defining a name and using the default values from the model:
    dex.add_item({'name': 'John'})

    # Overriding the default values? Just specify a valid value
    dex.add_item({'name': 'Thomas', 'age': 36, 'sex': 'M'})

    # Update record with id = 1 and set its name to John:
    dex.add_item({'id': 1, 'name': 'John'}) 

    # Calling close() will trigger executing all prepared SQL-statements
    dex.close()


Say you want to update all records with some calculated value, something you couldn`t find a way to do in SQL.
Using dse this is easy and fast::

    dex = dse.ModelDelayedExecutor(foobar)
    # Use Djangos ORM to generate dictionaries to use in DSE; objects.all().values().
    for item in foobar.objects.all().values():
        item['somevar'] = calculated_value
        dex.add_item(item)
    dex.close()