from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='shift2calendar',
      version=version,
      description="Synchronize Tieto Corporation employee Shifts to the (Google) Calendar",
      long_description="""\
Synchronize Tieto Corporation employee Shifts to the (Google) Calendar""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Shift Tieto Google Calendar',
      author='Lumir Jasiok',
      author_email='lumir.jasiok@alfawolf.eu',
      url='https://github.com/jas02/shift2calendar',
      license='GPL',
      packages=find_packages('src'),
      include_package_data=True,
      package_dir = {'': 'src'},
      package_data = {
          '': ['*.conf'],
      },
      zip_safe=False,
      install_requires=['configobj', 'gdata'],
      entry_points={'console_scripts': [
                        'shift2calendar = \
                        shift2calendar.shift2calendar:main']
          },
      )

