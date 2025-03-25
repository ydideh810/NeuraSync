from setuptools import setup, find_packages

setup(
    name="neura-sync-sdk",
    version="0.1.0",
    description="SDK for interacting with NEURA-SYNC distributed execution platform",
    author="NEURA-SYNC Team",
    author_email="contact@neura-sync.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "grpcio",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
