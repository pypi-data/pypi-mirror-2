import re
from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator

class PartialUrlValidator:
    implements(IValidator)
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        # field gets passed in via kwargs
        if '://' not in value:
            widget = kwargs.get('field').widget
            default_p = getattr(widget,'default_protocol','http')
            value = default_p + '://' + value
        pattern = re.compile(r'(ht|f)tps?://[^\s\r\n]+')
        m = pattern.match(value)
        if not m:
            return ("Validation failed(%s): value is %s"%(self.name,
                repr(value)))
        return 1
