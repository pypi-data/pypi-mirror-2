
=============
Configuration
=============

This section contains information about how to configure your Django projects
to use *django-primary-slug* and also contains a quick reference of the available
*settings* that can be used in order to customize the functionality of this
application.


Configuring your project
========================

In the Django project's ``settings`` module, add ``primary_slug`` to the
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'primary_slug',
    )


Reference of the application settings
=====================================

The following settings can be specified in the Django project's ``settings``
module to customize the functionality of *django-primary-slug*.

``PRIMARY_SLUG_SLUGIFY_FUNC``
    Set a function that should be used to produce the slug. By default,
    ``primary_slug.utils.simple_slugify`` is used.
``PRIMARY_SLUG_VALID_CHARS``
    A string containing all characters that should be valid for the slugfield.
    A properly decoded string is required if you use non-latin characters. Eg::
    
        PRIMARY_SLUG_VALID_CHARS = \
            '-_0-9a-zA-ZαβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩςάέήίϊΐόύϋΰώΆΈΉΊΪΌΎΫΏ'.decode('iso8859-7')


