from django import forms

from floppyforms.widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                                 FileInput, ClearableFileInput, SelectMultiple,
                                 DateInput, DateTimeInput, TimeInput, URLInput,
                                 NumberInput, RangeInput, EmailInput)


class FloppyField(forms.Field):
    widget = TextInput
    hidden_widget = HiddenInput

    def __init__(self, *args, **kwargs):
        super(FloppyField, self).__init__(*args, **kwargs)
        self.widget.is_required = self.required  # fallback to support
                                                 # is_required with
                                                 # Django < 1.3


class CharField(FloppyField):
    widget = TextInput


class BooleanField(FloppyField, forms.BooleanField):
    widget = CheckboxInput


class ChoiceField(FloppyField, forms.ChoiceField):
    widget = Select


class FileField(FloppyField, forms.FileField):
    widget = ClearableFileInput


class ImageField(FloppyField, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceField(forms.MultipleChoiceField):
    widget = SelectMultiple


class DateField(FloppyField, forms.DateField):
    widget = DateInput


class DateTimeField(FloppyField, forms.DateTimeField):
    widget = DateTimeInput


class TimeField(FloppyField, forms.TimeField):
    widget = TimeInput


class DecimalField(FloppyField, forms.DecimalField):
    widget = NumberInput


class FloatField(FloppyField, forms.FloatField):
    widget = NumberInput


class IntegerField(FloatField, forms.IntegerField):
    widget = NumberInput


class EmailField(FloppyField, forms.EmailField):
    widget = EmailInput


class URLField(FloppyField, forms.URLField):
    widget = URLInput
