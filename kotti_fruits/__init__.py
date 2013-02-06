from pyramid.events import subscriber
from pyramid.events import ApplicationCreated

from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_fruits')

from resources import populate

from views import includeme as fruits_includeme


@subscriber(ApplicationCreated)
def call_populate(event):
    populate()


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_fruits'
    settings['kotti.available_types'] += ' kotti_fruits.resources.FruitCategoriesFolder kotti_fruits.resources.FruitCategory kotti_fruits.resources.Fruit'

def automore(request, elements, kw):
    # this is for adding the more kwargs for backbone urls (from sontek's datanommer_web)
    kw.setdefault('more', ())
    return elements, kw

def include_populator(config):
    config.add_subscriber(call_populate)

def includeme(config):

    config.add_translation_dirs('kotti_fruits:locale')
    config.scan(__name__)

    config.add_route('index', '/*more', pregenerator=automore)

    fruits_includeme(config)
