Random Instances
====================================

This module exports a **get\_or\_create_random** function that improves Django's 
[get_or_create](http://djangoproject.com/documentation/models/get_or_create/)
on two aspects:

* invoking **get\_or\_create_random** with parameters that match MULTIPLE instances
does not raise an error, but rather returns one of those instances at random

* invoking **get\_or\_create_random** with parameters that do not match ANY instance
returns a NEW instance of that model (the same occurs with get_or_create). The
improvement is that **get\_or\_create_random** can be invoked without passing a value
for all the 'required' fields of the model. If these fields are not passed, 
they are automatically filled with random values (e.g.: CharFields are filled
with random strings, ImageFields with random images).

The goal is to make prototyping faster, as model instances can be obtained and 
created by specifying just the minimum set of desired fields. This is useful
when writing tests and can avoid having to write complex fixtures.

Installation
====================================

Download and install the package from GitHub, or do it the easy way:

    pip install random_instances

Example usages
====================================

Say you have the following **Subject** model defined in the **subjects** 
application, and no instances of Subject in the database:

    from django.db import models
    class Subject(models.Model):
        word             = models.CharField(unique=True, max_length=255)
        is_current       = models.BooleanField(default=False)

To get or create a random subject, type:

    from random_instances import get_or_create_random
    from subjects.models import Subject
    get_or_create_random(Subject)
    
This will generate an instance of Subject with the following values:

* word => a random string (no longer than 255 characters)
* is_current => a random Boolean value (True or False)

To get or create a subject with a specific value for the *word* field, type:

    get_or_create_random(Subject, word='Peace')

This will generate an instance of Subject with the following values:

* word => 'Peace'
* is_current => a random Boolean value (True or False)

To get a subject or create one with some *default* values, type:

    get_or_create_random(Subject, word='Peace', defaults={'is_current': True})

This will get a Subject instance with word='Peace', if any exists. 
Otherwise, a new one will be created with the following values:

* word => 'Peace'
* is_current => True

In short, **get\_or\_create_random** creates a new instance whenever an 
existing appropriate one cannot be found. The fields of the newly created 
instance are filled according to these ordered rules:

* if the field has been assigned a value in the function parameters, that value is used
* if the field is required (blank=False, null=False), a random value is used
* otherwise, the field is left unassigned


Testing and contributing
====================================

The module contains a suite of tests that can be executed by importing
random_instances into the INSTALLED\_APPS of a Django project and running:

    python manage.py test random_instances

To contribute to the module and report bugs, add the appropriate tests, check
that they pass, then send a pull request with the patch or the fixed bug.


To do
====================================

As of v0.0.2, add relationship fields (ForeignKey, ManyToMany, OneToOne) and
add tests to check that all the fields parameters are respected (e.g., maximum
length for CharField, number of digits for Decimals).


Acknowledgments
====================================

This project was partly inspired by [Dilla](https://github.com/beheadedmyway/dilla).
