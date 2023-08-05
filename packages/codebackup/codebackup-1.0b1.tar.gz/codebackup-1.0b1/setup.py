from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '1.0b1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'argparse',
]


setup(name='codebackup',
    version=version,
    description="A simple tool to backup your Github and Bitbucket repositories",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='github bitbucket backup mercurial git',
    author='Sridhar Ratnakumar',
    author_email='sridhar.ratna@gmail.com',
    url='http://github.com/srid/codebackup',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['codebackup=codebackup:main']
    }
)
