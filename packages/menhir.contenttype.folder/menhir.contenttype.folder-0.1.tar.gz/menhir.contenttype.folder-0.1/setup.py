from setuptools import setup, find_packages
from os.path import join

name = 'menhir.contenttype.folder'
version = '0.1'
readme = open(join('src', 'menhir', 'contenttype', 'folder', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

tests_require = [
    'zope.component',
    'zope.publisher',
    'dolmen.app.security',
    'zope.securitypolicy',
    'zope.site',
    'grokcore.content',
    'zope.container',
    'zope.security',
    ]

setup(name = name,
      version = version,
      description = 'Dolmen contenttype extension : folder',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'souheil@chelfouh.com',
      url = 'http://tracker.trollfot.org/',
      download_url = 'http://pypi.python.org/pypi/menhir.contenttype.folder',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['menhir', 'menhir.contenttype'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      install_requires=[
          'dolmen.app.container',
          'dolmen.app.content',
          'dolmen.app.layout',
          'dolmen.app.viewselector',
          'dolmen.content',
          'dolmen.menu',
          'grok',
          'grokcore.view',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
      ],
      classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
