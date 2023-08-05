from setuptools import setup, find_packages
import sys, os

version = '0.1.0'
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs/HISTORY.txt')
    + '\n' )


setup(name='zopyx.smartprintng.psd',
      version=version,
      description="PSD -> PrinceXML converter",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/zopyx.smartprintng.psd',
      license='GPL 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['zopyx', 'zopyx.smartprintng'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml',
      ],
      entry_points=dict(console_scripts=(
          'psd2prince=zopyx.smartprintng.psd.psd:main',
      )),
      )
