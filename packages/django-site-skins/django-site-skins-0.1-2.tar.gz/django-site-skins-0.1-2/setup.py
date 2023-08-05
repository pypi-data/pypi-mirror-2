from setuptools import setup, find_packages

version = __import__('skins').__version__

setup(
    name = 'django-site-skins',
    version = version,
    description = "site-skins",
    long_description = """Django site skins provides django apps with the ability to use skins with mulitple sites, automatically determining the correct skin based on the request.""",
    author = 'Bruce Kroeze',
    author_email = 'bruce@ecomsmith.com',
    url = 'http://bitbucket.org/bkroeze/django-site-skins/',
    license = 'New BSD License',
    platforms = ['any'],
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'],
    packages = find_packages(),
    include_package_data = True,
)
