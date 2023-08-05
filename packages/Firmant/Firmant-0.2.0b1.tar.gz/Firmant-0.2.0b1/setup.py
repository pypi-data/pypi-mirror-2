from distutils.core import setup

setup(name='Firmant',
      version='0.2.0b1',
      author='Robert Escriva (rescrv)',
      author_email='firmant@mail.robescriva.com',
      packages=['firmant'
               ,'firmant.parsers'
               ,'firmant.routing'
               ,'firmant.templates'
               ,'firmant.utils'
               ,'firmant.writers'
               ],
      package_dir={'firmant': 'firmant'},
      package_data={'firmant': ['templates/*.html',
                                'templates/*/*.html']},
      scripts=['bin/firmant'],
      url='http://firmant.org/',
      license='LICENSE',
      description='A framework for developing static web applications.',
      long_description=open('doc/README.rst').read(),
      )
