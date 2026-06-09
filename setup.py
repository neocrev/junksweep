from setuptools import setup, find_packages

setup(
    name="junksweep",
    version="1.0.0",
    description="Find and clean junk directories reclaim gigabytes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["cleanup", "disk-space", "cli", "developer-tools", "node_modules"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "junksweep=junksweep:main",
        ],
    },
    url="https://github.com/neocrev/junksweep",
)
