from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='libacr',
      version=version,
      description="TurboGears2 Content Management Framework",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='tg2 cms cmf',
      author='AXANT',
      author_email='info@axant.it',
      url='http://labs.axant.it/acr',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data = {'':['*.html', '*.js', '*.css', '*.png', '*.gif']},
      zip_safe=False,
      install_requires=[
        "feedparser",
        "tw.jquery",
        "tw.tinymce",
        "BeautifulSoup",
        "PIL",
        "turbomail"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
