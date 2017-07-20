import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    content = 'not found'
    try:
        with open(fname) as file:
            content = file.read()
    except:
        print(u'Warning: failed to open file {0}'.format(fname))
        pass
    return content

requires = [
    'lxml',
    'kend==0.7.1',
    'pyutopia==3.1.0.10',
    'pyutopia-tools==3.1.0.10',
]

setup(
    name='pyutopia-plugins-common',
    version='3.1.0.10',
    author='David Thorne',
    author_email='davethorne@gmail.com',
    description='Utopia common plugins package',
    long_description=read('README.rst'),
    license=read('LICENSE.txt'),
    url='https://github.com/lostislandlabs/python-utopia-plugins-common',
    packages=['utopia.plugins'],
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
    ],
)
