import transaction
import ast
import uuid

from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from kotti import get_settings
from kotti import DBSession
from kotti.security import get_principals
from kotti.security import SITE_ACL
from kotti.resources import Content
from kotti.resources import Document
from kotti.populate import populate as kotti_populate


class FruitCategoriesFolder(Content):
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    type_info = Content.type_info.copy(
        name=u'FruitCategoriesFolder',
        title=u'FruitCategoriesFolder',
        add_view=u'add_fruit_categories_folder',
        addable_to=[u'Document', u'FruitCategoriesFolder'],  # [TODO] How to do? to root?
        )

    def __init__(self, **kwargs):
        super(FruitCategoriesFolder, self).__init__(**kwargs)


class FruitCategory(Content):
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    fruit_category_folder_id = Column(Integer(), ForeignKey('nodes.id'))
    fruit_category_folder = \
        relationship("Node",
                     backref=backref('fruit_categories'),
                     primaryjoin='Node.id==FruitCategory.fruit_category_folder_id')

    type_info = Content.type_info.copy(
        name=u'FruitCategory',
        title=u'FruitCategory',
        add_view=u'add_fruit_category',
        addable_to=[u'FruitCategoriesFolder'],
        )

    def __init__(self, **kwargs):
        super(FruitCategory, self).__init__(**kwargs)

#    def make_record(r):
#        fruits = DBSession.query(Fruit).all()
#        fruit_ids = [fruit.id for fruit in fruits if fruit.name == r.name]
#        fruit_category_folder = r.__parent__.__parent__
#        return { u'id': r.id, 
#                 u'title': r.title, 
#                 u'fruits': fruit_ids, 
#                 u'fruit_category_folder': fruit_category_folder.id }
#
#    @classmethod
#    def fruit_category(self, cls, id_wanted):
#        r = DBSession.query(FruitCategory).filter_by(id=id_wanted).first()
#        if r is not None:
#            self.make_record(r)
#        else:
#            return None
#
#    @classmethod
#    def update_fruit_category(self, request, cls, id_wanted):
#        data = ast.literal_eval(request.body) 
#        print data
#        r = DBSession.query(FruitCategory).filter_by(id=id_wanted).first()
#        if r is not None:
#            # only update the parent and primary properties
#            # (updates to children happen there)
#            r.fruit_category_folder = data['fruit_category_folder']
#            r.title = data['title']
#            return self.make_record(r)
#        else:
#            return None
#
#    @classmethod
#    def fruit_categories_bunch(cls, order_by, how_many=10):
#        # fruit_categories contain fruits
#        ret = []
#        fruits = DBSession.query(Fruit).all()
#        for fruit_category in DBSession.query(FruitCategory).all():
#            fruit_ids = [fruit.id for fruit in fruits if fruit.name == fruit_category.name]
#            fruit_category_folder = fruit_category.__parent__.__parent__
#            ret.append({ u'id': fruit_category.id, 
#                         u'title': fruit_category.title,
#                         u'fruits': fruit_ids,
#                         u'fruit_category_folder': fruit_category_folder.id })
#        return ret
#
#    @classmethod
#    def create_fruit_category(self, request): 
#        data = ast.literal_eval(request.body) 
#        # Later can have multiple fruit_categories folders, maybe, but now assume 1
#        fruit_categories_folder = DBSession.query(FruitCategoriesFolder).first()
#        name = str(uuid.uuid4())
#        fruit_category = FruitCategory(name=name,
#                                       title=data['title'], 
#                                       parent=fruit_categories_folder)
#        fruit_category.__acl__ = SITE_ACL
#        session = DBSession()
#        session.add(fruit_category)
#        session.flush()
#        transaction.commit()
#        fruit_category = DBSession.query(FruitCategory).filter_by(name=name).first()
#        ret = { u'id': fruit_category.id, 
#                u'title': fruit_category.title }
#        return ret
#

class Fruit(Content):
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    calories              = Column(Integer(), info='Calories')
    calories_from_fat     = Column(Integer(), info='Calories from Fat')
    total_fat_g           = Column(Integer(), info='Total Fat (g)')
    total_fat_dv          = Column(Integer(), info='Total Fat (%DV)')
    sodium_mg             = Column(Integer(), info='Sodium (mg)')
    sodium_dv             = Column(Integer(), info='Sodium (%DV)')
    potassium_g           = Column(Integer(), info='Potassium (mg)')
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

    def __init__(self, calories=0, calories_from_fat=0, total_fat_g=0, total_fat_dv=0, sodium_mg=0, sodium_dv=0, potassium_g=0, potassium_dv=0, total_carbohydrate_g=0, total_carbohydrate_dv=0, dietary_fiber_g=0, dietary_fiber_dv=0, sugars_g=0, protein_g=0, vitamin_a_dv=0, vitamin_c_dv=0, calcium_dv=0, iron_dv=0, **kwargs):
        super(Fruit, self).__init__(**kwargs)
        self.calories              = calories
        self.calories_from_fat     = calories_from_fat
        self.total_fat_g           = total_fat_g
        self.total_fat_dv          = total_fat_dv
        self.sodium_mg             = sodium_mg
        self.sodium_dv             = sodium_dv
        self.potassium_g           = potassium_g
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

#    def make_record(r):
#        fruit_category = DBSession.query(FruitCategory).filter_by(name=r.name).first()
#        return { u'id': r.id, 
#                 u'name': r.name, 
#                 u'title': r.title, 
#                 u'fruit_category_id': r.__parent__.id }
#
#    @classmethod
#    def fruit(self, cls, id_wanted):
#        r = DBSession.query(Fruit).filter_by(id=id_wanted).first()
#        if r is not None:
#            self.make_record(r)
#        else:
#            return None
#
#    @classmethod
#    def fruits_bunch(cls, order_by, how_many=10):
#        ret = []
#        for r in DBSession.query(Fruit).all():
#            fruit_category = DBSession.query(FruitCategory).filter_by(name=r.name).first()
#            ret.append({ u'id': r.id, u'name': r.name, u'fruit_category': fruit_category.id })
#        return ret
#
#    @classmethod
#    def create_fruit(self, request): 
#        data = ast.literal_eval(request.body) 
#        fruit_category = DBSession.query(FruitCategory).filter_by(id=data['fruit_category']).first()
#        name = str(uuid.uuid4())
#
#        fruit = Fruit(parent=fruit_category)
#        fruit.__acl__ = SITE_ACL
#        session = DBSession()
#        session.add(fruit)
#        session.flush()
#        transaction.commit()
#        fruit = DBSession.query(Fruit).filter_by(name=name).first()
#        ret = { u'id': fruit.id, 
#                u'title': fruit.title,
#                u'fruit_category': fruit.__parent__.id }
#        return ret

def get_root(request=None):
    session = DBSession()
    return session.query(Content).filter(Content.parent_id==None).first()

def populate():
    session = DBSession()
    #nodecount = session.query(Content).count()
    go = 1
    if go == 1:
        kotti_populate()
        #root = Document(parent=None, title=u"My Site")
        #root.__acl__ = SITE_ACL
        #session.add(root)

        root_document = session.query(Content).filter(Content.parent_id==None).first()
        print
        print
        print root_document
        print root_document['about']
        print
        print

        #session.delete(root_document)

        from fixtures import fruit_categories, fruit_data, fruit_data_names

        fruit_categories_folder = \
                FruitCategoriesFolder(name=u"fruit_categories_folder",
                                      title=u"Fruit Categories",
                                      in_navigation=False,
                                      parent=root_document)

        fruit_categories_folder.__acl__ = SITE_ACL
        session.add(fruit_categories_folder)

        folder = session.query(Content).filter_by(name=u"fruit_categories_folder").first()

        fruit_category_instances = {}
        for fruit_category in fruit_categories:
            fruit_category_instances[fruit_category] = \
                FruitCategory(name=fruit_categories[fruit_category]['name'],
                              title=fruit_categories[fruit_category]['name'],
                              parent=folder)

        for key in fruit_category_instances:
            fruit_category_instances[key].__acl__ = SITE_ACL
            session.add(fruit_category_instances[key])

        # Find the fruit_categories
        fruit_category_results = DBSession.query(FruitCategory).all()

        fruit_instances = {}
        for fruit_category in fruit_categories:
            fruit_category_obj = \
                    DBSession.query(FruitCategory).filter_by(title=fruit_category).first()
            for fruit_name in fruit_categories[fruit_category]['fruits']:
                        #Fruit(**dict({'fruit_category_id': fruit_category_obj.id,
                fruit_instances[fruit_name] = \
                        Fruit(**dict({'name': fruit_name,
                                      'title': fruit_name,
                                      'parent': fruit_category_obj,
                                      'calories': fruit_data[fruit_name]['calories'],
                                      'calories_from_fat': fruit_data[fruit_name]['calories_from_fat'],
                                      'total_fat_g': fruit_data[fruit_name]['total_fat_g'],
                                      'total_fat_dv': fruit_data[fruit_name]['total_fat_dv'],
                                      'sodium_mg': fruit_data[fruit_name]['sodium_mg'],
                                      'sodium_dv': fruit_data[fruit_name]['sodium_dv'],
                                      'potassium_g': fruit_data[fruit_name]['potassium_g'],
                                      'potassium_dv': fruit_data[fruit_name]['potassium_dv'],
                                      'total_carbohydrate_g': fruit_data[fruit_name]['total_carbohydrate_g'],
                                      'total_carbohydrate_dv': fruit_data[fruit_name]['total_carbohydrate_dv'],
                                      'dietary_fiber_g': fruit_data[fruit_name]['dietary_fiber_g'],
                                      'dietary_fiber_dv': fruit_data[fruit_name]['dietary_fiber_dv'],
                                      'sugars_g': fruit_data[fruit_name]['sugars_g'],
                                      'protein_g': fruit_data[fruit_name]['protein_g'],
                                      'vitamin_a_dv': fruit_data[fruit_name]['vitamin_a_dv'],
                                      'vitamin_c_dv': fruit_data[fruit_name]['vitamin_c_dv'],
                                      'calcium_dv': fruit_data[fruit_name]['calcium_dv'],
                                      'iron_dv': fruit_data[fruit_name]['iron_dv']}))

        for key in fruit_instances:
            fruit_instances[key].__acl__ = SITE_ACL
            session.add(fruit_instances[key])

        print
        print
        print 'len fruit category folders', len(DBSession.query(FruitCategoriesFolder).all())
        print 'len fruit categories', len(DBSession.query(FruitCategory).all())
        print 'len fruits', len(DBSession.query(Fruit).all())
        melons_category = DBSession.query(FruitCategory).filter_by(title=u"Melons").first()
        print 'melons_category parent', melons_category.__parent__
        grapefruit = DBSession.query(Fruit).filter_by(title='Grapefruit').first()
        print 'grapefruit id', grapefruit.id
        print 'grapefruit parent', grapefruit.__parent__
        print
        print

#    principals = get_principals()
#    if u'admin' not in principals:
#        principals[u'admin'] = {
#            u'name': u'admin',
#            u'password': get_settings()['kotti.secret'],
#            u'title': u"Administrator",
#            u'groups': [u'role:admin'],
#            }
#    if u'test' not in principals:
#        principals[u'test'] = {
#            u'name': u'test',
#           u'password': u'test',
#            u'title': u"Tester",
#            u'groups': [u'role:admin'],
#            }

    session.flush()
    transaction.commit()

    #import pdb; pdb.set_trace()
