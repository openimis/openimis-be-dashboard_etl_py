import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='openimis-be-dashboard_etl',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='GNU AGPL v3',
    description='The openIMIS Backend module to extract data from production and push to another database designed for Business Intelligence tool',
    # long_description=README,
    url='https://openimis.org/',
    author='Hiren Soni',
    author_email='hiren.soni@swisstph.ch',
    install_requires=[
        'django',
        'python-dateutil==2.8.2',
        'django-redis',
        'sqlalchemy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)
