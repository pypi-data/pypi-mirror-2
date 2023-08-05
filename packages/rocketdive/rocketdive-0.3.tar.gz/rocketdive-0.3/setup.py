try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import distutils.cmd
import re
import doctest
try:
    import py2exe
except ImportError:
    pass
import rocketdive


PY2EXE_OPTIONS = {"packages": ["rocket"]}
PY2APP_OPTIONS = {"argv_emulation": True, "packages": "rocket"}


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
      setup_requires=["py2exe", "py2app"],
      app=["rocketdive.py"],
      windows=["rocketdive.py"],
      data_files=[],
      options={"py2exe": PY2EXE_OPTIONS, "py2app": PY2APP_OPTIONS},
      license=rocketdive.__license__)

