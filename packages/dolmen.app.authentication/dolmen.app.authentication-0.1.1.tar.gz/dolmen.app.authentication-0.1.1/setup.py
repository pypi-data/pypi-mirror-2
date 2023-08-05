from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.authentication'
version = '0.1.1'
readme = open(
    join('src', 'dolmen', 'app', 'authentication', 'README.txt')).read()
history = open(
    join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

install_requires=[
    'dolmen.app.layout',
    'dolmen.app.security',
    'dolmen.app.site',
    'dolmen.authentication >= 0.2',
    'dolmen.content',
    'dolmen.forms.base',
    'grok',
    'grokcore.component',
    'grokcore.view',
    'megrok.menu',
    'setuptools',
    'z3c.schema',
    'zope.authentication',
    'zope.component',
    'zope.container',
    'zope.event',
    'zope.formlib',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.location',
    'zope.pluggableauth',
    'zope.principalregistry',
    'zope.publisher',
    'zope.schema',
    'zope.security',
    'zope.securitypolicy',
    'zope.site',
    'zope.traversing',
    ]

test_requires = [
    'megrok.z3cform.base',
    'megrok.z3cform.layout',
    'zope.app.appsetup',
    'zope.app.publication',
    'zope.app.wsgi',
    'zope.browserpage',
    'zope.i18n',
    'zope.testing',
    ]

setup(name = name,
      version = version,
      description = 'Dolmen CMS authentication package',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'souheil@chelfouh.com',
      url = 'http://tracker.trollfot.org/',
      download_url = 'http://pypi.python.org/pypi/dolmen.app.authentication',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      extras_require={'test': test_requires},
      install_requires=install_requires,
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
