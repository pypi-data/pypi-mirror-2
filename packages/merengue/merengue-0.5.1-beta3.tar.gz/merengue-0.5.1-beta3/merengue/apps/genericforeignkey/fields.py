from django import forms

from genericforeignkey.widgets import GenericForeignKeyWidget, RelatedGenericWidget


class GenericForeignKeyField(forms.MultiValueField):

    widget = GenericForeignKeyWidget

    def __init__(self, fields, initial, exclude_content_types=None, *args, **kwargs):
        field_contenttype = fields[0]
        field_contenttype.widget.attrs['class'] = 'genericforeignkey'
        for app_label, model in exclude_content_types:
            field_contenttype.queryset = field_contenttype.queryset.exclude(app_label=app_label,
                                                                            model=model)
        self.widget = self.widget(widgets=[field_contenttype.widget, RelatedGenericWidget], initial=initial)
        super(GenericForeignKeyField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 2 and data_list[0] and data_list[1]:
            return data_list[0].model_class().objects.get(id=data_list[1])
        return None
