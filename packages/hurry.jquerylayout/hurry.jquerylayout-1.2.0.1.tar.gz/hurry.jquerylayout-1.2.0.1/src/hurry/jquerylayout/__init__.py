from hurry.resource import Library, ResourceInclusion
from hurry.jquery import jquery
from hurry.jqueryui import jqueryui

jquerylayout_lib = Library('jquerylayout', 'jquerylayout-build')

jquerylayout = ResourceInclusion(
    jquerylayout_lib, 'jquery.layout.js',
    depends=[jquery, jqueryui],
    minified='jquery.layout.min.js')
