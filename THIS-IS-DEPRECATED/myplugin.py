# -*- coding: utf-8 -*-
"""
Contains classes and utilities related to meta data in hyde.
"""

from collections import namedtuple
from functools import partial
from itertools import ifilter
from operator import attrgetter
import re
import sys

from hyde.exceptions import HydeException
from hyde.model import Expando
from hyde.plugin import Plugin
from hyde.site import Node, Resource
from hyde.util import add_method, add_property, pairwalk

import traceback
from fswrap import File, Folder
import yaml


def is_active(resource, menu_item):
    try:

        url = menu_item.get('url', None)
        if url is None:
            return False
        if url.endswith('/'):
            url += 'index.html'
        if resource.source.path.endswith(url):
            return 'active'
    except:
            traceback.print_exc()
            raise

class MyPlugin(Plugin):
    def __init__(self, site):
        self.site = site.is_active = is_active
