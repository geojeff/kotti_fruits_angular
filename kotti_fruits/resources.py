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

    calories              = Column('calories',              Integer(), info='Calories')
    calories_from_fat     = Column('calories_from_fat',     Integer(), info='Calories from Fat')
    total_fat_g           = Column('total_fat_g',           Integer(), info='Total Fat (g)')
    total_fat_dv          = Column('total_fat_dv',          Integer(), info='Total Fat (%DV)')
    sodium_mg             = Column('sodium_mg',             Integer(), info='Sodium (mg)')
    sodium_dv             = Column('sodium_dv',             Integer(), info='Sodium (%DV)')
    potassium_g           = Column('potassium_g',           Integer(), info='Potassium (mg)')
    potassium_dv          = Column('potassium_dv',          Integer(), info='Potassium (%DV)')
    total_carbohydrate_g  = Column('total_carbohydrate_g',  Integer(), info='Total Carbohydrate (g)')
    total_carbohydrate_dv = Column('total_carbohydrate_dv', Integer(), info='Total Carbohydrate (%DV)')
    dietary_fiber_g       = Column('dietary_fiber_g',       Integer(), info='Dietary Fiber (g)')
    dietary_fiber_dv      = Column('dietary_fiber_dv',      Integer(), info='Dietary Fiber (%DV)')
    sugars_g              = Column('sugars_g',              Integer(), info='Sugars (g)')
    protein_g             = Column('protein_g',             Integer(), info='Protein (g)')
    vitamin_a_dv          = Column('vitamin_a_dv',          Integer(), info='Vitamin A (%DV)')
    vitamin_c_dv          = Column('vitamin_c_dv',          Integer(), info='Vitamin C (%DV)')
    calcium_dv            = Column('calcium_dv',            Integer(), info='Calcium (%DV)')
    iron_dv               = Column('iron_dv',               Integer(), info='Iron (%DV)')

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

    def __init__(self, **kwargs):
        super(Fruit, self).__init__()
        self.name                  = kwargs['title']
        self.title                 = kwargs['title']
        self.fruit_category_id     = kwargs['fruit_category_id']
        self.calories              = kwargs['calories']
        self.calories_from_fat     = kwargs['calories_from_fat']
        self.total_fat_g           = kwargs['total_fat_g']
        self.total_fat_dv          = kwargs['total_fat_dv']
        self.sodium_mg             = kwargs['sodium_mg']
        self.sodium_dv             = kwargs['sodium_dv']
        self.potassium_g           = kwargs['potassium_g']
        self.potassium_dv          = kwargs['potassium_dv']
        self.total_carbohydrate_g  = kwargs['total_carbohydrate_g']
        self.total_carbohydrate_dv = kwargs['total_carbohydrate_dv']
        self.dietary_fiber_g       = kwargs['dietary_fiber_g']
        self.dietary_fiber_dv      = kwargs['dietary_fiber_dv']
        self.sugars_g              = kwargs['sugars_g']
        self.protein_g             = kwargs['protein_g']
        self.vitamin_a_dv          = kwargs['vitamin_a_dv']
        self.vitamin_c_dv          = kwargs['vitamin_c_dv']
        self.calcium_dv            = kwargs['calcium_dv']
        self.iron_dv               = kwargs['iron_dv']

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

        #session.delete(root_document)

        from fixtures import fruit_categories, fruit_data, fruit_data_names

        fruit_categories_folder = \
                FruitCategoriesFolder(name=u"fruit_categories_folder",
                                      title=u"Fruit Categories",
                                      in_navigation=False,
                                      parent=root_document)

        fruit_categories_folder.__acl__ = SITE_ACL
        session.add(fruit_categories_folder)

        fruit_category_instances = {}
        for fruit_category in fruit_categories:
            fruit_category_instances[fruit_category] = \
                FruitCategory(name=fruit_categories[fruit_category]['name'],
                              title=fruit_categories[fruit_category]['name'],
                              parent=fruit_categories_folder)

        for key in fruit_category_instances:
            fruit_category_instances[key].__acl__ = SITE_ACL
            session.add(fruit_category_instances[key])

        # Find the fruit_categories
        fruit_category_results = DBSession.query(FruitCategory).all()

        fruit_instances = {}
        for fruit_category in fruit_categories:
            fruit_category_obj = \
                    DBSession.query(FruitCategory).filter_by(name=fruit_category).first()
            for fruit_name in fruit_categories[fruit_category]['fruits']:
                fruit_instances[fruit_name] = \
                        Fruit(**dict({'fruit_category_id': fruit_category_obj.id,
                                      'title': fruit_name},
                                      **dict(fruit_data[fruit_name])))

        for key in fruit_instances:
            fruit_instances[key].__acl__ = SITE_ACL
            session.add(fruit_instances[key])

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
