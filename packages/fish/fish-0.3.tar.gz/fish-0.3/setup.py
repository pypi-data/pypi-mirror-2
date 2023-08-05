from distutils.core import setup
from os import path

long_desc = path.join(path.dirname(__file__), "README.rst")

setup(name="fish", version="0.3",
      url="http://sendapatch.se/",
      author="Ludvig Ericson",
      author_email="ludvig@sendapatch.se",
      description="Animating fishes for progress bars",
      long_description=long_desc,
      py_modules=["fish"])
