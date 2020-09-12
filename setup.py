from setuptools import setup
import sys
import os

assert sys.version_info >= (3, 6, 0), "ascii_generator requires Python 3.6+"
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    return "DESCRIPTION"

ext_modules = []

setup(
    name="ascii_generator",
    use_scm_version={
        "write_to": "src/_ascii_generator_version.py",
        "write_to_template": 'version = "{version}"\n',
    },
    description="Simple python ascii art generator.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="ascii art generator image",
    author="Alessandro Crugnola",
    author_email="alessandro.crugnola@gmail.com",
    url="https://github.com/sephiroth74/ascii_generator",
    license="MIT",
    py_modules=["_ascii_generator_version"],
    ext_modules=ext_modules,
    packages=["ascii_generator"],
    package_dir={"": "src"},
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=[
        "requests>=2.24.0",
        "Pillow>=7.2.0",
        "coloredlogs>=10.0",
    ],
    extras_require={},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "ascii_generator=ascii_generator:main",
        ]
    },
)