from distutils.core import setup

setup(name='Firmant',
        version='0.1.1',
        description='Static Blog Generator',
        author='Robert Escriva',
        author_email='projects@mail.robescriva.com',
        url='http://projects.robescriva.com/projects/show/firmant',
        packages=['firmant', 'firmant.parsers', 'firmant.routing',
            'firmant.utils', 'firmant.writers'],
        )
