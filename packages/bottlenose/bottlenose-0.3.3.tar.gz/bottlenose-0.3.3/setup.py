from setuptools import setup, find_packages
import sys, os

version = '0.3.3'

install_requires = []

CURRENT_FOLDER = os.path.dirname(__file__)

def _py26OrGreater():
    return sys.hexversion > 0x20600f0

if not _py26OrGreater():
    install_requires.append("simplejson>=1.7.1")

setup(name='bottlenose',
      version=version,
      description="A Python hook into the Amazon.com Product Advertising API",
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
          ],
      keywords='amazon, product advertising, api',
      author='Dan Loewenherz',
      author_email='bottlenose@dlo.me',
      url='http://github.com/dlo/bottlenose',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
)
