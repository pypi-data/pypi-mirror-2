import compiler
from pyf.dataflow import component
from pyf.componentized.components.configuration import Configuration
from pyf.componentized import ET

import logging
log = logging.getLogger(__name__)

class Component(object):
    def get_config_key(self, key, default=None):
        """ Returns a config key for the current process and id
            or default value """
        val = self.get_config_key_in_node(self.config_node, key)
        if val is None and hasattr(self, 'process_config_node'):
            val = self.get_config_key_in_node(self.process_config_node, key)
        
        if val is not None:
            return val
        else:
            return default
        
    def get_config_key_in_node(self, node, key, default=None):
        """ Returns a config key searching in a specific node """
        key_node = node.find(key)
        if key_node is not None:
            if key_node.text is not None and key_node.text != "":
                return key_node.text
            else:
                return default
        else:
            return default
        
    def get_config_key_node(self, key):
        node_current = self.config_node.find(key) # local config
        if node_current is None and hasattr(self, 'process_config_node'):
            node_current = self.process_config_node.find(key) # global config
        
        return node_current
        
    def set_config_key(self, key, value):
        """ Returns a config key for the current process and id
            or default value """
        key_node = self.config_node.find(key)
        if key_node is None:
            key_node = ET.SubElement(self.config_node, key)
            
        key_node.text = value
        
    def set_process_config_node(self, node):
        self.process_config_node = node
        
    def set_output_file_getter(self, getter):
        self.registered_output_files = list()
        self._get_output_file = getter
        
    def get_output_filename(self, target_filename):
        if not hasattr(self, '_get_output_file'):
            raise ValueError("Please don't try to get an output file before run.")
        
        # TODO: implement replace
        
        temp_filename = self._get_output_file(target_filename)
        self.registered_output_files.append((temp_filename, target_filename))
        
        return temp_filename
        
    @property
    def params(self):
        if hasattr(self, '_params'):
            return self._params
        else:
            return None
        
    @property
    def message_callback(self):
        if hasattr(self, '_message_callback'):
            return self._message_callback
        else:
            return log.info
        
    def set_params(self, params):
        self._params = params
        
    def set_message_callback(self, message_callback):
        self._message_callback = message_callback
    
    def get_configuration(self):
        config_node = 'configuration'
        config = Configuration()

        if hasattr(self, 'process_config_node'):
            configuration_node = self.process_config_node.find('config')
            if not configuration_node is None:
                config.read(configuration_node)

            configuration_node = self.process_config_node.find(config_node)
            if not configuration_node is None:
                config.read(configuration_node)

        configuration_node = self.config_node.find(config_node)
        if not configuration_node is None:
            config.read_xml_node(configuration_node)

        return config
        
class CodeComponent(Component):
    def __init__(self, config_node, name, gets_data=True):
        super(CodeComponent, self).__init__()
        
        self.config_node = config_node
        self.name = name
        
        self.code_node = self.config_node.find('code')
        self.code_text = self.code_node.text.strip()
        
        if gets_data:
            self.code_type = self.code_node.get('type', 'function')
            if self.code_type == 'function':
                self.introspect_function()
                self.code = compile(self.code_text, '<component "%s">' % self.name, 'exec')
                self.launch = self.launch_function
                
            elif self.code_type == 'exec':
                self.code = compile(self.code_text, '<component "%s">' % self.name, 'exec')
                self.launch = self.launch_exec
                
            elif self.code_type == 'eval':
                self.code = compile(self.code_text, '<component "%s">' % self.name, 'eval')
                self.launch = self.launch_eval
        else:
            self.introspect_function()
            self.code = compile(self.code_text, '<component "%s">' % self.name, 'exec')
            self.launch = self.launch_producer
        
    def introspect_function(self):
        """
        Gets the name of the last element of the code block.
        This is used to get the name of the function to execute.
        """
        self.code_func_name = compiler.parse(self.code_text,
                                             'exec').node.nodes[-1].name
                                             
    @component('IN', 'OUT')
    def launch_function(self, values, out):
        evaldict = dict(out=out,
                        get_config_key=self.get_config_key,
                        get_config_key_node=self.get_config_key_node,
                        config_node=self.config_node,
                        message_callback=self.message_callback,
                        param=self.params)
        exec self.code in evaldict
        for result in evaldict[self.code_func_name](values):
            yield result
            
    @component('IN', 'OUT')
    def launch_exec(self, values, out):
        for item in values:
            exec self.code
            yield item
    
    @component('IN', 'OUT')
    def launch_eval(self, values, out):
        for item in values:
            yield eval(self.code)
            
    def launch_producer(self, progression_callback=None,
                        message_callback=None, params=None):
        evaldict = dict(progression_callback=progression_callback,
                        message_callback=message_callback,
                        params=params,
                        get_config_key=self.get_config_key,
                        get_config_key_node=self.get_config_key_node)
        exec self.code in evaldict
        return evaldict[self.code_func_name]()
