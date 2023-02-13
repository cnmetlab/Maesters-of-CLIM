import os
from setuptools import find_packages, setup

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(FILE_PATH, "README.md"), "r") as f:
    description = f.read()

with open(os.path.join(FILE_PATH, "requirements.txt")) as f:
    required = f.read().splitlines()

setup(
    name="maesters-clim",
    version="0.0.3",
    author="blizhan",
    author_email="blizhan@icloud.com",
    description="Maesters-of-Clim tempt to help retriving climate data (climate index, reanalysis) from the main-stream climate insitution (like IRI, PSL, NCEI, RDA).",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/blizhan/maesters-of-clim",
    package_dir={"maesters-of-clim": "maesters-of-clim", ".": "./"},
    package_data={
        "": ["*.toml", "*.txt"],
    },
    include_package_data=True,
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
