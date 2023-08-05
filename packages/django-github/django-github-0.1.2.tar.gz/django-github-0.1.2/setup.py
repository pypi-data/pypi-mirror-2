import os
from setuptools import setup, find_packages

from github import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-github',
    version=".".join(map(str, VERSION)),
    description='simple django integration with github\'s v2 api',
    long_description=readme,
    author='Charles Leifer',
    author_email='coleifer@gmail.com',
    url='http://github.com/coleifer/django-github/tree/master',
    packages=find_packages(exclude=['example']),
    package_data = {
        'github': [
            'fixtures/*.json',
            'templates/*.html',
            'templates/*/*.html',
        ],
    },
    install_requires = ['httplib2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
