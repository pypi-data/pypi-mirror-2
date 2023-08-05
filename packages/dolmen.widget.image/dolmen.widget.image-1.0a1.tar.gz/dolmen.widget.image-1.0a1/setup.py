from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.widget.image'
version = '1.0a1'
readme = open(join('src', 'dolmen', 'widget', 'image', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.file >= 0.5.1',
    'dolmen.thumbnailer',
    'dolmen.widget.file >= 1.0a1',
    'grokcore.component',
    'grokcore.view',
    'setuptools',
    'zeam.form.base',
    'zeam.form.ztk',
    'zope.interface',
    ]

tests_require = [
    'zope.app.testing',
    'zope.component',
    'zope.container',
    'zope.i18n',
    'zope.publisher',
    'zope.schema',
    'zope.security',
    'zope.site',
    'zope.testing',
    'zope.traversing',
    ]

setup(name=name,
      version=version,
      description='Image widget (with thumbnails) for `zeam.form`',
      long_description=readme + '\n\n' + history,
      keywords='Grok Zeam Zope3 Dolmen Widget Image',
      author='Souheil Chelfouh',
      author_email='trollfot@gmail.com',
      url='',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.widget'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      test_suite="dolmen.widget.image",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
