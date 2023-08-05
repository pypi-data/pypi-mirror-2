from setuptools import setup, find_packages
setup(
    name = "quaternionarray",
    version = "0.6.1",
    py_modules = ['quaternionarray, test_quaternionarray'], 

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "Andrea Zonca",
    author_email = "code@andreazonca.com",
    description = "Python package for fast quaternion arrays math",
    license = "GPL3",
    keywords = "quaternion, nlerp, rotate",
    url = "http://andreazonca.com/software/quaternion-array/",   # project home page, if any
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Office/Business',
          'Topic :: Scientific/Engineering :: Physics',
          ],
)
