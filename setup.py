import setuptools


setuptools.setup(
    name='fuzzy-tribble',
    version='0.0.1',
    description='Processing GoC spending data',
    long_description='',
    author='Jason White',
    author_email='actinolite.jw@gmail.com',
    url='https://github.com/GoC-Spending/fuzzy-tribble',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    entry_points='''
        [console_scripts]
        tribble=tribble.cli:main
    ''',
)
