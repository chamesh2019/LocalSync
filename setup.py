#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from pyproject.toml dependencies
dependencies = [
    "fastapi>=0.118.0",
    "netifaces>=0.11.0", 
    "requests>=2.32.5",
    "tabulate>=0.9.0",
    "uvicorn>=0.37.0",
    "watchdog>=6.0.0",
    "zeroconf>=0.148.0",
]

setup(
    name="localsync",
    version="0.1.0",
    author="Chamesh",
    author_email="chamesh2019@github.com",
    description="Local package synchronization and sharing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chamesh2019/LocalSync",
    project_urls={
        "Bug Tracker": "https://github.com/chamesh2019/LocalSync/issues",
        "Source Code": "https://github.com/chamesh2019/LocalSync",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=dependencies,
    entry_points={
        "console_scripts": [
            "localsync=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)