from setuptools import setup

version = '1.3.1'

setup(name='tcpwatch',
      version=version,
      description="TCP monitoring and logging tool with support for HTTP 1.1",
      long_description= open('README.txt').read() + '\n\n' +
                        open('CHANGES.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='tcp monitor proxy',
      author='Shane Hathaway',
      author_email='shane@zope.com',
      url='http://hathawaymix.org/Software/TCPWatch',
      py_modules = ['tcpwatch'],
      package_data = {
        '': ['*.txt', '*.rst']
      },
      license="ZPL 2.0",
      zip_safe=False,
      install_requires=[],
      entry_points= {
        'console_scripts': [
                'tcpwatch = tcpwatch:run_main',
            ],
      },
      )
