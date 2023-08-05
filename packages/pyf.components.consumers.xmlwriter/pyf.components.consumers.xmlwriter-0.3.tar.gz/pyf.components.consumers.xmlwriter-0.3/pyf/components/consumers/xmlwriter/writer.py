from pyf.componentized.error import MissingConfigEntryError, MissingConfigSectionError
from pyf.componentized.components.writer import FileWriter
from ConfigParser import NoOptionError, NoSectionError
from genshi.template import Template, MarkupTemplate
from pkg_resources import resource_string
from pyf.componentized.components.multiwriter import MultipleFileWriter
import codecs

from pyf.dataflow import component

import logging
log = logging.getLogger()

class XMLWriter(MultipleFileWriter):
    name = "xmlwriter"
    def __init__(self, config_node, component_name):
        """Initialize a new XMLWriter
        @param config: SafeConfigParser
        @type config: SafeConfigParser instance

        @param process_name: The process name to use
        @type process_name: String
        """
        self.config_node = config_node
        self.name = component_name

        self.template = self.get_template()
        
    def get_template(self):
        template_node = self.config_node.find('template')
        template_type = template_node.get('type', 'embedded')
        
        if template_type == 'plugin':
            template_module = template_node.get('module')
            return MarkupTemplate(
                       resource_string(
                           template_module,
                           "static/templates/" + template_node.text.strip() + ".xml"
                       )
                   )
            
        elif template_type == 'embedded':
            return MarkupTemplate(template_node.text.strip())
        
        else:
            raise NotImplementedError, "Template type %s is not handled." % \
                                                                template_type

    def write(self, values, key, output_filename, target_filename):
        encoding = self.get_config_key('encoding')
        
        target_file = codecs.open(output_filename, 'wb+', encoding)

        for num, markup in enumerate(self.template.generate(
                    file_name=target_filename,
                    splitkey=key,
                    encoding=encoding,
                    datas=values,
                    get_config_key=self.get_config_key).serialize(method='xml')):
            target_file.write(markup)
            yield True

        target_file.close()
        yield True
