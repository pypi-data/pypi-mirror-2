import os
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
import models
from django.conf import settings

from filer.settings import FILER_ADMIN_ICON_SIZES, FILER_PUBLICMEDIA_PREFIX, FILER_PRIVATEMEDIA_PREFIX, FILER_STATICMEDIA_PREFIX

class FilerImagePlugin(CMSPluginBase):
    model = models.FilerImage
    name = _("Image (Filer)")
    render_template = "cmsplugin_filer_image/image.html"
    text_enabled = True
    raw_id_fields = ('image',)
    admin_preview = False
    
    def render(self, context, instance, placeholder):
        # TODO: this scaling code needs to be in a common place
        # use the placeholder width as a hint for sizing
        placeholder_width = context.get('width', None)
        if instance.image:
            if instance.use_autoscale and placeholder_width:
                width = placeholder_width
            else:
                if instance.width:
                    width = instance.width
                else:
                    width = instance.image.width
            if instance.height:
                height = instance.height
                if width == instance.image.width:
                    # width was not externally defined: use ratio to scale it by the height
                    width = int( float(height)*float(instance.image.width)/float(instance.image.height) )
            else:
                # height was not externally defined: use ratio to scale it by the width
                height = int( float(width)*float(instance.image.height)/float(instance.image.width) )
        else:
            width, height = instance.width, instance.height
        context.update({
            'object':instance,
            'link':instance.link, 
            #'image_url':instance.scaled_image_url,
            'image_size': u'%sx%s' % (width, height),
            'placeholder':placeholder
        })
        return context
    def icon_src(self, instance):
        if instance.image:
            return instance.image.thumbnails['admin_tiny_icon']
        else:
            return os.path.normpath(u"%s/icons/missingfile_%sx%s.png" % (FILER_STATICMEDIA_PREFIX, 32, 32,))
plugin_pool.register_plugin(FilerImagePlugin)
