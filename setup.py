import os.path
from setuptools import setup, find_packages
from jsonextra import __version__

req = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(req, 'rt', encoding="utf-8") as f:
    install_requires = [dep for dep in f.read().splitlines() if not dep.startswith('#')]


setup(name='jsonextra',
      version=__version__,
      description='JSON Extra | JSON that gives you extra',
      author='Denis Sazonov',
      author_email='den@saz.lt',
      packages=find_packages(),
      license='Restricted',
      install_requires=install_requires,
      include_package_data=True,
      python_requires=">=3.5",
      zip_safe=True)
