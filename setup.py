from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tmai-api",
    version="0.3.0",  # Updated version
    author="TMAI",
    author_email="info@tokenmetrics.ai",
    description="Python SDK for Token Metrics AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/token-metrics/tmai-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "pandas",
    ],
)
