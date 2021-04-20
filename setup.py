from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=1", "requests>=2", "lxml>=4"]

setup(
    name = "twofourseven",
    version = "0.0.5",
    author = "Nathan Reeb",
    author_email = "Nathan.Reeb94@outlook.com",
    description = "Package to scrape 247Sports website for recruiting data",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Natron0919/twofourseven/",
    packages = find_packages(),
    install_requires = requirements,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)