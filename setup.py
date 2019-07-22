from setuptools import setup

with open('.version', 'r') as f:
    VERSION = f.read()

setup(
    name='zmqpc',
    description='High performance inter-process communication using zmq.',
    author='Allen Zhang',
    version=VERSION,
    packages=[
        'zmqpc',
    ],
    install_requires=[
        'colorlog',
        'pyarrow',
        'pyzmq',
    ],
    extras_require = {
        'test': [
            'pytest',
        ],
    },
)
