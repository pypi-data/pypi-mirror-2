from optparse import OptionParser
from ConfigParser import ConfigParser

### duplicate/extend ConfigParser functions as we can't use them directly :(

def getlist(string, separator=','):
  """returns a list from a string given a separator"""
  string = string.strip()
  if not string:
    return []
  return [i.strip() for i in string.split(separator)]

def getboolean(string):
  return string.lower() == 'true'


class Undefined(object):
  def __init__(self, default):
    self.default=default

class ConfigOptionParser(OptionParser):
  def __init__(self, defaults_section='DEFAULTS', dict_section=None,
               variables=None, **kwargs):
    """
    - defaults_section: section of .ini to look for configuration variables
    - dict_section: section of .ini to return as a dictionary
    - variables: attr on returned options to parse dictionary from command line
    """
    self.defaults_section = defaults_section
    self.dict_section = dict_section
    self.variables = variables
    if self.dict_section and not self.variables:
      self.variables = dict_section
    OptionParser.__init__(self, **kwargs)
    OptionParser.add_option(self,
                            '-c', '--config', dest='config', action='append',
                            help='ini file to read from')

  def add_option(self, *args, **kwargs):
    kwargs['default'] = Undefined(kwargs.get('default'))
    OptionParser.add_option(self, *args, **kwargs)

  def parse_args(self, args=None, values=None):
    options, args = OptionParser.parse_args(self, args, values)

    # get defaults from the configuration parser
    defaults = {}
    config = ConfigParser()
    if options.config:
      config.read(options.config)
      if self.defaults_section in config.sections():
        defaults = dict(config.items(self.defaults_section, raw=True))

    # option dict
    option_dict = dict([(i.dest, i) for i in self.option_list
                        if i.dest not in ('config', 'help')])

    # conversion functions for .ini data
    conversions = { 'store_true': getboolean,
                    'store_false': getboolean,
                    'append': getlist }

    # fill in the defaults not set from the command line
    for key, value in options.__dict__.items():
      
      # don't override command line arguments! they win!
      if isinstance(value, Undefined):

        if key in defaults and key in option_dict:
          # fill in options from .ini files

          option = option_dict[key]
          
          # converstion function
          function = conversions.get(option.action, lambda x: x)
          
          setattr(options, key, function(defaults[key]))
        else:
          # set from option defaults
          setattr(options, key, value.default)

    # get variables from dict_section and command line arguments
    # TODO: could do this first then interpolate the config file from these
    variables = {}
    if self.dict_section in config.sections():
      variables.update(dict(config.items(self.dict_section, raw=True)))
    if self.variables:
      variables.update(dict([i.split('=',1) for i in args if '=' in i]))
      args = [i for i in args if '=' not in i]
      setattr(options, self.variables, variables)
    
    return (options, args)
      
