# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

version = '1.0a1'
readme = open(join('src', 'dolmen', 'widget', 'tinymce', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'grokcore.view',
    'hurry.jquery',
    'hurry.tinymce',
    'hurry.zopetinymce',
    'megrok.resource',
    'setuptools',
    'zeam.form.base',
    'zeam.form.ztk',
    'zope.interface',
    ],

tests_require = [
    'grokcore.component',
    'zeam.form.ztk [test]',
    'zope.browserpage',
    'zope.browserresource',
    'zope.component',
    'zope.interface',
    'zope.publisher',
    'zope.schema',
    'zope.security',
    ]

setup(name='dolmen.widget.tinymce',
      version=version,
      description="A rich text widget using TinyMCE for Dolmen",
      long_description = readme + '\n\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org/',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.widget'],
      include_package_data=True,
      zip_safe=False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
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
