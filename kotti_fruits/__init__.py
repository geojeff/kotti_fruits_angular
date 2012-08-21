from pyramid.events import subscriber
from pyramid.events import ApplicationCreated

from resources import populate


@subscriber(ApplicationCreated)
def call_populate(event):
    populate()


def kotti_configure(config):
    config['kotti.includes'] += ' kotti_fruits.views'
    config['kotti.available_types'] += ' kotti.resources.Document kotti_fruits.resources.FruitCategoriesFolder kotti_fruits.resources.FruitCategory kotti_fruits.resources.Fruit'


def include_populator(config):
    config.add_subscriber(call_populate)
