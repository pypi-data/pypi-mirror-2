from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='DjangoPluggableApp',
      version=version,
      description="A pluggable system for django applications",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django plugin apps',
      author='Gael Pasgrimaud',
      author_email='gpasgrimaud@bearstech.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'PasteScript',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      django-pluggableapp = pluggableapp.scripts:main

      [paste.paster_create_template]
      django_app = pluggableapp.template:DjangoAppTemplate

      [django.pluggable_app]
      admin = pluggableapp.apps:admin
      admin_docs = pluggableapp.apps:admin_docs
      pluggable_registration = pluggableapp.apps:registration
      pluggable_pagination = pluggableapp.apps:pagination
      pluggable_reversion= pluggableapp.apps:reversion
      pluggable_messages = pluggableapp.apps:messages
      pluggable_attachments = pluggableapp.apps:attachments
      """,
      )
