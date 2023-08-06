
# Use bdist_esky instead of py2exe
from esky import bdist_esky
from distutils.core import setup

setup(
  name = "example-app",
  version = "0.1",
  #  All executables are listed in the "scripts" argument
  scripts = ["example.py"],
  options = {"bdist_esky": {"compile_bootstrap_exes": True}},
)

