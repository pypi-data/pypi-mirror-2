class Field(object):
    type = "input"
    default_classname = ""
    
    def __init__(self, default=None, classname="", title=None):
        self.default = default
        self.value = ""
        self.classname = classname or self.default_classname

class InputField(Field):
    pass

class TextAreaField(Field):
    type = "textarea"

class SingleSelectField(Field):
    type = "select"
    
    def __init__(self, values=None, default=None, classname="", title=None):
        super(SingleSelectField, self).__init__(default=default, classname=classname, title=title)
        
        if values is None:
            raise ValueError, "You should define possible values for a select list"
        
        self.values = values
        
class MultipleFields(Field):
    type = "container"
    
    def __init__(self, content=None, default=None, classname="", title=None):
        super(MultipleFields, self).__init__(default=default, classname=classname, title=title)
        
        if content is None:
            raise ValueError, "You should define content sub widgets for a multiple field"
        
class InlineMultipleFields(Field):
    type = "inline_container"
    
    def __init__(self, content=None, default=None, classname="", title=None):
        super(MultipleFields, self).__init__(default=default, classname=classname, title=title)
        
        if content is None:
            raise ValueError, "You should define content sub widgets for a multiple field"
        
        self.content = content
        
class RepeatingField(Field):
    type = "repeating"
    
    def __init__(self, content=None, default=None, classname="", title=None):
        super(RepeatingField, self).__init__(default=default, classname=classname, title=title)
        
        if content is None:
            raise ValueError, "You should define content sub widgets for a multiple field"
        
        self.content = content