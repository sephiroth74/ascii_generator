from setuptools import setup
import sys
import os

assert sys.version_info >= (3, 8, 0), "black requires Python 3.8+"
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    return (
        (CURRENT_DIR / "README.md").read_text(encoding="utf8")
        + "\n\n"
        + (CURRENT_DIR / "CHANGES.md").read_text(encoding="utf8")
    )


USE_MYPYC = False
# To compile with mypyc, a mypyc checkout must be present on the PYTHONPATH
if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    USE_MYPYC = True
if os.getenv("BLACK_USE_MYPYC", None) == "1":
    USE_MYPYC = True

if USE_MYPYC:
    mypyc_targets = [
        "src/ascii_generator/__init__.py",
        "src/ascii_generator/libs/__init__.py",
        "src/ascii_generator/libs/logger.py",
    ]

    from mypyc.build import mypycify

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    ext_modules = mypycify(mypyc_targets, opt_level=opt_level)
else:
    ext_modules = []

setup(
    name="ascii_generator",
    use_scm_version={
        "write_to": "src/_ascii_generator_version.py",
        "write_to_template": 'version = "{version}"\n',
    },
    description="Simple python ascii art generator.",
    long_description="get_long_description()",
    long_description_content_type="text/markdown",
    keywords="ascii art generator image",
    author="Alessandro Crugnola",
    author_email="alessandro.crugnola@gmail.com",
    url="https://github.com/sephiroth74/ascii_generator",
    license="MIT",
    py_modules=["_ascii_generator_version"],
    ext_modules=ext_modules,
    package_dir={"": "src"},
    python_requires=">=3.8",
    zip_safe=False,
    install_requires=[
        "requests>=2.24.0",
        "Pillow>=7.2.0",
        "coloredlogs>=10.0",
    ],
    extras_require={
    },
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