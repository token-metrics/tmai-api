from setuptools import setup, find_packages

setup(
    name="tmai-openai",
    version="1.0.0",
    description="Token Metrics AI helper library for OpenAI Agents",
    author="Token Metrics",
    author_email="support@tokenmetrics.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pyjwt>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
