# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# To create destribution
# pip install wheel
# Use cmd
# python setup.py bdist_wheel
# twine upload dist/<...>.whl

setup(
    name='fortnum',
    version='0.0.1',
    description='Singletons using class syntax',
    # long_description=io.open('README.rst', encoding='utf-8').read() + '\n\n' +
    #     io.open('HISTORY.rst', encoding='utf-8').read(),
    author='Sverker Sjöberg',
    url='https://github.com/SverkerSbrg/fortnum',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)