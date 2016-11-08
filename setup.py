try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return 'see README'


setup(
    name='hypernova',
    version='0.0.3',
    author='Stephen Hurwitz',
    author_email='ornj@stevehurwitz.com',
    url='https://github.com/ornj/hypernova-python',
    description='Python client for Hypernova, https://github.com/airbnb/hypernova',
    long_description=read('readme.md'),
    keywords='hypernova react javascript client',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    license='MIT License',
    install_requires=['six', 'requests'],
    packages=['hypernova', 'hypernova.plugins'],
    include_package_data=True
)
