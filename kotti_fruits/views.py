# -*- coding: utf-8 -*-

from kotti import DBSession
from kotti.resources import Image
from kotti.views.edit import ContentSchema
from kotti.views.edit import make_generic_add
from kotti.views.edit import make_generic_edit
from pyramid.view import view_config
from resources import Fruit

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


def includeme(config):

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
