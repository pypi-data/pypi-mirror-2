from distutils.core import setup

setup(name='twittercollect',
      version='0.1.0',
      author='Robert Escriva, Rensselaer Polytechnic Institute',
      author_email='escrir@cs.rpi.edu',
      packages=['twittercollect'
               ],
      scripts=['bin/twittercollect'],
      license='3-clause BSD',
      description='A utility for consuming Twitter\'s stream API.',
      long_description=open('doc/README.rst').read(),
      )
