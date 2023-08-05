from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from genericforeignkey.fields import GenericForeignKeyField
from genericforeignkey.forms import GenericAdminModelForm


class GenericAdmin(object):

    form = GenericAdminModelForm
    EXCLUDE_CONTENT_TYPES = ()

    def get_form(self, request, obj=None):
        form = super(GenericAdmin, self).get_form(request, obj)
        initial = None
        for generic_foreign_key in self.model._meta.virtual_fields:
            if isinstance(generic_foreign_key, GenericForeignKey):
                old_content_type_field = form.base_fields[generic_foreign_key.ct_field]
                old_obj_id_field = form.base_fields[generic_foreign_key.fk_field]
                if not request.POST:
                    initial = obj and getattr(obj, generic_foreign_key.name, None) or None
                else:
                    ct_id = request.POST.get('%s_0' % generic_foreign_key.name, None)
                    fk_id = request.POST.get('%s_1' % generic_foreign_key.name, None)
                    if ct_id and fk_id:
                        ctype = ContentType.objects.get(pk=ct_id)
                        initial = ctype.model_class().objects.get(pk=fk_id)
                cts_id = [ct.id for ct in old_content_type_field.queryset if not ct.model_class()]
                old_content_type_field.queryset = ContentType.objects.exclude(pk__in=cts_id)
                exclude_content_types = self.EXCLUDE_CONTENT_TYPES or getattr(settings, 'EXCLUDE_CONTENT_TYPES', [])
                form.base_fields[generic_foreign_key.name] = GenericForeignKeyField(fields=[old_content_type_field, old_obj_id_field],
                                                                                    initial=initial,
                                                                                    exclude_content_types=exclude_content_types,
                                                                                    label=old_content_type_field.label,
                                                                                    required=old_content_type_field.required or old_obj_id_field.required,
                                                                                    help_text=_('Select first the content type, and after select a content of this type'))
                del form.base_fields[generic_foreign_key.ct_field]
                del form.base_fields[generic_foreign_key.fk_field]
        return form


def register(site):
    from genericforeignkey.admin_register import GenericContentTypeAdmin
    site.register(ContentType, GenericContentTypeAdmin)
