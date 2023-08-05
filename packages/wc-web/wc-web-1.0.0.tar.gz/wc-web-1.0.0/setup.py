"""
WidgetCo - web which depends on wc-socket.

This is demonstrating how to create namespace packages.

See my blog article which explains their usage here: 

    http://www.sourceweaver.com/posts/python-namespace-packages

This should eggify and in theory upload to pypi without problems.

This is released under the BSD license.

Oisin Mulvihill
2010-05-31

"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

Name='wc-web'
ProjecUrl=""
Version='1.0.0'
Author='Oisin Mulvihill'
AuthorEmail='oisinmulvihill at gmail dot com'
Maintainer=' Oisin Mulvihill'
Summary='WidgetCo web: This is a fake web module used to teach namespace packages ( http://www.sourceweaver.com/posts/python-namespace-packages).'
License='BSD License'
ShortDescription=Summary
Description=Summary

needed = [
    'wc-socket==1.0.0',
]


# Include everything under package dir. I needed to add a __init__.py
# to each directory inside package. I did this using the following
# handy command:
#
#  find lib/wc -type d -exec touch {}//__init__.py \;
#
# If new directories are added then I'll need to rerun this command.
#
EagerResources = [
    'wc',
]

ProjectScripts = [
    'scripts/runweb',
]

PackageData = {
    '': ['*.*'],
}

# Make exe versions of the scripts:
EntryPoints = {
    'console_scripts': [
        'runweb =wc.web.hello:main',
    ]
}

setup(
#    url=ProjecUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    license=License,
    scripts=ProjectScripts,
    install_requires=needed,
    include_package_data=True,
    packages=find_packages('lib'),
    package_data=PackageData,
    package_dir = {'': 'lib'},
    eager_resources = EagerResources,
    entry_points = EntryPoints,
    namespace_packages = ['wc'],
)

