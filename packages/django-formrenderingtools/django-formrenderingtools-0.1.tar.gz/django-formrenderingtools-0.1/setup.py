#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages


setup(
    name='django-formrenderingtools',
    version='0.1',
    url='http://bitbucket.org/benoitbryon/django-formrenderingtools',
    download_url='http://bitbucket.org/benoitbryon/django-formrenderingtools/downloads',
    author='Benoit Bryon',
    author_email='benoit@marmelune.net',
    license='BSD',
    description="An application for the `Django framework. It provides tools " \
                "for the template designer to customize forms. " \
                "Rather than using {{ form.as_p }}, set up and reuse " \
                "templates to render form elements.",
    long_description=open('README.txt').read(),
    platforms='Any',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    packages=find_packages(),
    include_package_data = True,
    install_requires=[
        'django>=1.1',
        'django-templateaddons>=0.1'
    ],
)
