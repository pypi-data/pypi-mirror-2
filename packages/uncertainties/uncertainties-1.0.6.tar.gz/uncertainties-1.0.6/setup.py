from distutils.core import setup

setup(name = 'uncertainties', version = '1.0.6',
      author = 'Eric O. LEBIGOT (EOL)',
      author_email = 'eric.lebigot@normalesup.org',
      
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

**Correlations** between expressions are correctly taken into account 
(``x-x`` is exactly zero, for instance).

Basic examples::

    # Mathematical operations:
    x = uncertainties.Number_with_uncert((0.20, 0.01))  # x = 0.20+-0.01
    x = uncertainties.Number_with_uncert("0.20(1)")  # Other representation
    print x**2  # Prints "0.04+-0.004"
    print math.sin(x**2)  # Prints "0.0399...+-0.00399..."

    # Access to the value at the origin, and to the uncertainty:
    y = x**2
    print y  # Prints "0.04+-0.004"
    print y.origin_value  # Prints "0.04"
    print y.std_dev()  # Prints "0.004..."

    print y.derivatives[x]  # Partial derivative: prints "2"

    print y - x*x  # Exactly zero: correlations taken into account

**Almost all mathematical operations** are supported, including most 
functions from the standard ``math`` module and functions from the 
third-party numpy_ module (fast operations on arrays and matrices).  
There is no restriction on the complexity of the expressions, or on the 
number of variables involved.

Another possible use of this module is the calculation of **partial 
derivatives** of mathematical functions.

More examples and additional information can be obtained with ``pydoc 
uncertainties`` after installation.

Please send feature requests, bug reports, or compliments to the author.

.. _numpy: http://numpy.scipy.org/
''',
      
      keywords = ('error propagation', 'uncertainties',
                  'uncertainty calculations',
                  'standard deviation',
                  'derivatives', 'partial derivatives', 'differentiation'),
      
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


