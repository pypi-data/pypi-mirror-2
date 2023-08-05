from os.path import abspath, dirname, join as pjoin
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

fn = abspath(pjoin(dirname(__file__), 'README.rst'))
fp = open(fn, 'r')
long_description = fp.read()
fp.close()

setup(
    name='aino-mutations',
    version='0.1.0.0',
    url='http://bitbucket.org/aino/aino-mutations/',
    license='BSD',
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    description='Mutating for evolution using Django and Mercurial',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Version Control',
        'Framework :: Django',
    ],
    packages=[
        'mutations',
        'mutations.conf',
        'mutations.management',
        'mutations.management.commands',
    ],
    zip_safe=False,
    platforms='any',
)
