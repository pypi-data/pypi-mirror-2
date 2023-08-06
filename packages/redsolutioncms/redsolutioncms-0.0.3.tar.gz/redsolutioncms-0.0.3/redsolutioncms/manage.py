#!/usr/bin/env python
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
])
sys.path[0:0] = [
    os.path.abspath(current_dir),
    os.path.abspath(os.path.join(current_dir, '..', 'parts', 'django')),
    os.path.abspath(os.path.join(current_dir, '..', 'eggs', 'zc.buildout-1.5.1-py2.6.egg')),
    os.path.abspath(os.path.join(current_dir, '..', 'eggs', 'zc.buildout-1.5.1-py2.5.egg')),
    os.path.abspath(os.path.join(current_dir, '..', 'eggs', 'setuptools-0.6c12dev_r84273-py2.6.egg')),
    os.path.abspath(os.path.join(current_dir, '..', 'eggs', 'setuptools-0.6c12dev_r84273-py2.5.egg')),
]

from manage_additional import *

from django.core.management import execute_manager
try:
    import settings_additional as settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
