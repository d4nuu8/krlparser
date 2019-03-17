#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def camel_to_snake(camel_string):
    return re.sub("([A-Z]+)", r"_\1", camel_string).lstrip("_").lower()
