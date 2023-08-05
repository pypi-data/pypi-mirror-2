import os, sys
from setuptools import setup, find_packages

def read_file(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except:
        return ''

setup(
    name = "django-alphafilter",
    version = __import__('alphafilter').get_version().replace(' ', '-'),
    url = '',
    author = 'coordt',
    author_email = '',
    description = '',
    long_description = read_file('README'),
    packages = find_packages(),
    license = 'Apache 2.0',
    include_package_data = True,
    install_requires=read_file('requirements.txt'),
    classifiers = [
    ],
)
