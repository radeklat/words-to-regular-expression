import setuptools

from src import __version__


setuptools.setup(
    name='words2regexp',
    version=__version__,
    url='https://github.com/radeklat/words-to-regular-expression',
    author='Radek Lat',
    author_email='radek.lat@gmail.com',
    description='A command line tool and Python library for converting '
                'lists of strings into matching regular expressions '
                '(finite automata).',
    long_description=open('README.md').read() + '\n' + open('CHANGES.md').read(),
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
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
    py_modules=['src'],
    entry_points={
        'console_scripts': [
            'w2re=src.w2re:main'
        ]
    },
    install_requires=[
        'typing;python_version<"3.4"',
    ]
)

