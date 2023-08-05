"""
Internationalization and localization support for django models.
"""

from weakref import WeakKeyDictionary

from django.db.models.signals import post_save

from easymode.i18n.gettext import MakeModelMessages

_post_save_handlers = WeakKeyDictionary()

def register(cls, location=None):
    """
    Register a model for translation
    like so:
    
    >>> from easymode import i18n
    >>> i18n.register(SomeModel)
    
    This will add entries to the gettext catalog located in the
    ``settings.LOCALE_DIR`` or directory.
    
    You can also store the catalogs somewhere else. The next example stores the
    catalog in the same dir as the file in which i18n.register is called:
    
    >>> i18n.register(SomeModel, __file__)
    
    You can also explictly give a path:
    
    >>> i18n.register(SomeModel, '/tmp/)
    
    Please note that the entire locale is stored in that path, so if the path
    is /tmp/ the locale is: /tmp/locale/ this directory will be created if it
    does not exist.
    
    :param cls: The model class that should be translated by means of gettext.
    :param location: The location of the po file. This can be either a directory\
        or a file name. If left unspecified, ``settings.LOCALE_DIR`` or\
        ``settings.PROJECT_DIR`` will be used.
    """
       
    create_po_for_model = MakeModelMessages(location, cls)
    
    _post_save_handlers[cls] = create_po_for_model
    
    post_save.connect(create_po_for_model, cls, False)

def unregister(cls):
    """
    unregisters a previously registered model.
    
    This means the po file will not be updated when the model is saved.
    
    :param cls: The model class that should nolonger be translated by means of gettext.
    """
    handler = _post_save_handlers.get(cls, None)
    if handler:
        post_save.disconnect(handler, cls)