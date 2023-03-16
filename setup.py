import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="metrics",
    version="0.1.0",
    description="Metrics CLI for delivery managers",
    author="Rahul Nehru",
    author_email="rnehru92@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        "click", "hvac", "requests", "pyyaml"
    ],
    test_suite="tests",
    entry_points={"console_scripts": ["metrics=src.metrics:main"]},
)
