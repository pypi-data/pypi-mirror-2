import os
from setuptools import setup, find_packages

def read(*filenames):
    return open(os.path.join(os.path.dirname(__file__), *filenames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(name='serf',
      version='0.3.1',
      description="A web server to prototype rich client-side web apps",
      long_description=long_description,
      keywords="wsgi javascript hurry.resource",
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   ],
      license="BSD",
      packages=['serf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'martian',
        'hurry.resource >= 0.10',
        'WebOb'],
      entry_points={
        'console_scripts': [
            'serf = serf.main:main',
            ]
        },
      )
