from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
# Also requires python-dev and python-openssl
setup(

    name = "AWSpider",
    version = "0.2.5.8",

    packages = find_packages(),

    install_requires = ['twisted>=8.1', 'genshi>=0.5.1', 'python-dateutil>=1.4', 'simplejson>=2.0.9'],
    include_package_data = True,
    
    # metadata for upload to PyPI
    author = "John Wehr",
    author_email = "johnwehr@gmail.com",
    description = "Amazon Web Services web crawler",
    license = "MIT License",
    keywords = "AWS amazon ec2 s3 simpledb twisted spider crawler",
    url = "http://github.com/wehriam/awspider/"
    
)