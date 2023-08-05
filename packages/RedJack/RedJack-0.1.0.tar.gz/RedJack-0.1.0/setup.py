from setuptools import setup

setup(
    name='RedJack',
    version='0.1.0',
    author='Michal Nowikowski',
    author_email='godfryd@gmail.com',
    packages=['redjack'],
    url='http://redjacklab.net/',
    license='LICENSE.txt',
    description='RedJack - continuous integration system.',
    long_description=open('README.txt').read(),
    install_requires=['pyyaml>3.0', 'mako'],
    entry_points = {
        'console_scripts': [
            'rjserver = redjack.server:main',
            'rjagent = redjack.agent:main',
        ]
    }

)
