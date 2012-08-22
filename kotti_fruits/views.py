# -*- coding: utf-8 -*-

import json

from pyramid.view import view_config

from kotti import DBSession
from kotti.resources import Image
from kotti.views.edit import ContentSchema
from kotti.views.edit import make_generic_add
from kotti.views.edit import make_generic_edit

from kotti_fruits.resources import FruitCategoriesFolder
from kotti_fruits.resources import FruitCategory
from kotti_fruits.resources import Fruit


class FruitCategoriesFolderSchema(ContentSchema):
    pass


class FruitCategorySchema(ContentSchema):
    pass


class FruitSchema(ContentSchema):
    pass



class FruitCategoriesFolderView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(context=FruitCategoriesFolder,
                 name='view',
                 permission='view',
                 renderer='templates/view/fruit-categories-folder-view.pt')
    def view(self):

        session = DBSession()
        query = session.query(FruitCategory)\
                       .filter(FruitCategory.parent_id == self.context.id)\
                       .order_by(FruitCategory.position)
        fruit_categories = query.all()

        return {"fruit_categories": fruit_categories}


class FruitCategoryView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(context=FruitCategory,
                 name='view',
                 permission='view',
                 renderer='templates/view/fruit-category-view.pt')
    def view(self):

        session = DBSession()
        query = session.query(Fruit)\
                       .filter(Fruit.parent_id == self.context.id)\
                       .order_by(Fruit.position)
        fruits = query.all()

        return {"fruits": fruits}


class FruitView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(context=Fruit,
                 name='view',
                 permission='view',
                 renderer='templates/view/fruit-view.pt')
    def view(self):

        session = DBSession()
        query = session.query(Fruit)\
                       .filter(Fruit.id == self.context.id)
        fruit = query.first()

        return {"fruit": fruit}


def includeme_add_and_edit_view(config):

    config.scan("kotti_fruits")

    config.add_view(make_generic_edit(FruitCategoriesFolderSchema()),
                    context=FruitCategoriesFolder,
                    name='edit',
                    permission='edit',
                    renderer='kotti:templates/edit/node.pt', )

    config.add_view(make_generic_add(FruitCategoriesFolderSchema(), FruitCategoriesFolder),
                    name=FruitCategoriesFolder.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )

    config.add_view(make_generic_edit(FruitCategorySchema()),
                    context=FruitCategory,
                    name='edit',
                    permission='edit',
                    renderer='kotti:templates/edit/node.pt', )

    config.add_view(make_generic_add(FruitCategorySchema(), FruitCategory),
                    name=FruitCategory.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )

    config.add_view(make_generic_edit(FruitSchema()),
                    context=Fruit,
                    name='edit',
                    permission='edit',
                    renderer='kotti:templates/edit/node.pt', )

    config.add_view(make_generic_add(FruitSchema(), Fruit),
                    name=Fruit.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )

def fruit_categories_view(request):
    return FruitCategory.fruit_categories_bunch(FruitCategory.name.desc())

def fruit_category_view(request):
    if request.method == 'POST':
        return FruitCategory.create_fruit_category(request)
    else:
        return FruitCategory.fruit_category(FruitCategory.name.desc(),
                                            request.matchdict['id'])

def fruits_view(request):
    return Fruit.fruits_bunch(Fruit.name.desc())

def fruit_view(request):
    if request.method == 'POST':
        return Fruit.create_fruit(request)
    else:
        return Fruit.fruit(Fruit.name.desc(), request.matchdict['id'])

def includeme_bunch_view(config):
    # The url for these is: /@@fruit_categories, or /@@fruits
    config.add_view(fruit_categories_view,
                    name='fruit_categories',
                    permission='view',
                    renderer='json')
    config.add_view(fruits_view,
                    name='fruits',
                    permission='view',
                    renderer='json')
    
def includeme_single_view(config):
    # The url for these is: /fruit_category/5, or /fruit/15
    config.add_route('fruit_category', 'fruit_category/{id}')
    config.add_view(fruit_category_view,
                    route_name='fruit_category',
                    permission='view',
                    renderer='json')
    config.add_route('fruit', 'fruit/{id}')
    config.add_view(fruit_view, route_name='fruit', permission='view', renderer='json')
    
def includeme(config):
    includeme_add_and_edit_view(config) 
    includeme_bunch_view(config) 
    includeme_single_view(config) 
