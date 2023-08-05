import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-viewtester",
    version = "10.4.3",
    url = 'http://bitbucket.org/pterk/django-viewtester/',
    license = 'BSD',

    description = "A django views-tester",
    long_description = read('README.rst'),

    author = 'Peter van Kampen',
    author_email = 'pterk@datatailors.com',

    
    packages = find_packages(),
    package_data = {'viewtester': [
        'templates/viewtester/*',
        ]
    },

    include_package_data=True,

    zip_safe = False,

    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
