
from setuptools import setup

setup(
    name='pytest-yamlwsgi',
    description='Run tests against wsgi apps defined in yaml',
    author_email='aafshar@gmail.com',
    version='0.1',
    py_modules = ['pytest_yamlwsgi'],
    entry_points = {
        'pytest11': [
            'pytest_yamlwsgi = pytest_yamlwsgi',
        ]
    },
)

