from setuptools import setup

setup(
    name='lektor-git',
    version='0.1',
    author='Ryan Hiebert',
    author_email='ryan@ryanhiebert.com',
    license='MIT',
    package_dir={'': 'src'},
    py_modules=['lektor_git'],
    url='https://github.com/ryanhiebert/lektor-git',
    install_requires=[
        'Lektor>=2',
    ],
    entry_points={
        'lektor.plugins': [
            'git = lektor_git:GitPlugin',
        ]
    }
)
