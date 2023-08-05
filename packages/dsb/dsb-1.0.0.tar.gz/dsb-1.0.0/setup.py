#!/usr/bin/env python
#
#   setup.py
#   dsb
#

# Bootstrap setuptools
import ez_setup
ez_setup.use_setuptools()

# Install package
from setuptools import setup, find_packages

setup(
    name="dsb",
    version='1.0.0',
    
    packages=find_packages(),
    package_data={
        'dsb.accounts': ['templates/registration/*.html'],
        'dsb.services': ['templates/services/tags/*.html'],
    },
    
    install_requires=[
        'Django>=1.0.0',
        'pytz',
    ],
    
    zip_safe=True,
    
    author="Ross Light",
    author_email="ross@zombiezen.com",
    url="https://launchpad.net/dsb/",
    description="DSB gives you what Django should have. For your website to "
                "run, you need Survival Basics.",
    long_description="Survival basics include: template tags for Google "
                     "Webmaster Tools and Analytics, static resource URLs, and "
                     "timezone support.",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
