from django import forms
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class GenericAdminModelForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(GenericAdminModelForm, self).clean()
        for generic_foreign_key in self._meta.model._meta.virtual_fields:
            if isinstance(generic_foreign_key, GenericForeignKey):
                obj = cleaned_data.get(generic_foreign_key.name, None)
                if not obj:
                    cleaned_data[generic_foreign_key.name] = None
                    cleaned_data[generic_foreign_key.ct_field] = None
                    cleaned_data[generic_foreign_key.fk_field] = None
                else:
                    cleaned_data[generic_foreign_key.ct_field] = ContentType.objects.get_for_model(obj)
                    cleaned_data[generic_foreign_key.fk_field] = obj.pk
        return cleaned_data
