# -*- encoding: utf8 *-*
from distutils2.core import setup

DESCRIPTION = """\
pep345demo
==========

Demonstrates PEP 345 features at PyPI.

The requirements where randomly picked juste to demonstrate.

"""

setup(name='pep345demo',
      version='1.0',
      author=u'Tarek Ziadé',
      author_email='tarek@ziade.org',
      home_page='http://bitbucket.org/tarek/pep345demo',
      keywords=['distutils', 'packaging'],
      summary='Demonstrates PEP 345',
      description=DESCRIPTION,
      requires_dist=['pip', 'bottle'],
      project_url=
      [("HitchHicker's Guide", 'http://guide.python-distribute.org'),
       ('Distutils', 'http://docs.python.org/distutils'),
       ('Distutils2', 'http://hg.python.org/distutils2')
        ]
      )

