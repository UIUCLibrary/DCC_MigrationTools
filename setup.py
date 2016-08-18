from setuptools import setup
import sys

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        # self.pytest_args.append("--doctest-modules")
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='MigrationTools',
    version='0.1.0',
    packages=['MigrationTools', 'tests'],
    url='',
    license='',
    test_suite="tests",
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    author='Henry Borchers',
    author_email='hborcher@illinois.edu',
    description='Tools for migration',
)
