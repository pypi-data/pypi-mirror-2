from setuptools import setup, find_packages

setup(
    name = "py_1digit_checksum",
    version = "0.0.1",
    description="Several 1-digit checksum algorithms",
    author = "Hermann Himmelbauer",
    author_email = "hermann@qwer.tk",
    license = "LGPL",
    packages = ['py_1digit_checksum'],
    test_suite = "py_1digit_checksum.test",
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
    }
)
