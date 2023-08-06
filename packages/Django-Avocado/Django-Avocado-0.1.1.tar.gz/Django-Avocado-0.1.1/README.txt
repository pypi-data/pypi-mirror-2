Avacado
=======

Version : 0.1.1
Author : Thomas Weholt <thomas@weholt.org>
License : GPL v3.0
WWW : https://bitbucket.org/weholt/django-avacado
Status : Experimental/Alpha/Proof-of-concept.


About
-----
Deliciously delayed and cached database logging for django.

FYI: The code is still in early alpha stage of development so beware.

NB! It sorta looks like the std module logger in python, but it's not.
This is that one time that even if it looks like a duck and quacks like a duck, 
it's still not a duck.

The code has so far only been tested using SQLite, Django 1.3, Python 2.6.6 on
Ubuntu 10.10.

Usage
-----
Avocado is meant to be used when you want to log huge amounts of log entries
related to the same context, store the log in the db for easy sorting and viewing,
and not have the performance hit of using the django orm.

You might do something like this in your view::

    from avocado.context import get_context
    
    with get_context("filescanning") as log:
        for filename in somefilescanningmethod():
            # do something with the file and store some information about it
            log.info("Did something to %s." % filename)
        
You can also log information and add an instance of a django model. In the admin
you can see the log and click to go directly to the related model::

    with get_context("UserProcessing") as log:
        for usr in User.objects.all():
            # do something with the user and store some information about it
            log.info("Did something to %s." % user, instance=user)


You can also log exceptions and avocado will try to log more than just the name
of the exception being raised, but this not formatted very pretty at the moment
and the code seems to bring along a lot of useless info. Still, here's how to test it::

    with get_context("UserProcessing") as log:
        try:
            a = 0
            b = 2
            c = b / a
        except Exception, e:
            log.exception("Math exception: %s" % e)
        
You don't have to pass the exception along. Avocado will dig out lots of stuff for you.


Installation
------------

pip install django-avocado

or

hg clone https://bitbucket.org/weholt/django-avacado
python setup.py install

Add avocado to INSTALLED_APPS. You might have to copy or symlink to the templates
in the avocado-folder, but I don't think so.


Requirements
------------
* django
* dse
