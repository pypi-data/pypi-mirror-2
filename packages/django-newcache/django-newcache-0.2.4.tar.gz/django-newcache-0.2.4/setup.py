import os

from setuptools import setup

VERSION = '0.2.4'

setup(
    name='django-newcache',
    version=VERSION,
    description='Improved memcached cache backend for Django',
    long_description=file(
        os.path.join(os.path.dirname(__file__), 'README.txt')
    ).read(),
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    license='BSD',
    url='http://github.com/ericflo/django-newcache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Environment :: Web Environment',
    ],
    zip_safe=False,
    py_modules=['newcache'],
)