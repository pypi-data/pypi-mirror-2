from django.forms.widgets import MediaDefiningClass
from django.utils.datastructures import SortedDict
from django.contrib import admin

from easymode.easypublisher import admin as publisher_admin
from easymode.tree.admin import relation


CLASS_MAP = SortedDict({
    relation.ForeignKeyAwareModelAdmin:publisher_admin.EasyPublisherFKAModelAdmin,
    relation.InvisibleModelAdmin:publisher_admin.EasyPublisherInvisibleModelAdmin,
    admin.ModelAdmin:publisher_admin.EasyPublisher,
})

def bases_walker(cls):
    for base in cls.__bases__:
        yield base
        for more in bases_walker(base):
            yield more
    
def nearest_publisher_admin(bases):
    """
    Finds the best easypublisher match for a modeladmin class
    
    :param cls: An instance of :ref:django.contrib.admin.ModelAdmin:
    """
    # if isinstance(cls, relation.ForeignKeyAwareModelAdmin):
    #     return publisher_admin.EasyPublisherFKAModelAdmin
    # if isinstance(cls, relation.InvisibleModelAdmin):
    #     return publisher_admin.EasyPublisherInvisibleModelAdmin
    # if isinstance(cls, admin.ModelAdmin):
    #     return publisher_admin.EasyPublisher
    
    for cls in bases:
        print cls
        for (key, value) in CLASS_MAP.iteritems():
            # print "%s %s %s" % (cls, key, value)
            # print "isinstance(%s, %s)?" % (cls, key)
            print "%s in bases_walker(%s)" % (key, cls)
            if key in bases_walker(cls):
                print "%s in bases_walker(%s) !!!!!!!" % (key, cls)
                return value
    
    return None

class ForcePublisherMediaDefiningClass(MediaDefiningClass):
    """docstring for ForcePublisherMediaDefiningClass"""
    def __new__(cls, name, bases, attrs):
        a = nearest_publisher_admin(bases)
        if a:
            bases = (a, ) + bases
        print bases
        return super(ForcePublisherMediaDefiningClass, cls).__new__(cls, name, bases,
                                                           attrs)
