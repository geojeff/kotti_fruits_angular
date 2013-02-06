from pyramid.interfaces import ITranslationDirectories

from kotti_fruits import includeme
from kotti_fruits import kotti_configure


def test_kotti_configure():

    settings = {
        'kotti.available_types': '',
        'pyramid.includes': '',
    }

    kotti_configure(settings)

    assert settings['pyramid.includes'] == ' kotti_fruits'
    assert settings['kotti.available_types'] == ' kotti_fruits.resources.FruitCategoriesFolder kotti_fruits.FruitCategory kotti_fruits.Fruit'


def test_includeme(config):

    includeme(config)

    utils = config.registry.__dict__['_utility_registrations']
    k = (ITranslationDirectories, u'')

    # test if the translation dir is registered
    assert k in utils
    assert utils[k][0][0].find('kotti_fruits/locale') > 0
