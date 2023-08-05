import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='ice.control',
      version='0.4.0',
      author='Ilshad R. Khabibullin',
      author_email='astoon.net at gmail.com',
      url='http://launchpad.net/ice.control',
      description='System Administration and Site Management for BlueBream',
      long_description = (read('src/ice/control/doc/README.rst')) +\
          '\n\n' + read('src/ice/control/doc/CHANGES.rst'),
      license='GPL v.3',
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Framework :: ZODB',
        'Framework :: Zope3'],
      packages=find_packages('src'),
      namespace_packages=['ice',],
      package_dir={'':'src'},
      install_requires=['setuptools',

                        'zope.testbrowser',
                        'zope.viewlet',

                        'zope.app.testing',
                        'zope.app.zcmlfiles',
                        'zope.app.apidoc',

                        'zc.resourcelibrary',

                        'z3c.testsetup',
                        'z3c.configurator',
                        'z3c.layer.pagelet',
                        'z3c.template',
                        'z3c.formui',
                        'z3c.zrtresource',
                        'z3c.contents'],
      include_package_data=True,
      zip_safe=False)
