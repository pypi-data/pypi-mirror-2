import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a
# top level
# README file and 2) it's easier to type in the README file than to put
# a raw
# string in below ...
def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "testr_recipe",
    version = '0.2',
    packages = find_packages(),
    entry_points = {
        'zc.buildout': [
            'testr = testr_recipe:Testr',
            'default = testr_recipe:Testr',
            ]
        },
    install_requires = [
        'setuptools',
        'zc.recipe.egg',
        'testrepository',
        ],
    package_data = {
        '': ['README.txt'],
        },
    author = "James Westby",
    author_email = "james.westby@linaro.org",
    license = "ZPL",
    keywords = "testing testrepository testr buildout recipe",
    url = "https://launchpad.net/testr_recipe",
    description = "buildout recipe to create scripts to run testrepository.",
    long_description = read("README.txt"),
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Plugins",
            "Framework :: Buildout",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Zope Public License",
            "Programming Language :: Python",
            "Topic :: Software Development :: Testing",
        ],
)
