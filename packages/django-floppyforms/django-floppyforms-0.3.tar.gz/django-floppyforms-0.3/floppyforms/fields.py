from django import forms

from floppyforms.widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                                 FileInput, ClearableFileInput, SelectMultiple,
                                 DateInput, DateTimeInput, TimeInput, URLInput,
                                 NumberInput, RangeInput, EmailInput,
                                 NullBooleanSelect, SlugInput, IPAddressInput)

__all__ = (
    'Field', 'CharField', 'IntegerField', 'DateField', 'TimeField',
    'DateTimeField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'FloatField', 'DecimalField', 'SlugField', 'RegexField', 'IPAddressField',
)


class Field(forms.Field):
    widget = TextInput
    hidden_widget = HiddenInput

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        self.widget.is_required = self.required  # fallback to support
                                                 # is_required with
                                                 # Django < 1.3


class CharField(Field):
    widget = TextInput


class BooleanField(Field, forms.BooleanField):
    widget = CheckboxInput


class NullBooleanField(Field, forms.NullBooleanField):
    widget = NullBooleanSelect


class ChoiceField(Field, forms.ChoiceField):
    widget = Select


class FileField(Field, forms.FileField):
    widget = ClearableFileInput


class ImageField(Field, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceField(forms.MultipleChoiceField):
    widget = SelectMultiple


class DateField(Field, forms.DateField):
    widget = DateInput


class DateTimeField(Field, forms.DateTimeField):
    widget = DateTimeInput


class TimeField(Field, forms.TimeField):
    widget = TimeInput


class DecimalField(Field, forms.DecimalField):
    widget = NumberInput


class FloatField(Field, forms.FloatField):
    widget = NumberInput


class IntegerField(FloatField, forms.IntegerField):
    widget = NumberInput


class EmailField(Field, forms.EmailField):
    widget = EmailInput


class URLField(Field, forms.URLField):
    widget = URLInput


class SlugField(Field, forms.SlugField):
    widget = SlugInput


class RegexField(Field, forms.RegexField):
    widget = TextInput

    def __init__(self, regex, js_regex=None, max_length=None, min_length=None,
                 error_message=None, *args, **kwargs):
        self.js_regex = js_regex
        super(RegexField, self).__init__(regex, max_length, min_length,
                                         *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(RegexField, self).widget_attrs(widget) or {}
        if self.js_regex is not None:
            attrs['pattern'] = self.js_regex
        return attrs


class IPAddressField(Field, forms.IPAddressField):
    widget = IPAddressInput
