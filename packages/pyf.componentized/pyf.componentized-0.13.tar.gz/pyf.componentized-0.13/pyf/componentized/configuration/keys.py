from pyf.componentized import ET
from pyf.componentized.configuration.fields import InputField, TextAreaField,\
    RepeatingField

class ComponentConfiguration(object):
    pass

class ConfigurationKey(object):
    def __init__(self, key, default=None, field=None):
        self.key = key
        self.default = default
        
        if field is None:
            self.field = self.get_default_field()
        else:
            self.field = field
    
    def get_default_field(self):
        return InputField(default=self.default)
        
    def to_xml(self, value):
        raise NotImplementedError, "Method to_xml isn't implemented for %s" % self.key
    
    def from_xml(self, node):
        raise NotImplementedError, "Method from_xml isn't implemented for %s" % self.key

class SimpleKey(ConfigurationKey):
    def to_xml(self, value):
        el = ET.Element(self.key)
        el.text = value
        return el
    
    def from_xml(self, node):
        return node.text
    
class CDATAKey(SimpleKey):
    def get_default_field(self):
        return TextAreaField(default=self.default)
        
    def to_xml(self, value):
        el = ET.Element(self.key)
        if hasattr(ET, 'CDATA'):
            el.text = ET.CDATA(value)
        else:
            el.text = value
        return el
    
class XMLKey(CDATAKey):
    def get_default_field(self):
        return TextAreaField(default=self.default, classname="xmlcode")
    
class PythonKey(CDATAKey):
    def get_default_field(self):
        return TextAreaField(default=self.default, classname="pythoncode")
    
class CompoundKey(ConfigurationKey):
    def __init__(self, key,
                 content_definition = None,
                 default=None, field=None):
        super(RepeatedKey, self).__init__(key, default=default, field=field)
        
        if content_definition is None:
            raise ValueError, "No content definition for "

class RepeatedKey(ConfigurationKey):
    def __init__(self, key,
                 content=None,
                 default=None, field=None):
        super(RepeatedKey, self).__init__(key, default=default, field=field)
        self.each_key = each_key
        
        if content is not None:
            self.content = content
            self.field = self.get_repeated_field(content)
        
    def get_default_field(self):
        # we return none here, we will set our default field witb content.
        return None
    
    def get_repeated_field(self, content):
        return RepeatingField(content=content, default=self.default)
        
    def to_xml(self, value):
        el = ET.Element(self.key)
        
        for item in value:
            sel = self.content.to_xml(item)
            el.append(sel)
        
        return el
    
    def from_xml(self, node):
        search_key = self.content.key
        values = list()
        for item in node.searchall(search_key):
            values.append(self.content.from_xml(item))
        
        return values