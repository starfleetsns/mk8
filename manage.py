#!/usr/bin/env python3
import os
import sys

import collections
import collections.abc as abc
# Money patch collections to make the site work again
collections.Iterator = abc.Iterator
collections.Mapping = abc.Mapping
collections.Sequence = abc.Sequence

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mk8.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
