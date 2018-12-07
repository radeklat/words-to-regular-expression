import setuptools

from src import __version__, APPLICATION_NAME


DESCRIPTION = (
    'A command line tool and Python library for converting lists of strings '
    'into matching regular expressions (finite automata).'
)


setuptools.setup(
    name=APPLICATION_NAME,
    version=__version__,
    url='https://github.com/radeklat/words-to-regular-expression',
    author='Radek Lat',
    author_email='radek.lat@gmail.com',
    description=DESCRIPTION,
    long_description=(
        DESCRIPTION + '\n\nSee project on GitHub: '
        'https://github.com/radeklat/words-to-regular-expression\n\nChangelog: '
        'https://github.com/radeklat/words-to-regular-expression/blob/develop/'
        'CHANGELOG.md#unreleased'
    ),
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
    license='MIT',
    packages=setuptools.find_packages(exclude=["tests.*"]),
    entry_points={
        'console_scripts': [
            APPLICATION_NAME + '=src.w2re:main'
        ]
    }
)

