# -*- coding: utf-8 -*-
"""
This module provides utility functions for modules.
"""


def filter_lines(lines, comment='#'):
    """ Filter lines by removing comments and empty lines
    """
    filtered_list = []
    for line in lines:
        line = line.strip()
        if not line.startswith(comment) and line != '':
            filtered_list.append(line)
    return filtered_list
