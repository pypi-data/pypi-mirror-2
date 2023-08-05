from ConfigParser import ConfigParser
from os.path import isfile
from os import environ
import sys
from time import strftime


def config_options(config=None):
    """Instead of calling ConfigParser all over the place
    we gather, read, parse and return valid configuration
    values for any yopypi log.utility here, config should
    always be a file object or None and config_options
    always returns a dictionary with values"""
    
    # If all fails we will always have default values
    configuration = config_defaults()

    # Options comming from the config file have
    # longer names, hence the need to map them correctly
    opt_mapper = {
            'yopypi.web.host':'web_host',
            'yopypi.web.port':'web_port',
            'yopypi.mirrors':'mirrors',
            }

    try:
        if config == None or isfile(config) == False:
            configuration = config_defaults()
            return configuration

    except TypeError:
        if type(config) is dict:
            configuration = config_defaults(config)
    
    else:
        try:
            converted_opts = {}
            parser = ConfigParser()
            parser.read(config)
            file_options = parser.defaults()

            # we are not sure about the section so we 
            # read the whole thing and loop through the items
            for key, value in opt_mapper.items():
                try:
                    file_value = file_options[key]
                    converted_opts[value] = file_value

                except KeyError:
                    pass # we will fill any empty values later with config_defaults
            try:
                configuration = config_defaults(converted_opts)
            except Exception, e:
                pass
        except Exception, e:
            pass

    return configuration

def config_defaults(config=None):
    """From the config dictionary it checks missing values and
    adds the defaul ones for them if any"""
    if config == None:
        config = {}
    defaults = {
            'web_host': 'localhost',
            'web_port': '8080',
            'mirrors' : ['d.pypi.python.org', 'c.pypi.python.org', 'b.pypi.python.org']
            }

    for key in defaults:
        try:
            config[key]
        except KeyError:
            config[key] = defaults[key]
    return config


class logging(object):
    
    def __init__(self, 
            module='',
            type='INFO'):

        self.log_file = environ.get('HOME')+'/.yopypi/yopypi.log'
        self.module = module
        self.type = type
        if self.module != '':
            self.name = 'yopypi.%s' % module
        else:
            self.name = 'yopypi'
        

    def write(self, message):
        try:
            if isfile(self.log_file):
                open_log = open(self.log_file, 'a')
            else:
                open_log = open(self.log_file, 'w')

            timestamp = strftime('%b %d %H:%M:%S')
            log_line = "%s %s %s %s" % (timestamp, self.type, self.name, message)
            open_log.write(log_line+'\n')
            open_log.close()

        except IOError:
            sys.stderr.write("Permission denied to write log file ")
            return False



