from setuptools import setup, find_packages

version = '0.0'

setup(name='testish',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'restish',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      main = testish.wsgiapp:make_app
      """,
      )
