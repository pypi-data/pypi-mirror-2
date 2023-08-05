from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminIntegerFieldWidget
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class GenericForeignKeyWidget(forms.MultiWidget):

    def __init__(self, widgets=None, initial=None, *args, **kwargs):
        self.initial = initial
        super(GenericForeignKeyWidget, self).__init__(widgets)
        [setattr(widget, 'genericforeignkey_initial', initial) for widget in self.widgets]

    def decompress(self, value):
        value = value or self.initial
        if value:
            ct = ContentType.objects.get(app_label=value._meta.app_label,
                                         model=value._meta.module_name)
            return [ct.id, value.id]
        return [None, None]


class RelatedGenericWidget(AdminIntegerFieldWidget):

    class Media:
        js = ('%sgenericforeignkey/js/jquery.genericforeignkeywidget.js' % settings.MEDIA_URL, )

    def __init__(self, *args, **kwargs):
        super(RelatedGenericWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, *args, **kwargs):
        output = u'<div style="float: left;" class="relatedgenericwidget">'
        output += u'<div style="padding-top: 3px; font-size:12px; line-height: 16px;">'
        output += u'<span class="selected_content hidden">'
        output += self.genericforeignkey_initial and smart_unicode(self.genericforeignkey_initial) or '----'
        output += u'</span>'
        output += u'<span class="remove_current">'
        output += u'<img src="%(media)sgenericforeignkey/img/cancel.png" alt="%(title)s" title="%(title)s" />' % {
            'title': _(u'Remove'),
            'media': settings.MEDIA_URL}
        output += u'</span>'
        output += u'</div>'
        output += u'<div class="obj_id">'
        output += super(RelatedGenericWidget, self).render(name, value, *args, **kwargs)
        output += u'</div>'
        params=[]

        if params:
            params_str = '&id__in=%s' % ','.join(params)
        else:
            params_str = ''
        if getattr(self, 'genericforeignkey_initial', None):
            ct = ContentType.objects.get(app_label=self.genericforeignkey_initial._meta.app_label,
                                         model=self.genericforeignkey_initial._meta.module_name)
            params_str += '&content_type_id=%s' % ct.id
        output += u'<a id="lookup_id_%s" class="content_type hidden" href="/admin/contenttypes/contenttype/?%s" onclick="javascript:showRelatedObjectLookupPopup(this); return false;">%s</a>' % (name, params_str, _('Select content'))
        output += u'</div>'
        output += u'<br style="clear: left;" />'
        return mark_safe(u''.join(output))
