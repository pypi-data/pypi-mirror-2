# Default configuration for external tests.
from conchoctopus.connect import default_config_opts as config_opts

user='test'
host='localhost'
port=22
config_opts.update(dict(
        auth_methods=['publickey']))
