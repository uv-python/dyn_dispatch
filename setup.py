# build with: python3 setup.py bdist_wheel
from setuptools import setup, find_packages

VERSION = "0.4.1"
DESCRIPTION = "Multiple dispatch"
with open("README.markdown", "r") as f:
    global LONG_DESCRIPTION
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="dyn-dispatch",
    version="0.4.1",
    author="Ugo Varetto",
    author_email="ugovaretto@gmail.com>",
    description="Multiple dispatch",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/uv-python/dyn_dispatch",
    package_data={"dyn-dispatch": ["py.typed", "dd.pyi", "__init__.pyi"]},
    packages=find_packages(),
    install_requires=[],
    license="BSD-3-Clause",
    keywords=["python", "multiple dispatch", "multimethods"],
)
