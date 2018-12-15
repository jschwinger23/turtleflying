from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.1'

setup(
    name='turtleflying',
    url='https://github.com/jschwinger23/turtleflying',
    description='alternative of Gevent',
    author='zc',
    author_email='greychwinger@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pytimerfd>=1.2.0,<2.0.0',
        'greenlet>=0.4.15,<1.0.0',
    ],
    python_requires='>=3.6.1',
    platform='Linux',
)
