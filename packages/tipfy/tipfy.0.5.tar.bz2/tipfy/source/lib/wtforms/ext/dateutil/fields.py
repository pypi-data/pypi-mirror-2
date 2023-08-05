"""
A DateTimeField and DateField that use the `dateutil` package for parsing.
"""
from dateutil import parser

from wtforms.fields import Field
from wtforms.validators import ValidationError
from wtforms.widgets import TextInput


__all__ = (
    'DateTimeField', 'DateField',
)


class DateTimeField(Field):
    """
    DateTimeField represented by a text input, accepts all input text formats
    that `dateutil.parser.parse` will.

    :param parse_kwargs:
        A dictionary of keyword args to pass to the dateutil parse() function.
        See dateutil docs for available keywords.
    :param display_format:
        A format string to pass to strftime() to format dates for display.
    """
    widget = TextInput

    def __init__(self, label=u'', validators=None, parse_kwargs=None,
                 display_format='%Y-%m-%d %H:%M', **kwargs):
        super(DateTimeField, self).__init__(label, validators, **kwargs)
        if parse_kwargs is None:
            parse_kwargs = {}
        self.parse_kwargs = parse_kwargs
        self.display_format = display_format
        self.raw_data = None

    def _value(self):
        if self.raw_data is not None:
            return self.raw_data
        else:
            return self.data and self.data.strftime(self.display_format) or u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.raw_data = str.join(' ', valuelist)
            parse_kwargs = self.parse_kwargs.copy()
            if 'default' not in parse_kwargs:
                try:
                    parse_kwargs['default'] = self._default()
                except TypeError:
                    parse_kwargs['default'] = self._default
            try:
                self.data = parser.parse(self.raw_data, **parse_kwargs)
            except ValueError:
                self.data = None
                raise ValidationError(u'Invalid date/time input')


class DateField(DateTimeField):
    """
    Same as the DateTimeField, but stores only the date portion.
    """
    def __init__(self, label=u'', validators=None, parse_kwargs=None,
                 display_format='%Y-%m-%d', **kwargs):
        super(DateField, self).__init__(label, validators, parse_kwargs=parse_kwargs, display_format=display_format, **kwargs)

    def process_formdata(self, valuelist):
        super(DateField, self).process_formdata(valuelist)
        if self.data is not None and hasattr(self.data, 'date'):
            self.data = self.data.date()
