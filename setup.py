import os.path
from setuptools import setup
from jsonextra import __version__

req = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(req, 'rt', encoding='utf-8') as f:
    install_requires = [dep for dep in f.read().splitlines() if not dep.startswith('#')]


reme = os.path.join(os.path.dirname(__file__), 'README.md')
with open(reme, 'rt', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='jsonextra',
    version=__version__,
    description='JSON Extra | JSON that gives you extra datetime and uuid data types',
    author='Denis Sazonov',
    author_email='den@saz.lt',
    packages=['jsonextra'],
    license='MIT License',
    keywords="json uuid datetime date".split(),
    install_requires=install_requires,
    include_package_data=True,
    long_description=long_description,
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
