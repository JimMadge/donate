from setuptools import setup, find_packages

setup(
    name="donate",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        "pyxdg",
        "pyyaml",
        "tabulate"
        ],
    entry_points={
        "console_scripts": [
            "donate = donate.__main__:main"
            ]
        }
    )
