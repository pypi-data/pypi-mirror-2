import chrome_remote_shell
import sys
from distutils.core import setup

requirements = []
if sys.version_info < (2, 6):
    requirements.append('simplejson')

setup(
    name='chrome_remote_shell',
    version='1.2',
    description='Client for talking to the Google Chrome remote shell port',
    long_description=chrome_remote_shell.__doc__.split('\n\n', 1)[1],
    author='Brandon Craig Rhodes',
    author_email='brandon@rhodesmill.org',
    url='http://bitbucket.org/brandon/chrome_remote_shell/',
    packages=['chrome_remote_shell'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        ],
    install_requires=requirements,
    )
