#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_revolver
----------------------------------

Tests for `pathmap` module.
"""

import pytest

from pathmap import (
    clean_path,
    _slash_pattern,
    _extract_match,
    _resolve_path,
    _check_ancestors,
    resolve_paths,
    resolve_by_method,
    Tree
)

# ========== Mock data ===========
before = [
    'not/found.py',
    '/Users/user/owner/repo/src/components/login.js',
    'site-packages/package/__init__.py',
    'path.py',
    'a/b/../Path With\\ Space'
]

after = [
    None,
    'src/components/login.js',
    'package/__init__.py',
    'path.py',
    'a/Path With Space'
]

toc = ','.join(map(lambda x: "" if x is None else x, after)) + ','


# ========= END Mock data ==========
def test_clean_path():
    path = '**/some/directory'
    assert clean_path(path) == 'some/directory'
    path = 'some/path\r/with/tabs\r'
    assert clean_path(path) == 'some/path/with/tabs'
    path = 'some\ very_long/directory\ name'
    assert clean_path(path) == 'some very_long/directory name'
    path = 'ms\\style\\directory'
    assert clean_path(path) == 'ms/style/directory'


def test_slash_pattern():
    has_slash = 'slash/'
    assert _slash_pattern(has_slash) == 'slash/'


def test_extract_match():
    toc = ',src/components/login.js,'
    index = toc.find('components')
    extracted = _extract_match(toc, index)
    assert extracted == 'src/components/login.js'


def test_resolve_path():
    # short to long
    path = 'Src/components/login.js'
    tree = Tree()
    tree.construct_tree(toc)
    new_path  = _resolve_path(tree, path)
    assert new_path == 'src/components/login.js'

def test_resolve_paths():
    resolved_paths = resolve_paths(toc, before)
    first = set([r for r in resolved_paths])
    second = set(after)

    assert first == second


def test_resolve_by_method():
    resolver = resolve_by_method(toc)
    assert callable(resolver)
    first = set(map(resolver, before))
    second = set(after)
    assert first == second


def test_check_ancestors():
    assert _check_ancestors('a', 'a', 1) is True, 'matches'
    assert _check_ancestors('A', 'a', 1) is True, 'matches case insensative'
    assert _check_ancestors('a/B', 'a/B', 1) is True, 'matches'
    assert _check_ancestors('A/B', 'a/b', 1) is True, 'matches case insensative'
    assert _check_ancestors('b/b', 'a/b', 1) is False, 'does not match first ancestor'
    assert _check_ancestors('a/b/c', 'x/b/c', 1) is True
    assert _check_ancestors('a/b/c', 'x/b/c', 2) is False
    assert _check_ancestors('a/b/c/d', 'X/B/C/D', 2) is True


def test_resolve_paths_with_ancestors():
    toc = ',x/y/z,'
    tree = Tree()
    tree.construct_tree(toc)

    # default, no ancestors ============================
    paths    = ['z', 'R/z', 'R/y/z', 'x/y/z', 'w/x/y/z']
    expected = [None, None, None, 'x/y/z', 'x/y/z']
    resolved = list(resolve_paths(toc, paths))
    assert resolved  == expected

    # one ancestors ====================================
    paths = ['z', 'R/z', 'R/y/z', 'x/y/z', 'w/x/y/z']
    expected = [None, None, None, 'x/y/z', 'x/y/z']
    resolved = list(resolve_paths(toc, paths, 1))
    assert set(resolved) == set(expected)

    # two ancestors ====================================
    paths = ['z', 'R/z', 'R/y/z', 'x/y/z', 'w/x/y/z']
    expected = [None, None, None,  'x/y/z', 'x/y/z']
    resolved = list(resolve_paths(toc, paths, 2))
    assert set(resolved) == set(expected)


def test_case_sensitive_ancestors():
    toc = ',src/HeapDump/GCHeapDump.cs,'
    tree = Tree()
    tree.construct_tree(toc)
    path = 'C:/projects/perfview/src/heapDump/GCHeapDump.cs'
    new_path = _resolve_path(tree, path, 1)
    assert new_path == 'src/HeapDump/GCHeapDump.cs'


def test_path_should_not_resolve():
    toc = ',four/six/three.py,'
    path = 'four/six/seven.py'
    tree = Tree()
    tree.construct_tree(toc)
    path = _resolve_path(tree, path)
    assert path is None

def test_path_should_not_resolve_case_insensative():
    resolvers = []
    toc = ',a/b/C,'
    path = 'a/B/c'
    tree = Tree()
    tree.construct_tree(toc)
    path  = _resolve_path(tree, path)
    assert path == 'a/b/C'

def test_resolve_path_shortest():
    tree = Tree()
    tree.construct_tree(',a/b/c.py,b/c.py,')
    new_path = _resolve_path(tree, 'r/b/c.py')
    assert new_path == 'b/c.py'
