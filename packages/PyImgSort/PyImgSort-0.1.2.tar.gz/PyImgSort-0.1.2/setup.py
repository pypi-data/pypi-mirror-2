from distutils.core import setup

setup(
    name='PyImgSort',
    version='0.1.2',
    author='x.seeks',
    author_email='x.seeks@gmail.com',
    packages=['pyimgsort'],
    scripts=['bin/pyimgsort'],
    url='http://pypi.python.org/pypi/PyImgSort/',
    license='LICENSE.txt',
    description='Automatically organizes images by aspect ratio.',
    long_description=open('README.txt').read(),
)
