from setuptools import setup, find_packages

setup(
    name='corpnamesregistry',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=0.12.2',
    ],
    setup_requires=[
    ],
    tests_require=[
        'pytest>=3.1.3',
    ],
)
