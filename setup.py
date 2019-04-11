import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='gbscli',
    version='0.1.0',
    author='Box and Whisker',
    author_email='box@boxnwhis.kr',
    description='GreedyBandit CLI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/boxnwhiskr/gbscli',
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'click==7.0',
        'requests==2.21.0',
    ],
    tests_require=[
        'pytest==4.4.0',
        'requests-mock==1.5.2',
    ],
    entry_points='''
        [console_scripts]
        gbs=gbscli.entrypoint:cli
    ''',
)
