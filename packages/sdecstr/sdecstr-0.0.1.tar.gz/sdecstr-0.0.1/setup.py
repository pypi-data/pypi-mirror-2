from setuptools import setup, find_packages

setup(
    name = "sdecstr",
    version = "0.0.1",
    description="Decimal datatype stored as a signed string, enabling rich comparisons.",
    author = "Hermann Himmelbauer",
    author_email = "dusty@qwer.tk",
    license = 'LGPL',
    packages = ['sdecstr'],
    test_suite = "sdecstr.test",
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
    }
)
