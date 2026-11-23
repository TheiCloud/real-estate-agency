"""
Установка пакета real_estate.

Установка:

    pip install -e .
"""

from setuptools import setup, find_packages


setup(
    name="real-estate-agency",
    version="1.0.0",
    description="Учебный проект: система учёта агентства недвижимости",
    author="Student",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "test": ["pytest>=7.4.0"],
    },
)
