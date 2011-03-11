from setuptools import setup, find_packages

from rattlesnake import __version__
version = __version__

setup(

    name='rattlesnake',
    version=version,
    description="dangerous web framework",
    classifiers=[],
    keywords='rattlesnake',
    author='Matt Wilson',
    author_email='matt@tplus1.com',
    url='http://rattlesnake.tplus1.com',
    license='BSD',
    packages=find_packages(exclude=['docs', 'pitzdir']),
    include_package_data=True,

    package_dir={'rattlesnake': 'rattlesnake'},

    zip_safe=False,

    install_requires=[],

    test_suite='nose.collector',

)
