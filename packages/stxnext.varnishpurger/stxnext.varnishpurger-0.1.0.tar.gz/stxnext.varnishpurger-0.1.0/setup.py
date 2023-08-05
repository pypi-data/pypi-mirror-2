from setuptools import setup, find_packages

version = open('src/stxnext/varnishpurger/version.txt').read()

setup (
    name = 'stxnext.varnishpurger',
    version = version,
    author = 'STX Next Sp. z o.o, Radek Jankiewicz, Marcin Ossowski, Wojciech Lichota',
    author_email = 'info@stxnext.pl',
    description = 'Plone viewlet for purging varnish cache for given url.',
    keywords = 'python plone varnish purge',
    platforms = ['any'],
    license = 'Zope Public License, Version 2.1 (ZPL)',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['stxnext'],
    zip_safe = False,
    install_requires = ['setuptools',
                        ],
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Zope2',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Programming Language :: Python',
        ]
    )
