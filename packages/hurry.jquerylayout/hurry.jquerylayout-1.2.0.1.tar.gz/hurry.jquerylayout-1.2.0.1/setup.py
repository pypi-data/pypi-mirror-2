from setuptools import setup, find_packages

JQUERY_LAYOUT_VERSION = '1.2.0'
version = '1.2.0.1'

import sys, os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(
    name='hurry.jquerylayout',
    version=version,
    description="hurry.resource style resources for jQuery UI.Layout.",
    long_description = long_description,
    classifiers=[],
    keywords='hurry.resource jquery',
    author='Martijn Faassen',
    author_email='faassen@startifact.com',
    license='MIT',
    packages=find_packages('src'),
    namespace_packages=['hurry'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'hurry.resource >= 0.10',
        'hurry.jquery',
        'hurry.jqueryui',
        ],
    entry_points = {
        'hurry.resource.libraries': [
            'jquerylayout = hurry.jquerylayout:jquerylayout_lib',
            ],
        },
    extras_require={
        'zopesupport': ['hurry.zoperesource'],
        },
    )
