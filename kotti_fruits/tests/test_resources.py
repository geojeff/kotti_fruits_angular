from kotti.resources import get_root
from kotti.testing import DummyRequest

from kotti_fruits.resources import FruitCategoriesFolder
from kotti_fruits.resources import FruitCategory
from kotti_fruits.resources import Fruit


def test_fruit_categories_folder(db_session):

    root = get_root()
    content = FruitCategoriesFolder()
    assert content.type_info.addable(root, DummyRequest()) is True
    root['content'] = content

def test_fruit_category(db_session):

    root = get_root()
    content = FruitCategory()
    assert content.type_info.addable(root, DummyRequest()) is True
    root['content'] = content

def test_fruit(db_session):

    root = get_root()
    content = Fruit()
    assert content.type_info.addable(root, DummyRequest()) is True
    root['content'] = content
