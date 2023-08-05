
from setuptools import setup

setup(
    name='bu',
    version='0.1',
    author='Ali Afshar',
    author_email='aafshar@gmail.com',
    url='http://packages.python.org/bu',
    description='Build Utilities, a microscopic build system.',
    license='GPLv3',
    packages=[
        'bu',
        'bu.actions',
        'bu.lib',
        'bu.tools',
    ],
    package_data = {
        'bu.lib': ['*.bu'],
        'bu.tools': ['bu.vim'],
    },
    scripts = [
        'bin/bu',
    ],
    install_requires = [
        'argparse',
        'execnet',
    ],
    entry_points = {'pygments.lexers': ['bu=bu.tools.bupygments:BuLexer']},
)

