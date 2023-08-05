try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import re
import doctest
import rocketdive


setup(name="rocketdive",
      description="Easy GUI frontend for Rocket, a modern WSGI web server.",
      long_description=rocketdive.__doc__,
      version=rocketdive.__version__,
      author=rocketdive.__author__,
      author_email=rocketdive.__email__,
      maintainer=rocketdive.__author__,
      maintainer_email=rocketdive.__email__,
      url="http://bitbucket.org/dahlia/rocketdive",
      py_modules=["rocketdive"],
      install_requires=["rocket"],
      license=rocketdive.__license__)

