"""Setup script for the python-act library module"""

from os import path

from setuptools import setup

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name="provreq-mcmc",
    version="0.0.17",
    author="mnemonic AS",
    zip_safe=True,
    author_email="opensource@mnemonic.no",
    description="Adversary Emulation Planner (AEP) Cyberhunt POC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="provreq,mcmc,attack,mnemonic",
    entry_points={
        "console_scripts": [
            "provreq-mcmc-create-stats= provreq.mcmc.create_stats:main",
            "provreq-mcmc-backsolve= provreq.mcmc.backsolve:main",
            "provreq-mcmc-statistics= provreq.mcmc.stats:main",
            "provreq-mcmc-montecarlo= provreq.mcmc.montecarlo:main",
        ]
    },
    # https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages
    namespace_packages=["provreq"],
    packages=["provreq.mcmc", "provreq.mcmc.aggregators"],
    url="https://github.com/mnemonic-no/provreq-mcmc",
    install_requires=[
        "caep",
        "provreq>=0.1.4",
        "tabulate",
        "stix2",
        "requests",
        "tabulate",
    ],
    python_requires=">=3.8, <4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
)
