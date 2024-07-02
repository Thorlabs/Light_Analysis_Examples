from setuptools import setup

setup(
    name='pyOSA',
    version='3.31',
    packages=['pyOSA'],
    package_data={'pyOSA': ['defines_dictionaries.json']},
    description='A Python module for Thorlabs OSA (Optical Spectrum Analyzer)',
    install_requires=['numpy'],
)