from setuptools import setup, find_packages

setup(name="gaphormodelimport",\
      version='0.0.1',\
      install_requires = ['gaphor'],\
      zip_safe=False,\
      packages = find_packages('src'),\
      package_dir = {'':'src'},\
      entry_points = {"gaphor.services":".gaphor_model_import = gaphormodelimport:GaphorModelImport"},\
      author = "Adam Boduch",\
      author_email = "adam.boduch@gmail.com",\
      license = "AGPL",\
      url = "http://www.boduch.ca/")
