from setuptools import setup
from justrss import __version__

if __name__ == '__main__':
    package_name = 'justrss'
    setup(name=package_name,
          version=__version__,
          py_modules=[package_name],
          test_suite='test')
