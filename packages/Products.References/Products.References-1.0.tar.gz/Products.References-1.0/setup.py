from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      namespace_packages=['Products'],
      zip_safe=False, # to let the tests work
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'Products', 'References')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='Products.References',
      version=pread('VERSION.txt').split('\n')[0],
      description='References to Zope objects for Zope 2.10 (or above)',
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Zope2',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/Products.References',
      packages=['Products', 'Products.References',],
      keywords='Zope 2, reference, symbolic link',
      license='BSD',
      **setupArgs
      )



