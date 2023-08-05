from setuptools import setup, find_packages
import sys, os

version = '0.0'
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-render-load',
      version=version,
      description="Django template tags render_object and load_object grouped together.",
      long_description=read('README'),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django template',
      author='Alexander Pugachev',
      author_email='alexander.pugachev@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
