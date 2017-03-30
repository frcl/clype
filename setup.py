import re
from setuptools import setup


def version():
    with open('clype/__init__.py', 'r') as init_file:
        _version = re.search('__version__ = \'([^\']+)\'',
                             init_file.read()).group(1)
    return _version


def readme():
    with open('readme.md', 'r') as readme_file:
        _readme = readme_file.read()
    return _readme


setup(
    name='clype',
    version=version(),
    description=('Python library for creating command line interfaces'
                 'using type annotations'),
    long_description=readme(),
    url='https://github.com/frcl/clype',
    author='Lars Franke',
    author_email='lars.franke@mailbox.org',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
    ],
    keywords='cli console typehints annotations',
    packages=['clype'],
)
