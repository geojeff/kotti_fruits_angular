import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='kotti_fruits_example',
      version='0.1',
      description="Kotti Fruits Example",
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSS under BSD license",
        ],
      author='Jeff Pittman',
      author_email='geojeff@me.com',
      url='http://kotti.pylonsproject.org',
      keywords='examples kotti cms pylons pyramid',
      license="BSD",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['Kotti'],
      tests_require=['nose', 'coverage'],
      )
