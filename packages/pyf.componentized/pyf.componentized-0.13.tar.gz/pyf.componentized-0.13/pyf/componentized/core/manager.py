from pyf.dataflow.core import component
from pyf.transport.packets import Packet
import datetime
import shutil
import os
import ConfigParser

import tempfile

from pyf.manager.network import Network
from pyf.manager import DataManager

from pyf.componentized.error import DataPathError

from pyf.componentized.components import ManagedComponent, ResourceManager

from pyf.componentized import ET

import logging
log = logging.getLogger()

class ProcessPipe(object):
    def __init__(self,
                 config_tree,
                 data_manager,
                 process_name,
                 options=None):
        self.config_tree = config_tree
            
        self.process_name = process_name

        self.resourcemanager = ResourceManager()
        
        self.data_manager = data_manager
        
#        self.root_config_node = self.config_tree.find('node')
        
        self.process_config_node = self.config_tree.find('config')
        if self.process_config_node is None:
            self.process_config_node = ET.SubElement(self.config_tree, 'config')
        
        if options is not None:
            self.__update_process_config(options)
            
        self.initialize()
        
#    def init_producer(self):
#        producer_tree = self.config_tree.find('node')
#        return ManagedComponent(producer_tree, self.process_config_node)

    def initialize(self, progression_callback=None,
                   message_callback=None,
                   params=None):
        self.components = dict()

        self.nodes = dict()
        self.nodes_to_be_linked = list()
        
        self.progression_callback = progression_callback
        self.message_callback = message_callback
        self.params = params
        
        for node in self.config_tree.findall('node'):
            self.parse_node(node, False)
            
        self.link_orphans()

        network = Network(self.nodes)
        self.data_manager.add_network(self.process_name, network)
        
    def __update_process_config(self, options):
        for key, value in options.iteritems():
            element = self.process_config_node.find(key)
            if element is None:
                element = ET.SubElement(self.process_config_node, key)
            
            element.text = value
            
    def setup_component(self, node):
        component = ManagedComponent(node, self.process_config_node,
                                     self.progression_callback,
                                     self.message_callback,
                                     self.params)
        self.components[component.name] = component
        return component
    
    def setup_joiner(self, node):
        if node is not None:
            plugin = ResourceManager().get_joiner(node.get('pluginname'))
            return plugin(node)
        else:
            return None
            
#    def parse_node(self, node, current_path_node, append_object=True):
#        if append_object:
#            component = self.setup_component(node)
#            component.init_component()
#            
#            road_component = dict(component = component.component)
#            
#            current_path_node.setdefault('content',
#                                         list()).append(road_component)
#        
#        children = node.findall('children/node')
#        if children:
#            if len(children) > 1:
#                for child in children:
#                    to_be_passed_dict = dict(content=list())
#                    current_path_node.setdefault('children', list()).append(to_be_passed_dict)
#                    self.parse_node(child, to_be_passed_dict)
#            else:
#                self.parse_node(children[0], current_path_node)

    @component('IN', 'OUTA')
    def splitter(self, source, out, size=3):
        """ Splits a data source in n sources (size kwarg)"""
        yield (out.size(), size)
        for row in source:
            if isinstance(row, Packet):
                serialized = row.serialized
                for i in range(size):
                    yield (out(i), Packet(data=serialized,
                                          data_type="serialized"))
            else:
                for i in range(size):
                    yield (out(i), row)

    def parse_node(self, config_node, before=None):
        node_id = config_node.get('name')
        if not node_id:
            raise ValueError("Node doesn't have a name !")
        
        node_type = config_node.tag
        
        if node_type == 'link':
            if not before:
                raise ValueError("Can't add a link without a parent.")
            
            if node_id in self.nodes:
                self.nodes[node_id].setdefault('before', list()).append(before)
            else:
                self.nodes_to_be_linked.append((node_id, before))
                
        else:
            component = self.setup_component(config_node)
            component.init_component()
            
            joiner_info = config_node.find('joiner')
            joiner = self.setup_joiner(joiner_info)
            
            node = dict(component=component.component,
                        before=(before and [before] or list()),
                        after=list(),
                        joiner=(joiner is not None) and joiner.launch or None,)
                        #splitter=self.splitter)
            
            children = config_node.findall('children/node') + config_node.findall('children/link')
            if children:
                for child in children:
                    self.parse_node(child, node_id)
                    node['after'].append(child.get('name'))
                    
            self.nodes[node_id] = node
            
    def link_orphans(self):
        for node_id, parent in self.nodes_to_be_linked:
            self.nodes[node_id]['before'].append(parent)
            self.nodes[parent]['after'].append(node_id)
        
            
    def process(self, progression_callback=None,
                message_callback=None,
                params=None,
                finalize=True):
        """
        """        
        if not progression_callback:
            progression_callback = lambda x: log.debug('Progression : %s' % x)

        if not message_callback:
            message_callback = log.debug
            
        self.initialize(progression_callback,
                        message_callback,
                        params)
        
        message_callback(u'Launching process %s' % self.process_name)
        self.__propagate_info(message_callback, params=params)
        self.__do_process(progression_callback, message_callback, params=params)
        message_callback(u'Finalizing process %s' % self.process_name)
        if finalize:
            self.__do_finalize_process(progression_callback, message_callback)
        else:
            return self.__get_finalization_info()

    def __do_process(self, progression_callback=None, message_callback=None, params=None):
        """
        """
        log.debug('getting extractor')
#        self.producer.init_component()
        
#        datas = self.producer.launch(progression_callback,
#                                message_callback,
#                                params=params)
#        
#        self.data_manager.setup_path(self.process_name, datas)
        self.data_manager.setup_network(self.process_name)
        
        message_callback(u'Path setup')
        
        status_handler = self.data_manager.get_network(self.process_name).get_status_handler()
        message_callback(u'Status handler setup')
        
        for status in status_handler:
            if not status:
                raise DataPathError("Unknown error in data path")

        now = datetime.datetime.now().date()
        
    def __propagate_info(self, message_callback=None, params=None):
        for name, component in self.components.iteritems():
            component.set_params(params)
            component.set_message_callback(message_callback)
            
    def __do_finalize_process(self, progression_callback=None, message_callback=None):
        for component in self.components.values():
            component.finalize()
            
    def __get_finalization_info(self):
        infos = list()
        for component in self.components.values():
            info = component.get_finalization_info()
            if info:
                for inf in info:
                    infos.append(inf)
                
        return infos
        
class Manager(object):
    def __init__(self, config_tree):
        self.config_tree = config_tree
        
        self.process_pipes = list()
        
        self.data_manager = DataManager()

    def get_process_names(self):
        """
        """
        return [n.get('name') for n in self.config_tree.findall('process')]

    def get_process_config(self, name):
        for process in self.config_tree.findall('process'):
            if process.get('name') == name:
                return process
            
        return None
        
    def process(self, name=None,
                params=None,
                progression_callback=None,
                message_callback=None,
                finalize=True,
                process_config=None,
                options=None):
        """
        If process_config is passed, ignore main config tree,
        and process with this tree instead.
        """
        if not name:
            returns = list()
            for process_name in self.get_process_names():
                returned = self.process(process_name,
                             params=params,
                             progression_callback=progression_callback,
                             message_callback=message_callback,
                             finalize=finalize,
                             options=options)
                if returned: returns.append(returned)
            return returns
        else:
            process_pipe = ProcessPipe((process_config or
                                        self.get_process_config(name)),
                                       self.data_manager,
                                       name,
                                       options=options)
            return process_pipe.process(params=params,
                                        progression_callback=progression_callback,
                                        message_callback=message_callback,
                                        finalize=finalize)
    
    def clean(self):
        self.data_manager.clean()
