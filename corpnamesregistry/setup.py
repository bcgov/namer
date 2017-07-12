import os

from setuptools import setup, find_packages


def read(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    return open(file_path).read()

setup(
    name='corpnamesregistry',
    author='',
    author_email='',
    version='0.1',
    description="Corporate Names Registry",
    long_description=read('../README.md'),

    packages=find_packages(),
    package_dir={'corpnamesregistry': 'corpnamesregistry'},
    include_package_data=True,
    install_requires=[
        'flask',
        'pymongo',
        'pygtrie',
    ],
    setup_requires=[
    ],
    tests_require=[
        'pytest',
    ],
    license='Apache 2.0'
)
