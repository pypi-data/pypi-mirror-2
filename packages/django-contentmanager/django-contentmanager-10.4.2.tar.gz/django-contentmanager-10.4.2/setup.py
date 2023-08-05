import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-contentmanager',
    version='10.4.2',
    url='http://bitbucket.org/pterk/django-contentmanager/',

    description='A simple, pluggable content-manager for django.',
    long_description = read('README'),

    license = 'BSD',

    author='Peter van Kampen',
    author_email='pterk@datatailors.com',

    install_requires = [
        'setuptools',
        'django-haystack',
        'Whoosh',
        ],

    packages=find_packages(),

    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
