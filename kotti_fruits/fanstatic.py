from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery import jquery
from js.angular import angular


library = Library('kotti_fruits', 'static')

css = Resource(
    library,
    'css/style.css',
    minified='css/style.min.css'
)

js = Resource(
    library,
    'js/script.js',
    minified='js/script.min.js',
    depends=[jquery, angular]
)

fruit_categories_js = Resource(
    library,
    'js/controllers/fruit_categories_list.js',
    #minified='js/controllers/fruit_categories_list.min.js',
    depends=[angular]
)

fruits_js = Resource(
    library,
    'js/controllers/fruits_list.js',
    #minified='js/controllers/fruits_list.min.js',
    depends=[angular]
)

kotti_fruits = Group([css, js, fruit_categories_js, fruits_js,])
