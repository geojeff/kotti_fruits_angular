kotti_fruits_angular
====================

This is a modification of kotti_fruits_example to use angular.js.

Do::

    pip install js.angular

README from kotti_fruits_example:

An example Kotti project using a dataset about fruits, containing images from
Wikipedia.

When run in a virtualenv with pserve development.ini, the populate() method in
resources.py will first call the Kotti default populate(), which adds a root
Document instance and an About Document. Then the kotti_fruits populate() code
adds a FruitCategoriesFolder, and within that FruitCategory instances, and
within each of those, Fruit instances. Each Fruit instance has a set of images
loaded also.

When you visit the new Kotti site, log in as admin/querty, then click Navigate
to see the content added to the site. Click the main FruitCategoriesFolder,
then a fruit category, such as 'Melons' then click individual fruits to see
an image and some data for that fruit.

Basic REST services are up. Visit /fruit_categories to see JSON data for all
the categories, and /fruits for all fruits. Visit /fruit_category/5 through
7 for the four fruit categories JSON data, and for the individual fruits it is
/fruit/8 through 27.
