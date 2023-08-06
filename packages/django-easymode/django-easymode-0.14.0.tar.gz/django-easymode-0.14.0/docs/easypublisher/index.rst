.. _easypublisher:

Basic approval support for models
=================================

Easymode comes with :mod:`~easymode.easypublisher`, a very simple approval 
application. It uses
`django-reversion <http://code.google.com/p/django-reversion/>`_ to store drafted
content. This has the very nice side effect that all drafts are in your history.
You should make sure reversion is installed before using easypublisher.

There is only one layer of approval, either you've got publishing rights or you
don't. Anyone with publisher rights can move content from draft to published, 
as long as they've got permission to modify the content. 

Usage
-----

To use the publisher you have to include ``easymode.easypublisher.urls`` in your
url conf::
    
    (r'^', include('easymode.easypublisher.urls')),

Also ``easymode.easypublisher`` should be added to your ``INSTALLED_APPS`` in the
settings file. After that, you may use
:class:`~easymode.easypublisher.admin.EasyPublisher` instead of 
:class:`~django.contrib.admin.ModelAdmin` as follows::

    from django.contrib import admin
    from foobar.models import *
    from easymode.easypublisher.admin import EasyPublisher
    
    class FooAdmin(EasyPublisher):
        model = Foo
    
    admin.site.register(Foo, FooAdmin)

The models you register with :class:`~easymode.easypublisher.admin.EasyPublisher`
should have a *published* property which must be a
:class:`~django.db.models.BooleanField`::

    class Foo(models.Model):
        published = models.BooleanField(default=True)

You can also use :class:`~easymode.easypublisher.models.EasyPublisherModel` as a
base class, which defines the *published* field for you.

Permissions
-----------

A new permission will be added ``easypublisher.can_approve_for_publication`` if some
body does *NOT* have this permission, all their changes will only be saved as versions
and never in the database. All people who *DO* have this permission can view the list
of *drafts*, load them and save them, which means they are published. All your drafts and 
versions will be kept track of by 
`django-reversion <http://code.google.com/p/django-reversion/>`_.

Use easypublisher together with ForeignKeyAwareModelAdmin
---------------------------------------------------------

In case you want to use easypublisher together with :mod:`easymode.tree.admin.relation`
you will find that multiple inheritance doesn't work due to conflicts. Instead,
use :class:`~easymode.easypublisher.admin.EasyPublisherFKAModelAdmin` where you would
use :class:`~easymode.tree.admin.relation.ForeignKeyAwareModelAdmin` and 
:class:`~easymode.easypublisher.admin.EasyPublisherInvisibleModelAdmin` where you would
use :class:`~easymode.tree.admin.relation.InvisibleModelAdmin`. 

More info about these admin classes is in :ref:`tree_explanation`.

Preview for flash sites
-----------------------

Including ``easymode.easypublisher.urls`` in your url conf gives you an opportunity
to implement preview of drafted content for flash sites. The request views will have
an extra querystring parameter called ``preview`` which contains the revision id.

In your view function you can then use this to obtain and insert the drafted content
in the xml that easymode produces. Some convenience functions are defined in
:mod:`easymode.easypublisher.response` and :mod:`easymode.easypublisher.utils`.

Easypublisher templatetag :func:`~easymode.easypublisher.templatetags.easypublisher.draft_list_items`
-----------------------------------------------------------------------------------------------------

:func:`~easymode.easypublisher.templatetags.easypublisher.draft_list_items` is a templatetag that can
be used to show all drafts that need approval as a list of links to these drafts. You could
include it in your admin template somewhere.

use like this:

.. code-block:: html+django

    {% load 'easypublisher' %}
    
    <ul>
    {% draft_list_items %}
    </ul>

This will render as a list of links to all unapproved drafts.
