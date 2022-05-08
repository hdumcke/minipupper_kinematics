import os

import yaml
from munch import munchify

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader as SafeLoader


def get_config(name):
    if 'VIRTUAL_ENV' in os.environ:
        default_filenames = [
            # DEV
            "%s/etc/%s/%s.yaml" % (os.path.dirname(os.path.dirname(__file__)), name, name),
            # VIRTUAL_ENV
            "%s/etc/%s/%s.yaml" % (os.environ['VIRTUAL_ENV'], name, name),
            # SYSTEM
            "/etc/%s/%s.yaml" % (name, name),
        ]
    else:
        default_filenames = ["/etc/%s/%s.yaml" % (name, name)]

    for filename in default_filenames:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                conf = munchify(yaml.load(f.read(), SafeLoader))
                conf.config_file = filename
                return conf


CONF = get_config('minipupper')
