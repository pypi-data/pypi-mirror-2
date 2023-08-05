"""
Implements Tipfy authentication using RPX/JanRain Engage.
"""
from setuptools import setup

setup(
    name = 'tipfy.ext.auth.rpx',
    version = '0.1',
    license = 'BSD',
    url = 'http://code.google.com/p/tipfy-ext-auth-rpx/',
    description = 'Implements Tipfy authentication using RPX/JanRain Engage.',
    long_description = __doc__,
    author = 'Ragan Webber',
    author_email = 'raganw@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
        'tipfy',
        'tipfy.ext',
        'tipfy.ext.auth',
    ],
    namespace_packages = [
        'tipfy',
        'tipfy.ext',
        'tipfy.ext.auth',
    ],
    include_package_data = True,
    install_requires = [
        'tipfy.ext.auth',
    ],
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
