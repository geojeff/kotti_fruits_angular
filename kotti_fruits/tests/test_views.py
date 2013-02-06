from kotti.resources import get_root

from kotti_fruits.resources import FruitCategoriesFolder
from kotti_fruits.views import FruitCategoriesFolderView


def test_views(db_session, dummy_request):

    root = get_root()
    content = FruitCategoriesFolder()
    root['content'] = content

    view = FruitCategoriesFolderView(root['content'], dummy_request)

    assert view.view() == {}
    assert view.alternative_view() == {}
