from pyf.componentized.error import MissingConfigEntryError, MissingConfigSectionError
from pyf.componentized.components.writer import FileWriter
from csv import DictWriter
from pyf.componentized.components.multiwriter import MultipleFileWriter
import csv

from pyf.dataflow import component

from pyf.components.consumers.csvwriter.addon import CSVAddon

import codecs

import logging
log = logging.getLogger()

class CSVWriter(MultipleFileWriter):
    name = "csvwriter"
    def __init__(self, config_node, component_id):
        """Initialize a new CSVWriter
        @param config: SafeConfigParser
        @type config: SafeConfigParser instance

        @param process_name: The process name to use
        @type process_name: String
        """
        self.config_node = config_node
        self.id = component_id


        self.encoding = self.get_config_key('encoding')
        self.columns = self.config_node.find('columns')
        self.delimiter = self.get_config_key('delimiter')

        self.column_definitions = list()
        self.renderers = dict()
        
        self.__retrieve_columns_definition()

        csv.register_dialect('%s_dialect' % self.id, delimiter=self.delimiter,
                quoting=csv.QUOTE_ALL)

    def __retrieve_columns_definition(self):
        defs = self.columns.findall('column')

        for column_def in defs:
            if column_def.get('attribute'):
                attr = column_def.get('attribute')
            else:
                attr = column_def.text.strip()
            
            self.column_definitions.append((attr,
                                            column_def.text.strip()))
                
            if column_def.get('renderer'):
                self.renderers[attr] = column_def.get('renderer')

    def __get_column_attributes(self):
        return [col_def[0] for col_def in self.column_definitions]

    def get_column_names(self):
        return [col_def[1] for col_def in self.column_definitions]
    
    def write(self, values, key, output_filename, target_filename):
        target_file = open(output_filename, 'wb+')

        csvengine = DictWriter(target_file,
                self.get_column_names(), dialect='%s_dialect' % self.id)
        
        firstrow = dict()
        for colname in self.get_column_names():
            firstrow[colname] = colname
        csvengine.writerow(firstrow)

        for data in values:
            adapted_data = CSVAddon(data, self.column_definitions,
                                    self.renderers, self.encoding)
            csvengine.writerow(adapted_data)
            del adapted_data
            yield True

        target_file.close()
        yield True
