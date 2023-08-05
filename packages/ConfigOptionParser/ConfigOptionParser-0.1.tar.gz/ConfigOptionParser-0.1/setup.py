from setuptools import setup, find_packages

version = '0.1'

setup(name='ConfigOptionParser',
      version=version,
      description="a version of OptionParser that allows parsing from .ini files",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ini cli',
      author='Jeff Hammel',
      author_email='jhammel@mozilla.com',
      url='http://k0s.org',
      license='MPL',
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
