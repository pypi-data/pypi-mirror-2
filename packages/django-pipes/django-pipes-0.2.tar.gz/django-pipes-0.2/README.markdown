django-pipes
============

This module offers a nice API to access remote JSON resources from within your Django applications. The API is intentionally kept as close as possible to the Django DB-API. So accessing data from a remote JSON API should feel just like an attempt to fetch the data from a database. It is inspired by Ruby on Rails' ActiveResource library.

Author: *Harish Mallipeddi* (harish.mallipeddi@gmail.com)

### NOTE ###

* `pipes` has been renamed to `django_pipes` because `pipes` conflicts with a module's name that ships with the Python distribution by default. You could do something like `import django_pipes as pipes` in your code.
