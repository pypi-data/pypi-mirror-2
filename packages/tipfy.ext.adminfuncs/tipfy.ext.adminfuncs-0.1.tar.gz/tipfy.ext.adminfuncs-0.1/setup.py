"""
Tipfy module to automatically build admin function runner
"""
from setuptools import setup

setup(
    name = 'tipfy.ext.adminfuncs',
    version = '0.1',
    license = 'BSD',
    description = 'short_description',
    long_description = __doc__,
    author = 'Brandon Thomson',
    author_email = 'brandon.j.thomson@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
        'tipfy',
        'tipfy.ext',
    ],
    namespace_packages = [
        'tipfy',
        'tipfy.ext',
    ],
    include_package_data = True,
    install_requires = [
        'tipfy',
        'tipfy.ext.jinja2',
        'adminfuncs',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
