"""Packaging logic for appcommander."""
from __future__ import annotations

import os
import sys

import setuptools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
setuptools.setup(
    install_requires=[
        # Lists the pip packages used by the src code of this project. Doesn
        # not include pre-commit packages.
        # Parse xml files into Python dictionaries.
        "xmltodict",
        # Plot the script flow to png.
        "matplotlib",
        # Plot the script flow as a graph, to png.
        "networkx",
        # Allow for auto generation of type-hints during runtime.
        "pyannotate",
        # Run python tests.
        "pytest-cov",
        # Ensure the python function arguments are verified at runtime.
        "typeguard",
        # Control Android apps through their user interface (UI).
        "uiautomator",
        # Some dependencies of dependencies, for service-identity 21.1.0.
        "pyasn1",
        "pyasn1-modules",
        "pyOpenSSL",
    ]
    # install_requires=['numpy','pandas'],
    # setup_requires=['pytest-runner'],
    # tests_require=['wandb','pytest==4.4.1'],
    # test_suite='tests',
)
