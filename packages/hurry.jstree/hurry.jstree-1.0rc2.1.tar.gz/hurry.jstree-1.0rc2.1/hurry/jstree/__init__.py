from hurry.resource import Library, ResourceInclusion
from hurry.jquery import jquery

jstree_lib = Library('jstree', 'jstree-build')

# XXX: Separate eggs for these 2
jqhotkeys = ResourceInclusion(
    jstree_lib, '_lib/jquery.hotkeys.js',
    depends=[jquery])
jqcookie = ResourceInclusion(
    jstree_lib, '_lib/jquery.cookie.js',
    depends=[jquery])

# XXX minified version would be nice
jstree = ResourceInclusion(
    jstree_lib, 'jquery.jstree.js',
    depends=[jquery, jqhotkeys, jqcookie])
