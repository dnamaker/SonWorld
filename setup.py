#!/usr/bin/env python3

# import os
from setuptools import setup, find_packages
from sonworld.version import __version__
from pathlib import Path

this_directory = Path(__file__).parent
long_description = """
### SONWORLD

"""


required = [
    'chromadb==0.4.20',
    'SQLAlchemy==2.0.23',
    'arrow==1.3.0',
    'fastapi==0.108.0',
    'pydantic==2.5.3',
    'uvicorn==0.25.0',
    'pyjwt==2.8.0',
    'aiofiles==23.2.1',
    'psutil==5.9.7',
    'python-rapidjson==1.14',
    'orjson==3.9.10',
    'sdnotify==0.3.2',
    'cachetools==5.3.2',
    'schedule==1.2.1',
    'gymnasium==0.29.1',
    'pettingzoo==1.24.3',
    'pytest==8.1.1'
    
]

# print(f"Required: {required}")
# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name="sonworld",
    description=(
        "MMO Game with Reinforcement Learning Agent."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    author="DNA MAKER",
    author_email="sonnhfit@gmail.com",
    url="https://github.com/dnamaker/sonworld",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9.0",
    install_requires=required,
    license="MIT",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "sonworld = sonworld.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="game mmo, rl, reinforcement learning, ai, agent, sonworld, sonworld, son, sonnhfit, sonworld",
)