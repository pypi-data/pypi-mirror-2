from setuptools import setup, find_packages

PACKAGE_NAME = 'supermin'

VERSION = __import__(PACKAGE_NAME).__version__

setup(
    name=PACKAGE_NAME,
    author='Jonas Obrist',
    version=VERSION,
    scripts=['bin/supermin'],
    packages=find_packages(),
    package_data={
        'supermin': [
            'default_configs.cfg',
        ],
    },
)
