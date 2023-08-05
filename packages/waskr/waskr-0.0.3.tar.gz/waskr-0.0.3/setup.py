import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

tests_require = ['nose', 'webtest']

setup(
    name = "waskr",
    version = "0.0.3",
    packages = find_packages(),
    scripts = ['waskr/waskrc.py'],
    install_requires = ['bottle>=0.8', 'pymongo'],
    entry_points = {
        'console_scripts': [
            'waskrc = waskrc:main'
            ]
        },
    include_package_data=True,
    package_data = {
        '': ['distribute_setup.py'],
        },

    # metadata for upload to PyPI
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "Stats Middleware for WSGI applications.",
    long_description = """\
 Provides a couple of ways to measure how well a WSGI application
 is performing via:
  * Requests Per Second via RequestCounterMiddleware
  * Request Duration via RequestDurationMiddleware
 """,

    license = "MIT",
    py_modules = ['waskr'],
    keywords = "WSGI stats statistics request measure performance",
    url = "http://code.google.com/p/waskr",   

)

