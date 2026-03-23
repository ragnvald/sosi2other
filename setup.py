from setuptools import setup

setup(
    name='sosi2other',
    version='0.8',
    description='SOSI to KML conversion utility',
    scripts=['sosi2kml.py'],
    install_requires=[
        'configobj',
        'psycopg2',
    ],
)