import setuptools


setuptools.setup(
    name='rcl',
    version='0.1',
    author='Ben Ryder',
    author_email='dev@benryder.me',
    description='A simple command line wrapper for rclone focused on easy folder syncing',
    keywords=['rclone', 'rclone-wrapper'],
    url='https://github.com/Ben-Ryder/rcl',
    download_url='https://github.com/Ben-Ryder/rcl/archive/v_01.tar.gz',
    py_modules=['rcl'],
    install_requires=[
        'Click',
        'toml'
    ],
    entry_points='''
        [console_scripts]
        rcl=rcl:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    license='GPLV3',
)
