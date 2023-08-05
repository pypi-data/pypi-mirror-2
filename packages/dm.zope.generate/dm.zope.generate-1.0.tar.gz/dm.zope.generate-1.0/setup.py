from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      install_requires=[] ,
      namespace_packages=['dm', 'dm.zope'],
      zip_safe=False,
      entry_points = dict(
        ),
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'zope', 'generate')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.zope.generate',
      version=pread('VERSION.txt').split('\n')[0],
      description="Code generation to facilitate Zope[2] application development.",
      long_description=pread('README.txt'),
      classifiers=[
#        'Development Status :: 3 - Alpha',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Framework :: Zope2',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/dm.zope.generate',
      packages=['dm', 'dm.zope', 'dm.zope.generate'],
      keywords='application development zope',
      license='BSD',
      **setupArgs
      )
