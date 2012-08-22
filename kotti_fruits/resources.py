import transaction
import ast
import uuid
import os

from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from kotti import DBSession
from kotti.security import SITE_ACL
from kotti.resources import Node
from kotti.resources import Content
from kotti.resources import Image
from kotti.populate import populate as kotti_populate

from kotti_fruits.static import images

from fixtures import fruit_categories, fruit_data


class FruitCategoriesFolder(Content):
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    type_info = Content.type_info.copy(
        name=u'FruitCategoriesFolder',
        title=u'FruitCategoriesFolder',
        add_view=u'add_fruit_categories_folder',
        addable_to=[u'Document', u'FruitCategoriesFolder'],
        )

    def __init__(self, **kwargs):
        super(FruitCategoriesFolder, self).__init__(**kwargs)


class FruitCategory(Content):
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    fruit_categories_folder_id = Column(Integer(), ForeignKey('nodes.id'))
    fruit_categories_folder = relationship(
            "Node",
            backref=backref('fruit_categories'),
            primaryjoin='Node.id==FruitCategory.fruit_categories_folder_id')

    type_info = Content.type_info.copy(
        name=u'FruitCategory',
        title=u'FruitCategory',
        add_view=u'add_fruit_category',
        addable_to=[u'FruitCategoriesFolder'],
        )

    def __init__(self, **kwargs):
        super(FruitCategory, self).__init__(**kwargs)

    def make_record(r, fruits):
        fruit_ids = \
                [fruit.id for fruit in fruits if fruit.__parent__.id == r.id]
        fruit_categories_folder = r.__parent__
        return {u'id': r.id,
                u'title': r.title,
                u'fruit_ids': fruit_ids,
                u'fruit_categories_folder': fruit_categories_folder.id}

    @classmethod
    def fruit_category(self, cls, id_wanted):
        r = DBSession.query(FruitCategory).filter_by(id=id_wanted).first()
        if r is not None:
            fruits = DBSession.query(Fruit).all()
            return self.make_record(r, fruits)
        else:
            return None

    @classmethod
    def update_fruit_category(self, request, cls, id_wanted):
        data = ast.literal_eval(request.body)
        print data
        r = DBSession.query(FruitCategory).filter_by(id=id_wanted).first()
        if r is not None:
            # only update the parent and primary properties
            # (updates to children happen there)
            r.fruit_categories_folder = data['fruit_categories_folder']
            r.title = data['title']
            fruits = DBSession.query(Fruit).all()
            return self.make_record(r, fruits)
        else:
            return None

    @classmethod
    def fruit_categories_bunch(cls, order_by, how_many=10):
        # fruit_categories contain fruits
        ret = []
        fruits = DBSession.query(Fruit).all()
        for r in DBSession.query(FruitCategory).all():
            ret.append(cls.make_record(r, fruits))
        return ret

    @classmethod
    def create_fruit_category(self, request):
        data = ast.literal_eval(request.body)
        # Assume only one fruit_categories folder.
        fruit_categories_folder = \
                DBSession.query(FruitCategoriesFolder).first()
        name = str(uuid.uuid4())
        fruit_category = FruitCategory(name=name,
                                       title=data['title'],
                                       parent=fruit_categories_folder)
        fruit_category.__acl__ = SITE_ACL
        session = DBSession()
        session.add(fruit_category)
        session.flush()
        transaction.commit()
        fruit_category = \
                DBSession.query(FruitCategory).filter_by(name=name).first()
        ret = {u'id': fruit_category.id,
               u'title': fruit_category.title}
        return ret


class Fruit(Content):
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    calories              = Column(Integer(), info='Calories')
    calories_from_fat     = Column(Integer(), info='Calories from Fat')
    total_fat_g           = Column(Integer(), info='Total Fat (g)')
    total_fat_dv          = Column(Integer(), info='Total Fat (%DV)')
    sodium_mg             = Column(Integer(), info='Sodium (mg)')
    sodium_dv             = Column(Integer(), info='Sodium (%DV)')
    potassium_mg          = Column(Integer(), info='Potassium (mg)')
    potassium_dv          = Column(Integer(), info='Potassium (%DV)')
    total_carbohydrate_g  = Column(Integer(), info='Total Carbohydrate (g)')
    total_carbohydrate_dv = Column(Integer(), info='Total Carbohydrate (%DV)')
    dietary_fiber_g       = Column(Integer(), info='Dietary Fiber (g)')
    dietary_fiber_dv      = Column(Integer(), info='Dietary Fiber (%DV)')
    sugars_g              = Column(Integer(), info='Sugars (g)')
    protein_g             = Column(Integer(), info='Protein (g)')
    vitamin_a_dv          = Column(Integer(), info='Vitamin A (%DV)')
    vitamin_c_dv          = Column(Integer(), info='Vitamin C (%DV)')
    calcium_dv            = Column(Integer(), info='Calcium (%DV)')
    iron_dv               = Column(Integer(), info='Iron (%DV)')

    fruit_category_id = Column(Integer(), ForeignKey('nodes.id'))
    fruit_category = \
        relationship("Node",
                     backref=backref('fruits'),
                     primaryjoin='Node.id==Fruit.fruit_category_id')

    type_info = Content.type_info.copy(
        name=u'Fruit',
        title=u'Fruit',
        add_view=u'add_fruit',
        addable_to=[u'FruitCategory'],
        )

    def __init__(self, calories=0, calories_from_fat=0, total_fat_g=0,
                 total_fat_dv=0, sodium_mg=0, sodium_dv=0, potassium_mg=0,
                 potassium_dv=0, total_carbohydrate_g=0,
                 total_carbohydrate_dv=0, dietary_fiber_g=0,
                 dietary_fiber_dv=0, sugars_g=0, protein_g=0, vitamin_a_dv=0,
                 vitamin_c_dv=0, calcium_dv=0, iron_dv=0,
                 **kwargs):

        super(Fruit, self).__init__(**kwargs)

        self.calories              = calories
        self.calories_from_fat     = calories_from_fat
        self.total_fat_g           = total_fat_g
        self.total_fat_dv          = total_fat_dv
        self.sodium_mg             = sodium_mg
        self.sodium_dv             = sodium_dv
        self.potassium_mg          = potassium_mg
        self.potassium_dv          = potassium_dv
        self.total_carbohydrate_g  = total_carbohydrate_g
        self.total_carbohydrate_dv = total_carbohydrate_dv
        self.dietary_fiber_g       = dietary_fiber_g
        self.dietary_fiber_dv      = dietary_fiber_dv
        self.sugars_g              = sugars_g
        self.protein_g             = protein_g
        self.vitamin_a_dv          = vitamin_a_dv
        self.vitamin_c_dv          = vitamin_c_dv
        self.calcium_dv            = calcium_dv
        self.iron_dv               = iron_dv

    def make_record(r):
        return {u'fruit_category_id': r.__parent__.id,
                u'id': r.id,
                u'name': r.name,
                u'title': r.title,
                u'calories': r.calories,
                u'calories_from_fat': r.calories_from_fat,
                u'total_fat_g': r.total_fat_g,
                u'total_fat_dv': r.total_fat_dv,
                u'sodium_mg': r.sodium_mg,
                u'sodium_dv': r.sodium_dv,
                u'potassium_mg': r.potassium_mg,
                u'potassium_dv': r.potassium_dv,
                u'total_carbohydrate_g': r.total_carbohydrate_g,
                u'total_carbohydrate_dv': r.total_carbohydrate_dv,
                u'dietary_fiber_g': r.dietary_fiber_g,
                u'dietary_fiber_dv': r.dietary_fiber_dv,
                u'sugars_g': r.sugars_g,
                u'protein_g': r.protein_g,
                u'vitamin_a_dv': r.vitamin_a_dv,
                u'vitamin_c_dv': r.vitamin_c_dv,
                u'calcium_dv': r.calcium_dv,
                u'iron_dv': r.iron_dv}

    @classmethod
    def fruit(self, cls, id_wanted):
        r = DBSession.query(Fruit).filter_by(id=id_wanted).first()
        if r is not None:
            return self.make_record(r)
        else:
            return None

    @classmethod
    def fruits_bunch(cls, order_by, how_many=10):
        ret = []
        for r in DBSession.query(Fruit).all():
            ret.append(cls.make_record(r))
        return ret

    @classmethod
    def create_fruit(self, request):
        data = ast.literal_eval(request.body)
        fruit_category = \
                DBSession.query(FruitCategory).filter_by(
                        id=data['fruit_category']).first()
        name = str(uuid.uuid4())

        fruit = Fruit(parent=fruit_category)
        fruit.__acl__ = SITE_ACL
        session = DBSession()
        session.add(fruit)
        session.flush()
        transaction.commit()
        fruit = DBSession.query(Fruit).filter_by(name=name).first()
        ret = {u'id': fruit.id,
               u'title': fruit.title,
               u'fruit_category': fruit.__parent__.id}
        return ret


def get_root(request=None):
    session = DBSession()
    return session.query(Content).filter(Content.parent_id==None).first()


def fruit_data_args_dict(fruit_name, fruit_category_obj):
    f = fruit_data[fruit_name]
    return {'name': fruit_name,
            'title': fruit_name,
            'parent': fruit_category_obj,
            'calories': f['calories'],
            'calories_from_fat': f['calories_from_fat'],
            'total_fat_g': f['total_fat_g'],
            'total_fat_dv': f['total_fat_dv'],
            'sodium_mg': f['sodium_mg'],
            'sodium_dv': f['sodium_dv'],
            'potassium_mg': f['potassium_mg'],
            'potassium_dv': f['potassium_dv'],
            'total_carbohydrate_g': f['total_carbohydrate_g'],
            'total_carbohydrate_dv': f['total_carbohydrate_dv'],
            'dietary_fiber_g': f['dietary_fiber_g'],
            'dietary_fiber_dv': f['dietary_fiber_dv'],
            'sugars_g': f['sugars_g'],
            'protein_g': f['protein_g'],
            'vitamin_a_dv': f['vitamin_a_dv'],
            'vitamin_c_dv': f['vitamin_c_dv'],
            'calcium_dv': f['calcium_dv'],
            'iron_dv': f['iron_dv']}


def populate():
    session = DBSession()
    if session.query(Node).count() == 0:
        kotti_populate()

        root_document = \
                session.query(Content).filter(Content.parent_id==None).first()

        fruit_categories_folder = \
                FruitCategoriesFolder(name=u"fruit_categories_folder",
                                      title=u"Fruit Categories Folder",
                                      in_navigation=False,
                                      parent=root_document)

        fruit_categories_folder.__acl__ = SITE_ACL
        session.add(fruit_categories_folder)

        folder = \
                session.query(Content).filter_by(
                        name=u"fruit_categories_folder").first()

        fruit_category_instances = {}
        for fruit_category in fruit_categories:
            fruit_category_instances[fruit_category] = \
                FruitCategory(name=fruit_categories[fruit_category]['name'],
                              title=fruit_categories[fruit_category]['name'],
                              parent=folder)

        for key in fruit_category_instances:
            fruit_category_instances[key].__acl__ = SITE_ACL
            session.add(fruit_category_instances[key])

        fruit_instances = {}
        for fruit_category in fruit_categories:
            fruit_category_obj = \
                    DBSession.query(FruitCategory).filter_by(
                            title=fruit_category).first()
            for fruit_name in fruit_categories[fruit_category]['fruits']:
                fruit_instances[fruit_name] = \
                    Fruit(**fruit_data_args_dict(fruit_name,
                                                 fruit_category_obj))

        for key in fruit_instances:
            fruit_instances[key].__acl__ = SITE_ACL
            session.add(fruit_instances[key])

            # images have filenames with format: apple.256.jpg
            for size in [32, 64, 128, 256, 512]:
                image_filename = "{0}.{1}.jpg".format(key, size)
                image_path = os.path.join(os.path.dirname(images.__file__),
                                          image_filename)
                image = open(image_path, 'rb').read()
                fruit_instances[key][image_filename] = \
                        Image(image,
                              image_filename,
                              u"image/jpeg",
                              title=image_filename)
                fruit_instances[key][image_filename].__acl__ = SITE_ACL
                session.add(fruit_instances[key][image_filename])

    session.flush()
    transaction.commit()
