# -*- coding: utf-8 -*-

from colander import SchemaNode
from colander import Integer

from kotti import DBSession

from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView

from kotti.resources import Image

from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_fruits import _
from kotti_fruits.resources import FruitCategoriesFolder
from kotti_fruits.resources import FruitCategory
from kotti_fruits.resources import Fruit
from kotti_fruits.fanstatic import kotti_fruits


class AppView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(name='app',
                 permission='view',
                 renderer='templates/app.pt')
    def view(self):

        kotti_fruits.need()

        return {}


##########################
#  FruitCategoriesFolder
##########################


class FruitCategoriesFolderSchema(ContentSchema):
    pass


@view_config(name=FruitCategoriesFolder.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class FruitCategoriesFolderAddForm(AddFormView):

    schema_factory = FruitCategoriesFolderSchema
    add = FruitCategoriesFolder
    item_type = _(u"FruitCategoriesFolder")


@view_config(name='edit',
             context=FruitCategoriesFolder,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class FruitCategoriesFolderEditForm(EditFormView):

    schema_factory = FruitCategoriesFolderSchema


@view_defaults(context=FruitCategoriesFolder, permission='view')
class FruitCategoriesFolderView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(name='view',
                 renderer='kotti_fruits:templates/fruit-categories-folder-view.pt')
    def view(self):

        session = DBSession()
        query = session.query(FruitCategory)\
                       .filter(FruitCategory.parent_id == self.context.id)\
                       .order_by(FruitCategory.position)
        fruit_categories = query.all()

        return {"fruit_categories": fruit_categories}

    @view_config(name='alternative-view',
                 renderer='kotti_fruits:templates/fruits-alternative.pt')
    def alternative_view(self):

        session = DBSession()
        query = session.query(FruitCategory)\
                       .filter(FruitCategory.parent_id == self.context.id)\
                       .order_by(FruitCategory.position)
        fruit_categories = query.all()

        return {"fruit_categories": fruit_categories}


###################
#  FruitCategory
###################


class FruitCategorySchema(ContentSchema):
    pass


@view_config(name=FruitCategory.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class FruitCategoryAddForm(AddFormView):

    schema_factory = FruitCategorySchema
    add = FruitCategory
    item_type = _(u"FruitCategory")


@view_config(name='edit',
             context=FruitCategory,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class FruitCategoryEditForm(EditFormView):

    schema_factory = FruitCategorySchema


class FruitCategoryView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(context=FruitCategory,
                 name='view',
                 permission='view',
                 renderer='templates/fruit-category-view.pt')
    def view(self):

        session = DBSession()
        query = session.query(Fruit)\
                       .filter(Fruit.parent_id == self.context.id)\
                       .order_by(Fruit.position)
        fruits = query.all()

        return {"fruits": fruits}


##########
#  Fruit
##########


class FruitSchema(ContentSchema):
    """Schema for add / edit forms of Fruit"""

    calories = SchemaNode(
            Integer(),
            title=_('Calories'),
            missing=u"")
    calories_from_fat = SchemaNode(
            Integer(),
            title=_('Calories from Fat'),
            missing=u"")
    total_fat_g = SchemaNode(
            Integer(),
            title=_('Total Fat (g)'),
            missing=u"")
    total_fat_dv = SchemaNode(
            Integer(),
            title=_('Total Fat (%DV)'),
            missing=u"")
    sodium_mg = SchemaNode(
            Integer(),
            title=_('Sodium (mg)'),
            missing=u"")
    sodium_dv = SchemaNode(
            Integer(),
            title=_('Sodium (%DV)'),
            missing=u"")
    potassium_mg = SchemaNode(
            Integer(),
            title=_('Potassium (mg)'),
            missing=u"")
    potassium_dv = SchemaNode(
            Integer(),
            title=_('Potassium (%DV)'),
            missing=u"")
    total_carbohydrate_g = SchemaNode(
            Integer(),
            title=_('Total Carbohydrate (g)'),
            missing=u"")
    total_carbohydrate_dv = SchemaNode(
            Integer(),
            title=_('Total Carbohydrate (%DV)'),
            missing=u"")
    dietary_fiber_g = SchemaNode(
            Integer(),
            title=_('Dietary Fiber (g)'),
            missing=u"")
    dietary_fiber_dv = SchemaNode(
            Integer(),
            title=_('Dietary Fiber (%DV)'),
            missing=u"")
    sugars_g = SchemaNode(
            Integer(),
            title=_('Sugars (g)'),
            missing=u"")
    protein_g = SchemaNode(
            Integer(),
            title=_('Protein (g)'),
            missing=u"")
    vitamin_a_dv = SchemaNode(
            Integer(),
            title=_('Vitamin A (%DV)'),
            missing=u"")
    vitamin_c_dv = SchemaNode(
            Integer(),
            title=_('Vitamin C (%DV)'),
            missing=u"")
    calcium_dv = SchemaNode(
            Integer(),
            title=_('Calcium (%DV)'),
            missing=u"")
    iron_dv = SchemaNode(
            Integer(),
            title=_('Iron (%DV)'),
            missing=u"")


@view_config(name=Fruit.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class FruitAddForm(AddFormView):

    schema_factory = FruitSchema
    add = Fruit
    item_type = _(u"Fruit")


@view_config(name='edit',
             context=Fruit,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class FruitEditForm(EditFormView):

    schema_factory = FruitSchema


class FruitView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(context=Fruit,
                 name='view',
                 permission='view',
                 renderer='templates/fruit-view.pt')
    def view(self):

        session = DBSession()
        query = session.query(Fruit)\
                       .filter(Fruit.id == self.context.id)
        fruit = query.first()

        image = None

        for child in self.context.children:
            if type(child) == Image:
                image = child
                break

        return {"fruit": fruit, "image": image}


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
        return Fruit.fruit(Fruit.name.desc(),
                           request.matchdict['id'])


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
    config.add_view(fruit_view,
                    route_name='fruit',
                    permission='view',
                    renderer='json')


def includeme(config):
    includeme_bunch_view(config)
    includeme_single_view(config)
