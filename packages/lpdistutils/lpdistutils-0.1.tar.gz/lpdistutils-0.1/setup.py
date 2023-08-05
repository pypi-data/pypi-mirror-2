import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="lpdistutils",
    version="0.1",
    packages=find_packages(),
    install_requires=['launchpadlib', 'bzr'],
    tests_require=['mocker', 'testtools'],
    description="Distutils commands for working with Launchpad and Bazaar.",
    long_description=read("README.txt"),
    url="https://launchpad.net/lpdistutils",
    author="James Westby",
    author_email="james.westby@linaro.org",
    license="GPL2+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Framework :: Setuptools Plugin",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Version Control",
        ],
    )
