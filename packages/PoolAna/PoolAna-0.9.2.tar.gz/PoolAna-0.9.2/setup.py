from distutils.core import setup

setup(
    name='PoolAna',
    version='0.9.2',
    author='J.S. Wilson',
    author_email='jsw@mps.ohio-state.edu',
    packages=['poolana'],
    url='http://pypi.python.org/pypi/PoolAna/',
    license='GPLv2',
    description='Worker process pool based analysis framework for use with PyROOT.',
    long_description=open('README').read(),
)
