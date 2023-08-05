from setuptools import setup, find_packages
import os, sys


setup(
    name='rtjp',
    version='0.2.1',
    author='Michael Carter',
    author_email='CarterMichael@gmail.com',
    url='',
    license='MIT License',
    description='eventlet and concurrence implementation of the rtjp protocol',
    long_description='',
    packages= find_packages(),
    zip_safe = False,
    install_requires = [ ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],        
)

