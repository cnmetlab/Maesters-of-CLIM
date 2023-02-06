import toml

import os

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def load_config(name:str):
    configfile = os.path.join(PACKAGE_DIR, 'config', f'{name}.toml')
    with open(configfile, 'r') as f:
        config = toml.load(f)
    return config
