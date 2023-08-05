
from setuptools import setup

setup(
    name='pytest-yamlwsgi',
    description='Run tests against wsgi apps defined in yaml',
    author='Ali Afshar',
    author_email='aafshar@gmail.com',
    version='0.6',
    py_modules = ['pytest_yamlwsgi'],
    entry_points = {
        'pytest11': [
            'pytest_yamlwsgi = pytest_yamlwsgi',
        ]
    },
    install_requires = ['py>=1.3.0', 'Werkzeug', 'pyyaml'],
)

