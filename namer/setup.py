import os

from setuptools import setup, find_packages


def read(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    return open(file_path).read()

setup(
    name='namer',
    author='',
    author_email='',
    version='0.1',
    description="Namer",
    long_description=read('../README.md'),

    packages=find_packages(),
    package_dir={'namer': 'namer'},
    include_package_data=True,
    install_requires=[
        'flask',
        'pymongo',
        'pytrie',
    ],
    setup_requires=[
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pep8',
        'pylint',
    ],
    license='Apache 2.0'
)
