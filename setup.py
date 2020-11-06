#!/usr/bin/env python3

import sys
from setuptools import find_packages, setup  # type: ignore

if sys.version_info < (3, 6, 0):
    sys.exit("Python 3.6 or later is required. ")

from pathlib import Path  # noqa E402
from runpy import run_path  # noqa E402
from typing import List  # noqa E402
import ast  # noqa E402
import re  # noqa E402

CURDIR = Path(__file__).parent


setup(
    name="importation",
    version="0.0.1",
    author="Chad Smith",
    author_email="grassfedcode@gmail.com",
    description="automagically install imports",
    long_description=CURDIR.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/cs01/importation",
    license="License :: OSI Approved :: MIT License",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    keywords=[
        "import",
        "importation",
        "magic",
        "cli",
        "PEP-582",
        "Virtual Environment",
    ],
    zip_safe=False,
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Documentation": "https://github.com/cs01/importation",
        "Source Code": "https://github.com/cs01/importation",
        "Bug Tracker": "https://github.com/cs01/importation/issues",
    },
)
