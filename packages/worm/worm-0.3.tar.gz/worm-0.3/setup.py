from distutils.core import setup
from os import path

long_desc = open(path.join(path.dirname(__file__), "README.rst")).read()

from worm import __version__

setup(name="worm", version=__version__,
      url="http://mechanicalcat.net/richard/",
      author="Richard Jones",
      author_email="richard@mechanicalcat.net",
      description="Animating worms for progress bars",
      long_description=long_desc,
      data_files=['README.rst'],
      py_modules=["worm"])
