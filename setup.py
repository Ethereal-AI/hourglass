from setuptools import setup

__author__ = "Ethereal AI"

setup(
    name="hourglass",
    version="0.0.1",
    packages=["hourglass"],
    url="https://github.com/Ethereal-AI/hourglass",
    author=__author__,
    description="Detect and parse date-time entities in text.",
    install_requires=[
        "spacy>=3.1.2",
        "dateutil>=2.8.1",
    ],
)
