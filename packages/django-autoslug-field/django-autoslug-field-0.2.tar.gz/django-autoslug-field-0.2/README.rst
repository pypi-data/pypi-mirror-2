######################
django-autoslug-field
######################

AutoSlugField for Django based on django-extensions AutoSlugField, adds option to track foreignkey/parent field for slug.

Installation
=============

Install django-autoslug-field like you would install any other pypi package::

    pip install django-autoslug-field


Configuration and usage
========================

* add `django_autoslug` to the list of `INSTALLED_APPS` in your `settings.py`
* use in `models.py`:

    from django_autoslug.fields import AutoSlugField

    ...

    class MyModel(models.Model):
        lang = models.CharField(_('lang'), max_length=50, choices=settings.LANGUAGES)
        title = models.CharField(_('title'), max_length=255)
        parent = models.ForeignKey('MyModel', blank=True, null=True)
        slug = AutoSlugField(populate_from=('title',), recursive='parent', prefix_from=('lang',), unique=True, max_length=255, overwrite=True)

* install `http://pypi.python.org/pypi/pytils` if you need russian translit support
