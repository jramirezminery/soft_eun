#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

__author__ = "Javier Ramírez, Alejandro Guillen"
__copyright__ = "Copyright 2021"
__credits__ = ["Soluciones Informaticas Roots", "Minery Report IT"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Javier Ramírez, Alejandro Guillen"
__email__ = "jramirez@mineryreport.com"
__status__ = "Development"

import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eun.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
