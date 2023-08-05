#!/usr/bin/env python

import distutils.core

distutils.core.setup(
    name='uncertainties', version='1.5.4',
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
``uncertainties`` allows calculations such as (2 +/- 0.1)*2 = 4
+/- 0.2 to be performed transparently.  Much more complex mathematical
expressions involving numbers with uncertainties can also be evaluated
directly.

**Correlations** between expressions are correctly taken into account.
Thus, ``x-x`` is exactly zero, for instance (most implementations
found on the web yield a non-zero uncertainty for ``x-x``, which is
incorrect).

Whatever the complexity of the calculation, the number of steps
involved, or the correlations between variables, uncertainties
produced by this program are what is predicted by `error propagation
theory`_.

Basic examples::

    from uncertainties import ufloat
    from uncertainties.umath import *  # sin(), etc.

    x = ufloat((0.20, 0.01))  # x = 0.20+/-0.01
    x = ufloat("0.20+/-0.01")  # Other representation
    x = ufloat("0.20")  # Implicit uncertainty of +/-1 on the last digit    
    x = ufloat("0.20(1)")  # Other representation

    # Mathematical operations:
    print x**2  # Square: prints "0.04+/-0.004"
    print sin(x**2)  # Prints "0.0399...+/-0.00399..."

    # Access to the nominal value, and to the uncertainty:
    square = x**2  # Square
    print square  # Prints "0.04+/-0.004"  
    print square.nominal_value  # Prints "0.04"
    print square.std_dev()  # Prints "0.004..."

    print square.derivatives[x]  # Partial derivative: prints "0.4" (= 2*0.20)

    print square - x*x  # Exactly zero: correlations taken into account

    # Arrays (if NumPy is installed):
    from uncertainties import unumpy
    random_vars = unumpy.uarray(([1, 2], [0.1, 0.2]))  # [1+/-0.1 2+/-0.2]
    print random_vars.mean()  # Prints "1.5+/-0.11180..."
    print unumpy.cos(random_vars)  # [0.54...+/-0.08... -0.41...+/-0.18...]

The Python_ (or IPython_) shell can thus be used as **a powerful
calculator** that handles quantities with uncertainties (``print``
statements are optional, which is convenient).

**Almost all mathematical operations** are supported, including most
functions from the standard math_ module (sin,...), which can be found
in the ``uncertainties.umath`` module.  Comparison operators (``>``,
``==``, etc.) are supported too.  There is no restriction on the
complexity of mathematical expressions, or on the number of variables
involved (x-sin(x)+y**2-tan(y*x) can for example be calculated,
whether x and y are quantities with uncertainties or not).

Many **fast operations on arrays and matrices** of numbers with
uncertainties are supported, through the ``uncertainties.unumpy``
package and its ``unumpy.ulinalg`` sub-module, which extend NumPy_\'s
capabilities: cosine of all the elements of an array
(``unumpy.cos()``), matrix inverse and pseudo-inverse (through
``unumpy`` matrices), etc.

Another possible use of this module is the calculation of numerical
**partial derivatives** of mathematical functions (they are used by
`error propagation theory`_, and are thus automatically calculated by
this module). They are directly available in the ``derivatives``
attribute of numbers with uncertainties.

Additional **examples and information** can be obtained with ``pydoc
uncertainties`` and ``pydoc uncertainties.umath`` after installation.
Information on array operations is available through ``pydoc
uncertainties.unumpy`` and ``pydoc uncertainties.unumpy.ulinalg``.

**Installation or upgrade**: ``sudo easy_install -U uncertainties`` might be
sufficient, depending on your installation (this does not require any
manual download, but does require setuptools_).  For additional
installation methods, download the source archive, and see the
``README.txt`` file that it contains.

*User feedback*:

- "*A gift of the gods for the work I\'m doing*" (e-mail)
- "*Your package is brilliant and I love it.*" (e-mail)
- "*PyPI\'s uncertainties rocks!*" (identi.ca_)
- "*Holy f\*\*\* this would have saved me so much f\*\*\*ing time last\
 semester*." (reddit_)

Please send **feature requests, bug reports, or feedback** to
`Eric O. LEBIGOT (EOL)`_.

Please **support this program** and its future development by donating
$5 or more through PayPal_.

*Version history* (main changes only):

- 1.5.4: ``ufloat`` does not accept a single number (nominal value) anymore. \
       This removes some potential confusion about \
       ``ufloat(1.1)`` (zero uncertainty) being different from \
       ``ufloat("1.1")`` (uncertainty of 1 on the last digit).
- 1.5.2: ``float_u``, ``array_u`` and ``matrix_u`` renamed ``ufloat``, \
       ``uarray`` and ``umatrix``, for ease of typing.
- 1.5:  Added functions ``nominal_value`` and ``std_dev``, and \
       modules ``unumpy`` (additional support for NumPy_ arrays and \
       matrices) and ``unumpy.ulinalg`` (generalization of some \
       functions from ``numpy.linalg``). \
       Memory footprint of arrays of numbers with uncertainties \
       divided by 3. \
       Function ``array_u`` is 5 times faster. \
       Main function ``num_with_uncert`` renamed \
       ``float_u``, for consistency with ``unumpy.array_u`` and \
       ``unumpy.matrix_u``, with the added benefit of a shorter name.
- 1.4.5: Added support for the standard ``pickle`` module.
- 1.4.2: Added support for the standard ``copy`` module.
- 1.4: Added utilities for manipulating NumPy_ arrays of numbers with\
       uncertainties (``array_u``, ``nominal_values`` and ``std_devs``).
- 1.3: Numbers with uncertainties are now constructed with \
  ``num_with_uncert()``, which replaces ``NumberWithUncert()``.  This \
  simplifies the class hierarchy by removing the ``NumberWithUncert`` class.
- 1.2.5: Numbers with uncertainties can now be entered as \
         ``NumberWithUncert("1.23+/-0.45")`` too.
- 1.2.3: ``log(x, base)`` is now supported by ``umath.log()``, in addition \
         to ``log(x)``.
- 1.2.2: Values with uncertainties are now output like 3+/-1, in order \
         to avoid confusing 3+-1 with 3+(-1).
- 1.2: A new function, ``wrap()``, is exposed, which allows non-Python \
       functions (e.g. Fortran or C used through a module such as SciPy) to \
       handle numbers with uncertainties.
- 1.1: Mathematical functions (such as cosine, etc.) are in a new \
       uncertainties.umath module; \
       they do not override functions from the ``math`` module anymore.
- 1.0.12: Main class (``Number_with_uncert``) renamed ``NumberWithUncert`` \
          so as to follow `PEP 8`_.
- 1.0.11: ``origin_value`` renamed more appropriately as \
          ``nominal_value``.
- 1.0.9: ``correlations()`` renamed more appropriately as \
         ``covariance_matrix()``.

.. _Python: http://docs.python.org/tutorial/interpreter.html
.. _IPython: http://ipython.scipy.org/
.. _NumPy: http://numpy.scipy.org/
.. _math: http://docs.python.org/library/math.html
.. _PEP 8: http://www.python.org/dev/peps/pep-0008/
.. _error propagation theory: http://en.wikipedia.org/wiki/Propagation\
_of_uncertainty
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _Eric O. LEBIGOT (EOL): mailto:eric.lebigot@normalesup.org
.. _reddit: http://www.reddit.com/r/Python/comments/am84v/\
now_you_can_do_calculations_with_uncertainties_5/
.. _identi.ca: http://identi.ca/notice/23330742
.. _PayPal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4TK7KNDTEDT4S
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
    
    # Files are defined in MANIFEST
    packages=['uncertainties', 'uncertainties.unumpy']
    )  # End of setup definition
