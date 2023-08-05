import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "yopypi",
    version = "0.0.1",
    packages = find_packages(),
    scripts = ['yopypi/cli.py'],
    install_requires = ['bottle>=0.8', 'supay', 'paste'],
    entry_points = {
        'console_scripts': [
            'yopypi-cli = cli:main'
            ]
        },
    include_package_data=True,
    package_data = {
        '': ['distribute_setup.py'],
        },

    # metadata for upload to PyPI
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "An outoing balancer for PYPI",
    long_description = """\
A self balancing instance that will redirect your PYPI request 
when PYPI is down to a default (or predefined) PYPI mirror.
 """,

    license = "MIT",
#    py_modules = ['yopypi'],
    keywords = "pypi mirror performance balancer",
    url = "http://code.google.com/p/yopypi",   

)

