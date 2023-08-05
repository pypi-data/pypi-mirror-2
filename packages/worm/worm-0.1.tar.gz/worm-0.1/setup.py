from distutils.core import setup
from os import path

long_desc = path.join(path.dirname(__file__), "README.rst")

setup(name="worm", version="0.1",
      url="http://mechanicalcat.net/",
      author="Richard Jones",
      author_email="richard@mechanicalcat.net",
      description="Animating worms for progress bars",
      long_description=long_desc,
      py_modules=["worm"])
