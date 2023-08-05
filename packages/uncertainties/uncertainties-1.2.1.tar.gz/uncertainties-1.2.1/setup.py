#!/usr/bin/python

from distutils.core import setup

setup(name='uncertainties', version='1.2.1',
      author='Eric O. LEBIGOT (EOL)',
      author_email='eric.lebigot@normalesup.org',
      url='http://pypi.python.org/pypi/uncertainties/',
      
      license='''\
This software is released under a dual license.  (1) The GNU General \
Public License version 2.  (2) Any other license, as long as it is \
obtained from the original author.''',
      
      description=('Transparent calculations with uncertainties on the'
                     ' quantities involved (aka "error propagation") ;'
                     ' calculation of derivatives'),
      
      long_description=u'''\
``uncertainties`` allows calculations such as (0.2 +/- 0.01)*2 = 0.4
+/- 0.02 to be performed transparently; much more complex mathematical
expressions involving numbers with uncertainties can also be evaluated
transparently.

**Correlations** between expressions are correctly taken into account.
``x-x`` is thus exactly zero, for instance (more naive implementations
found on the web yield a non-zero uncertainty for ``x-x``, which is
incorrect). Whatever the complexity of the calculation and the number
of steps involved, the uncertainties produced by this program are what
is predicted by `error propagation theory`_.


Basic examples::

    import uncertainties
    from uncertainties.umath import *  # sin(), etc.

    # Mathematical operations:
    x = uncertainties.NumberWithUncert((0.20, 0.01))  # x = 0.20+-0.01
    x = uncertainties.NumberWithUncert("0.20(1)")  # Other representation
    print x**2  # Square: prints "0.04+-0.004"
    print sin(x**2)  # Prints "0.0399...+-0.00399..."

    print x.position_in_sigmas(0.17)  # Prints "-3.0": deviation of -3 sigmas

    # Access to the nominal value, and to the uncertainty:
    square = x**2  # Square
    print square  # Prints "0.04+-0.004"  
    print square.nominal_value  # Prints "0.04"
    print square.std_dev()  # Prints "0.004..."

    print square.derivatives[x]  # Partial derivative: prints "0.4" (= 2*0.20)

    print square - x*x  # Exactly zero: correlations taken into account

The Python_ (or IPython_) shell can thus be used as a powerful
calculator that handles quantities with uncertainties (``print``
statements are optional, which is convenient).

**Almost all mathematical operations** are supported, including most 
functions from the standard math_ module (sin,...) and functions from the 
third-party numpy_ module (fast operations on arrays and matrices). 
Comparison operators (``>``, ``==``, etc.) are supported too.  There is 
no restriction on the complexity of mathematical expressions, or on the 
number of variables involved (x-sin(x)+y**2-tan(y*x) can for example be 
calculated, whether x and y are quantities with uncertainties or not).

Another possible use of this module is the calculation of **partial 
derivatives** of mathematical functions.

Additional examples and information can be obtained with ``pydoc 
uncertainties`` and ``pydoc uncertainties.umath`` after installation.

Please send feature requests, bug reports, or feedback to
`Eric O. LEBIGOT (EOL)`_.

*Installation*: ``sudo easy_install uncertainties`` might be
sufficient, depending on your installation (this does not require any
manual download, but requires setuptools_).  For additional
installation methods, download the source archive, and see the
``README.txt`` file that it contains.

*Version history* (main changes only):

- 1.2: a new function, ``wrap()``, is exposed, which allows non-Python \
       functions (e.g. Fortran or C used through a module such as Scipy) to \
       handle numbers with uncertainties.
- 1.1: mathematical functions (such as cosine, etc.) are in a new \
       uncertainties.umath module; \
       they do not override functions from the math module anymore.
- 1.0.12: main class (``Number_with_uncert``) renamed ``NumberWithUncert`` \
          so as to follow `PEP 8`_.
- 1.0.11: ``origin_value`` renamed more appropriately as \
          ``nominal_value``.
- 1.0.9: ``correlations()`` renamed more appropriately as \
         ``covariance_matrix()``.

.. _Python: http://docs.python.org/tutorial/interpreter.html
.. _IPython: http://ipython.scipy.org/
.. _numpy: http://numpy.scipy.org/
.. _math: http://docs.python.org/library/math.html
.. _PEP 8: http://www.python.org/dev/peps/pep-0008/
.. _error propagation theory: http://en.wikipedia.org/wiki/Propagation\
_of_uncertainty
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _Eric O. LEBIGOT (EOL): mailto:eric.lebigot@normalesup.org
''',
      
      keywords=['error propagation', 'uncertainties',
                  'uncertainty calculations',
                  'standard deviation',
                  'derivatives', 'partial derivatives', 'differentiation'],
      
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities'
          ],

      # Files are defined in MANIFEST.in
      packages=['uncertainties']
      # py_modules=['uncertainties', 'uncertainties.umath']
      )


