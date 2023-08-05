from distutils.core import setup

setup(name = 'uncertainties', version = '1.0',
      author = 'Eric O. LEBIGOT (EOL)',
      author_email = 'eric.lebigot@normalesup.org',
      
      license = '''\
This software is released under the GNU General Public License version
2, for private or academic use (http://creativecommons.org/licenses/GPL/2.0/).
It is possible to use this software under another license (in particular
for commercial uses), which must then be obtained from the original author.''',
      
      description = ('Transparent calculations with quantities with'
                     ' uncertainties (aka "error propagation")'),
      
      long_description = '''\
``uncertainties`` allows calculation such as (0.2 +- 0.01)**2 = 0.04 +- 0.004
to be performed transparently.

Correlations between expressions are correctly taken into account (for instance,
with x=0.2+-0.01, ``2*x - x - x`` is *exactly* zero, as is ``y - x - x``
with ``y = 2*x``).

Examples::

    # Mathematical operations:
    x = uncertainties.Number_with_uncert((0.20, 0.01))  # x = 0.20+-0.01
    x = uncertainties.Number_with_uncert("0.20(1)")  # Other representation
    print x**2  # Prints "0.04+-0.004"
    print math.sin(x**2)  # Prints "0.0399...+-0.00399..."

    # Access to the value at the origin, to the uncertainty, and to derivatives:
    y = x**2
    print y  # Prints "0.04+-0.004"
    print y.origin_value  # Prints "0.04"
    print y.std_dev()  # Prints "0.004..."
    print y.derivatives[x]  # Partial derivative: prints "2"

Almost all mathematical operations are supported, including many from
the standard ``math`` module and from the third-party numpy_ module.

More information can be obtained with ``pydoc uncertainties``.

.. _numpy: http://numpy.scipy.org/
''',
      
      keywords = ('error propagation, uncertainties,'
                  ' uncertainty calculation, standard deviation, derivatives'),
      
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
      py_modules = ['uncertainties'],
      )


