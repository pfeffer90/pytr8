from distutils.core import setup

from setuptools import find_packages

setup(
    name='pytr8',
    version='0.1',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=["numpy", "pandas", "lykkex"],
    url='https://github.com/pfeffer90/pytr8',
    license='MIT',
    author='Paul Pfeiffer, Stefan Voigt',
    author_email='',
    description='We create a trading algorithm in Python based on [the Lykke exchange](https://www.lykke.com/). The framework allows users to fetch current prices, to submit market and limit orders, and to track execution of the trades in a '
                'simple fashion.',
    entry_points={
        'console_scripts': [
            'pytr8=pytr8.pytrade:main',
        ],
    }
)
