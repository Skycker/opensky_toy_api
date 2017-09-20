from distutils.core import setup

import opensky_toy_api

setup(
    name='opensky_toy_api',
    version=opensky_toy_api.__version__,
    packages=['opensky_toy_api'],
    url='https://github.com/Skycker/opensky_toy_api',
    license='MIT',
    author='Kirill Kostyukhin',
    author_email='kostyukhin.kirill@gmail.com',
    description='API for opensky service',
    install_requires=['requests'],
    setup_requires=['requests'],
    keywords="opensky api",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)
