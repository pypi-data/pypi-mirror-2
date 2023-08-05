from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.viewselector'
version = '0.2.1'
readme = open(join('src', 'dolmen', 'app', 'viewselector', "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = 'Dolmen Layout/View Selector',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'souheil@chelfouh.com',
      url = 'http://tracker.trollfot.org/',
      download_url = 'http://pypi.python.org/pypi/dolmen.app.viewselector',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires=[
          'dolmen.app.layout',
          'grokcore.component',
          'grokcore.message',
          'grokcore.view',
          'grokcore.viewlet',
          'megrok.layout',
          'megrok.menu',
          'setuptools',
          'zope.component',
          'zope.interface',
          'zope.schema',
      ],
      extras_require = {'test': [
          'zope.container',
          'zope.i18n',
          'zope.location',
          'zope.principalregistry',
          'zope.publisher',
          'zope.security',
          'zope.securitypolicy',
          'zope.site',
          'zope.testing',
          'zope.traversing',
          ]},
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
