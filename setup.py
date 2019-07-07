import re
import os.path
from setuptools import setup


def readfile(fls: list):
    with open(os.path.join(os.path.dirname(__file__), *fls), 'rt', encoding='utf-8') as fh:
        return fh.read()


_version = re.search('__version__ = [\'"](.+)[\'"]', readfile(['jsonextra', '__init__.py'])).groups()[0]


install_requires = [
    dep for dep in readfile(['requirements.txt']).splitlines()
    if not dep.startswith('#')
]


setup(
    name='jsonextra',
    version=_version,
    description='JSON Extra | JSON that gives you extra datetime, uuid and bytes data types',
    author='Denis Sazonov',
    author_email='den@saz.lt',
    packages=['jsonextra'],
    license='MIT License',
    keywords="json uuid datetime date bytes".split(),
    install_requires=install_requires,
    include_package_data=True,
    long_description=readfile(['README.md']),
    long_description_content_type="text/markdown",
    url="https://github.com/den4uk/jsonextra",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    zip_safe=True,
)
