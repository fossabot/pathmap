# -*- coding: utf-8 -*-
from .pathmap import (
    clean_path,
    _check_ancestors,
    _slash_pattern,
    _resolve_path,
    _resolve_path_if_long,
    resolve_paths,
    resolve_by_method
)

from .utils import  (
    _extract_match
)

from .tree import Tree


__version__ = '0.1.0'
