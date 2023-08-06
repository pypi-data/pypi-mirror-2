==========================
DSE - Delayed SQL Executor
==========================

Version : 0.3.0
Author : Thomas Weholt <thomas@weholt.org>
License : GPL v3.0
Status : Beta

Background
==========

A way to solve a recurring problem when using the Django ORM; how to insert or update a bunch of
records without the huge performance hit of using the ORM to do it, for instance when you want to
scan a filesystem and add or update a record for each file found.

It has been designed to be used outside Django as well, but the main focus is good Django ORM integration.
It takes care of getting default-values specified in the model as well, both plain values and callables.
Just don`t specify a value in the dictionary to addItem() and the default value will be used in inserts.

If a key in the dictionary is similar to the primary key of the table related to the model it will result
in an update being executed, ie. in most cases, if the dictionary contains a key called "id", it will
be interpreted as an update.

When calling addItem(dict) you put the dict in a cache. When the cache reaches a specified number of elements
or close()/flush() is called a cursor.executemany(cache) will be called and the cache will be cleared. 

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

    dex = dse.ModelDelayedExecutor(foobar)
    dex.addItem({'name': 'Thomas', 'age': 36, 'sex': 'M'})
    dex.addItem({'name': 'Tom', 'age': 30, 'sex': 'M'})
    dex.addItem({'name': 'Claire', 'age': 27, 'sex': 'F'})
    dex.addItem({'name': 'John'}) # using the default values for age ( 20 ) and sex ( "M" )
    dex.addItem({'id': 1, 'name': 'John'}) # this will result in an update
    dex.close()

Say you want to update all records with some calculated value, something you couldn`t find a way to do in SQL.
Using dse this is easy and fast::

    dex = dse.ModelDelayedExecutor(foobar)
    for item in dex.getItems(): # you can add an where-clause to getItems, ex. getItems('age between 10 and 30', order_by = 'age')
        item['somevar'] = calculated_value
        dex.addItem(item)
    dex.close()