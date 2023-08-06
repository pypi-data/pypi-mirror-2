from distutils.core import setup
import pyqtrailer

setup(name='pyqtrailer',
      version=pyqtrailer.__version__,
      description='PyQt4 application to download trailers from www.apple.com/trailers',
      author='Stanislav Ochotnicky',
      author_email='sochotnicky@gmail.com',
      url='http://code.google.com/p/pyqtrailer',
      requires=["pytrailer"],
      install_requires=['pytrailer>=0.2',"python-dateutil >= 1.5"],
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: User Interfaces',
                   'Topic :: Multimedia :: Video'],
      keywords="movie trailer apple module pyqt qt4",
      license="GPLv3",
      platforms=["any"],
      packages=["pyqtrailer",
                "pyqtrailer.qtcustom"],
      scripts=["scripts/pyqtrailer"],
     )
