"""pdjn - the CLI tool of Pdjn"""

from setuptools import setup


setup(
    name='pdjn',
    version='0.1',
    description="CLI tool for managing Pydjn sites",
    url='https://github.com/hipikat/hpk.io/tree/master/src/cli',
    license='ISC',
    author='Ada Wright',
    author_email='ada@hpk.io',
    py_modules=['pdjn'],
    install_requires=['click',],
    entry_points='''
        [console_scripts]
        pdjn=pdjn:cli
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
