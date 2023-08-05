from distutils.core import setup

import simpledaemon

setup(
    name='SimpleDaemon',
    version='.'.join(map(str, simpledaemon.VERSION)),
    author="Shane Hathaway",
    author_email = "shane@hathawaymix.org",
    maintainer="Don Spaulding",
    maintainer_email="donspauldingii@gmail.com",
    packages=['simpledaemon'],
    license=open('LICENSE.txt').read(),
    description="Provides a simple Daemon class to ease the process of forking a python application on Unix systems.",
    long_description=open('README.txt').read(),
    url='http://bitbucket.org/donspaulding/simpledaemon/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
    ],
)