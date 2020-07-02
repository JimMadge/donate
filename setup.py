from setuptools import setup, find_packages

setup(
    name="donate",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyxdg",
        "pyyaml"
        ],
    entry_points={
        "console_scripts": [
            "donate = donate.__main__:main"
            ]
        }
    )
