from distutils.core import setup

setup(name = 'uncertainties', version = '1.0.17',
      author = 'Eric O. LEBIGOT (EOL)',
      author_email = 'eric.lebigot@normalesup.org',
      url = 'http://pypi.python.org/pypi/uncertainties/',
      
      license = '''\
This software is released under a dual license.  (1) The GNU General \
Public License version 2.  (2) Any other license, as long as it is \
obtained from the original author.''',
      
      description = ('Transparent calculations with uncertainties on the'
                     ' quantities involved (aka "error propagation") ;'
                     ' calculation of derivatives'),
      
      long_description = '''\
``uncertainties`` allows calculation such as (0.2 +- 0.01)**2 = 0.04 +- 0.004
to be performed transparently.

**Correlations** between expressions are correctly taken into account. 
``x-x`` is exactly zero, for instance (more naive implementations found 
on the web yield a non-zero uncertainty for ``x-x``, which is 
incorrect). Whatever the complexity of the calculation and the number of 
steps involved, the uncertainties produced by this program are
what is predicted by `error propagation theory`_.


Basic examples::

    import uncertainties
    from math import *  # Must be done *after* importing uncertainties

    # Mathematical operations:
    x = uncertainties.NumberWithUncert((0.20, 0.01))  # x = 0.20+-0.01
    x = uncertainties.NumberWithUncert("0.20(1)")  # Other representation
    print x**2  # Prints "0.04+-0.004"
    print sin(x**2)  # Prints "0.0399...+-0.00399..."

    print x.position_in_sigmas(0.17)  # Prints "-3.0": deviation of -3 sigmas

    # Access to the nominal value, and to the uncertainty:
    s = x**2  # Square
    print s  # Prints "0.04+-0.004"  
    print s.nominal_value  # Prints "0.04"
    print s.std_dev()  # Prints "0.004..."

    print s.derivatives[x]  # Partial derivative: prints "0.4" (= 2*0.20)

    print s - x*x  # Exactly zero: correlations taken into account

The Python_ (or IPython_) shell can thus be used as a powerful 
calculator that handles quantities with uncertainties (``print`` 
statements are optional, and all mathematical functions can for instance 
be imported with ``from math import *`` *after* importing this module 
with ``import uncertainties``).

**Almost all mathematical operations** are supported, including most
functions from the standard math_ module and functions from the
third-party numpy_ module (fast operations on arrays and matrices).
Comparison operators (``>``, ``==``, etc.) are supported too.  There
is no restriction on the complexity of the expressions, or on the
number of variables involved.

Another possible use of this module is the calculation of **partial 
derivatives** of mathematical functions.

Additional examples and information can be obtained with ``pydoc 
uncertainties`` after installation.

Please send feature requests, bug reports, or feedback to the author.

*Installation*: ``sudo easy_install uncertainties`` might work for you 
(this does not require any manual download, but requires setuptools_). 
For additional installation methods, see ``README.txt`` in the provided 
files.

*Version history* (main changes only):

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
''',
      
      keywords = ['error propagation', 'uncertainties',
                  'uncertainty calculations',
                  'standard deviation',
                  'derivatives', 'partial derivatives', 'differentiation'],
      
      classifiers = [
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
      py_modules = ['uncertainties']
      )


