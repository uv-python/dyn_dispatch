# build with: python3 setup.py bdist_wheel
from setuptools import setup  # , find_packages

VERSION = "0.4.2"
DESCRIPTION = "Multiple dispatch"
with open("README.markdown", "r") as f:
    global LONG_DESCRIPTION
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="dyn_dispatch",
    version="0.4.2",
    author="Ugo Varetto",
    author_email="ugovaretto@gmail.com>",
    description="Multiple dispatch",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/uv-python/dyn_dispatch",
    package_data={"dyn_dispatch": ["py.typed",
                                   "dyn_dispatch.pyi", "__init__.pyi",
                                   "doc_site"]},
    # packages=find_packages(),
    install_requires=[],
    license="BSD-3-Clause",
    keywords=["python", "multiple dispatch", "multimethods"],
)
