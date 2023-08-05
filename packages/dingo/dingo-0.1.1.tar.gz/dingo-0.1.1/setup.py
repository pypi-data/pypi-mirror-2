try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "dingo",
    version = "0.1.1",
    url = 'http://gitorious.org/dingo',

    long_description=(
         file('README.txt','r').read()
         + '\n'),

    packages = ['dingo',],
    package_dir = {'':'src'},
    
    install_requires = ['django'],

    include_package_data = True,
    package_data = {
        'dingo': ['templates/*.html'],
        },
    zip_safe = True,

    author = 'Nathan R. Yergler',
    author_email = 'nathan@yergler.net',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        ],

    )
