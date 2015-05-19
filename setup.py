try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path
import ndimage

path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(path, 'requirements.txt')

with open(path, 'r') as file_handle:
    requirements = file_handle.readlines()

config = {
    'description': 'Visualisation of lower dimensional representations of images transformed to by dimensionality reduction',
    'author': 'Samuel Jackson',
    'url': 'http://github.com/samueljackson92/NDImage',
    'download_url': 'http://github.com/samueljackson92/NDImage',
    'author_email': 'samueljackson@outlook.com',
    'version': ndimage.__version__,
    'install_requires': requirements,
    'packages': ['ndimage'],
    'name': 'ndimage'
}

setup(**config)
