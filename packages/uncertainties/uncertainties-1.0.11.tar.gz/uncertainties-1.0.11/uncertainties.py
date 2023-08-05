#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Calculations with full error propagation for quantities with uncertainties.
Derivatives can also be calculated.

Example of possible calculation: (0.2 +- 0.01)**2 = 0.04 +- 0.004.

Correlations between expressions are correctly taken into account (for
instance, with x = 0.2 +- 0.01, "2*x - x - x" is exactly zero, as is
"y - x -x" with "y = 2*x").

Examples:

  # Mathematical operations:
  import math
  x = uncertainties.Number_with_uncert((0.20, 0.01))  # x = 0.20+-0.01
  x = uncertainties.Number_with_uncert("0.20(1)")  # Other representation
  print x**2  # Prints "0.04+-0.004"
  print math.sin(x**2)  # Prints "0.0399...+-0.00399..."

  print x.position_in_sigmas(0.17)  # Print "-3.0": deviation of -3 sigmas

  # Access to the nominal value, and to the uncertainty:
  s = x**2  # Square
  print s  # Prints "0.04+-0.004"  
  print s.nominal_value  # Prints "0.04"
  print s.std_dev()  # Prints "0.004..."

  print s.derivatives[x]  # Partial derivative: prints "0.4" (= 2*0.20)
  
  # Correlations:
  u = uncertainties.Number_with_uncert((1, 0.05), "u variable")  # Tag
  v = uncertainties.Number_with_uncert((10,  0.1),  "v variable")
  sum_value = u+v
  
  u.set_std_dev(0.1)  # Standard deviations can be updated on the fly
  print sum_value - u - v  # Prints "0.0" (exact result)

  # List of all sources of error:
  print sum_value  # Prints "11+-0.1414..."
  for (var, error) in sum_value.error_components().iteritems():
      print "%s: %f" % (var.tag, error)  # Individual error components

  # Covariance matrices:
  cov_matrix = uncertainties.covariance_matrix([u, v, sum_value])
  print cov_matrix  # 3x3 matrix

  # Correlated variables can be constructed from a covariance matrix, if
  # Numpy is available:
  (u2, v2, sum2) = uncertainties.correlated_values([1, 10, 11],
                                                   cov_matrix)
  print u2  # Value and uncertainty of u: correctly recovered (1+-0.1)
  print uncertainties.covariance_matrix([u2, v2, sum2])  # = cov_matrix

If "from math import ..." is used, it must be run after importing this 
module, since otherwise the imported math functions would not be 
redefined so as to handle uncertainties.

- The main class provided by this module is Number_with_uncert, which
represents numbers with uncertainties.  Number_with_uncert objects can
be used as if they were regular Python numbers.  The main attributes
and methods of Number_with_uncert objects are defined in the
documentation for Number_with_uncert (available through pydoc).

- Valid operations include basic mathematical functions (addition,...),
as well most operations from the standard math module (sin,...).

Logical operations (>, ==, etc.) are also supported.

Many operations on Numpy arrays are supported, including inverting a
matrix that contains numbers with uncertainties.

- Utility functions are provided: the covariance matrix between
functions can be calculated [covariance_matrix()], or used as input
for the definition of correlated quantities [correlated_values(),
defined only if the numpy module is available].

- Mathematical expressions involving numbers with uncertainties
(Number_with_uncert objects) generally return AffineScalarFunc
objects.  Their most useful attributes and methods are described in
the documentation for AffineScalarFunc (available through pydoc).

- Uncertainties represent the standard deviation of probability 
distributions.  Nominal values are normally contained within the region 
of highest probability (for Number_with_uncert objects, a good nominal 
value is thus the location of highest probability of the random 
variable, the median, the average, etc.).

Linear approximations of functions (around the nominal values) are used 
for the calculation of the standard deviation of mathematical 
expressions.  The nominal value of an expression is the expression 
evaluated at the nominal values of its variables.

The calculated standard deviations and nominal values are meaningful 
approximations as long as the functions involved have precise linear 
expansions in the region where the probability distribution of the 
variables involved is large (for instance, sin(0+-0.01) yields a 
meaningful result, but cos(0+-0.01) yields an approximate standard 
deviation of 0, which might not be precise enough for all applications).

Probability distributions (random variables and calculation results) are 
printed as:

  nominal value +- standard deviation

but this does not imply any property on the nominal value, or that the 
probability distribution of the result is symmetrical (this is rarely 
the case).

- Logical operations on Number_with_uncert objects have a pragmatic
semantics: Number_with_uncert objects can be used where Python numbers
are used, most of the time with identical results.  However, since
numbers with uncertainties represent random variables and not
constants, logical operations have their own semantics.  For instance:

  "x = 3.14; y = 3.14" is such that x == y

but

  x = Number_with_uncert((3.14, 0.01))
  y = Number_with_uncert((3.14, 0.01))

is not such that x == y, since x and y are independent random
variables.  However, x == x still holds.

More generally, the result of a logical operation ("==", ">", etc.) is
defined as being True only if the operation yields True for all
infinitesimal variations of its (random) variables, except for a
finite number of cases.  For instance 0+-0.1 != 0, because the random
variable 0+-0.1 almost always yields a non-zero value (even though it
can yield 0).

The boolean value (bool(x), "if x...") of a Number_with_uncert object
x is the result of "x != 0".

- This module should work with Python 2.5 and above.

- This module contains tests.  They can be run either manually or
automatically with the nose unit testing framework (nosetests).

- The author wishes to thank Arnaud Delobelle, Pierre Cladé, and
contributors to the comp.lang.python newsgroup for valuable input.

(c) 2009 by Eric O. LEBIGOT (EOL) <eric.lebigot@normalesup.org>
Please send feature requests, bug reports, or feedback to this address.

This software is released under a dual license.  (1) The GNU General
Public License version 2.  (2) Any other license, as long as it is
obtained from the original author.'''

# The idea behind this module is to replace the result of mathematical
# operations by a local approximation of the defining function.  For
# example, sin(0.2+-0.01) becomes the affine function
# (AffineScalarFunc object) whose nominal value is sin(0.2) and
# whose variations are given by sin(0.2+delta) = 0.98...*delta.
# Uncertainties can then be calculated by using this local linear
# approximation of the original function.

from __future__ import division  # Many analytical derivatives depend on this

import re
from math import sqrt
import math
import weakref
from types import BuiltinFunctionType

import random  # For unit testing (test_...() functions)

# Attributes that are always exported (some other attributes are
# exported only if the numpy module is available...):
__all__ = [
    
    'Number_with_uncert',  # Main class: number with uncertainty
    
    # Utility functions (more are exported if Numpy is present):
    'covariance_matrix',
    
    # Class returned by most operations: not typically created by
    # users, but possibly manipulated by outside code ['derivatives()'
    # method, etc.]:
    'AffineScalarFunc'
    
    ]

###############################################################################

# Mathematical operations with local approximations (affine scalar
# functions)

class NotFloatLikeType(Exception):
    pass

def to_affine_scalar(x):
    """
    Transforms x into a constant affine scalar function
    (AffineScalarFunc), unless it is already an AffineScalarFunc (in
    which case x is returned unchanged).

    Raises an exception unless 'x' belong to some specific classes of
    objects that are known not to depend on AffineScalarFunc objects
    (which then cannot be considered as constants).
    """

    if isinstance(x, AffineScalarFunc):
        return x

    #! Python 2.6's numbers.Number would help:
    if isinstance(x, (float, int, complex)):
        # No variable => no derivative to define:
        return AffineScalarFunc(x, {})
    else:
        raise NotFloatLikeType("%s is not a known 'constant'"
                               % type(x))

def partial_derivative(f, arg_num, step = 1e-5):
    """
    Returns a function that numerically calculates the partial
    derivative of function f with respect to its argument number
    arg_num.

    The function values must combine linearly for the result to have a
    meaning.    
    """

    def partial_derivative_of_f(*args):

        f_nominal_value = f(*args)

        shifted_args = list(args)
        shifted_args[arg_num] += step
        shifted_f = f(*shifted_args)

        return (shifted_f - f_nominal_value)/step

    return partial_derivative_of_f

class NumericalDerivatives(object):
  """
  Iteratable with the numerical derivatives of a function.
  """
  
  def __init__(self, function):
    """
    'function' is the function whose derivatives can be computed.
    """
    self._function = function

  def __getitem__(self, n):
      """
      Returns the n-th numerical derivative of the function.
      """
      return partial_derivative(self._function, n)
  
def local_approx(f, derivatives_funcs = None):
    """
    Wraps function 'f' so that, when applied to AffineScalarFunc
    objects or float-like arguments, 'f' returns a local approximation
    of its values (in the form of an object of class FuncWithError).
    In this case, if none of the arguments of 'f' involves variables
    [i.e. Variable objects], 'f' simply returns its usual result.

    When 'f' is not called on AffineScalarFunc or float-like
    arguments, the original result of 'f' is returned.

    If supplied, 'derivatives_funcs' is a list of functions that yield
    the partial derivatives of f.  If any of these functions is None,
    or if derivatives_funcs is None, then numerical derivatives are
    calculated.
    """

    if derivatives_funcs is None:
        derivatives_funcs = NumericalDerivatives(f)

    def f_with_affine_output(*args):

        # Can this function perform the calculation of an
        # AffineScalarFunc (or maybe float) result?
        try:
            aff_funcs = map(to_affine_scalar, args)

        except NotFloatLikeType:

            # This class does not now how to itself perform
            # calculations with non-float-like arguments (as they
            # might for instance be objects whose value really changes
            # if some Variable objects had different values):

            # Is it clear that we can't delegate the calculation?

            if any(isinstance(arg, AffineScalarFunc) for arg in args):
                # This situation arises for instance when calculating
                # AffineScalarFunc(...)*numpy.array(...).  In this
                # case, we must let numpy to handle the multiplication
                # (which is then performed element by element):
                return NotImplemented
            else:
                # If none of the arguments is an AffineScalarFunc, we
                # can delegate the calculation to the original
                # function.  This can be useful when it is called with
                # only one argument (as in
                # math.log10(numpy.ndarray(...)), when math.log10 was
                # redefined by numpy):
                return f(*args)

        ########################################
        # Nominal value of the constructed AffineScalarFunc:
        args_values = [e.nominal_value for e in aff_funcs]
        f_nominal_value = f(*args_values)

        ########################################

        # List of involved variables (Variable objects):
        variables = set()
        for expr in aff_funcs:
            variables |= set(expr.derivatives)

        ## It is sometimes useful to only return a regular constant:

        # (1) Optimization / convenience behavior: when 'f' is called
        # on purely constant values (e.g., sin(2)), there is no need
        # for returning a more complex AffineScalarFunc object.

        # (2) Functions that do not return a "float-like" value might
        # not have a relevant representation as an AffineScalarFunc.
        # This includes boolean functions, since their derivatives are
        # either 0 or are undefined: they are better represented as
        # Python constants than as constant AffineScalarFunc functions.

        if not variables or isinstance(f_nominal_value, bool):
            return f_nominal_value

        # The result of 'f' does depend on 'variables'...

        ########################################

        # Calculation of the derivatives with respect to the arguments
        # of f (aff_funcs):

        # The chain rule is applied.  This is because, in the case of
        # numerical derivatives, it allows for a better-controlled
        # numerical stability than numerically calculating the partial
        # derivatives through '[f(x + dx, y + dy, ...) -
        # f(x,y,...)]/da' where dx, dy,... are calculated by varying
        # 'a'.  In fact, it is numerically better to control how big
        # (dx, dy,...) are: 'f' is a simple mathematical function and
        # it is possible to know how precise the df/dx are (which is
        # not possible with the numerical df/da calculation above).

        # We use numerical derivatives, if we don't already have a
        # list of derivatives:

        #! Note that this test could be avoided by requiring the
        # caller to always provide derivatives.  When changing the
        # functions of the math module, this would force this module
        # to know about all the math functions.  Another possibility
        # would be to force derivatives_funcs to contain, say, the
        # first 3 derivatives of f.  But any of these two ideas has a
        # chance to break, one day... (if new functions are added to
        # the math module, or if some function has more than 3
        # arguments).

        derivatives_wrt_args = []
        for (arg, derivative) in zip(aff_funcs, derivatives_funcs):
            derivatives_wrt_args.append(derivative(*args_values)
                                        if arg.derivatives
                                        else 0)
                                

        ########################################
        # Calculation of the derivative of f with respect to all the
        # variables (Variable) involved.

        derivatives_wrt_vars = dict((var, 0.) for var in variables)

        # The chain rule is used (we already have
        # derivatives_wrt_args):

        for (func, f_derivative) in zip(aff_funcs, derivatives_wrt_args):
            for (var, func_derivative) in func.derivatives.iteritems():
                derivatives_wrt_vars[var] += (f_derivative
                                              * func_derivative)

        # The function now returns an AffineScalarFunc object:
        return AffineScalarFunc(f_nominal_value, derivatives_wrt_vars)

    # It is easier to work with f_with_affine_output, which represents
    # a wrapped version of 'f', when it bears the same name as 'f':
    f_with_affine_output.__name__ = f.__name__

    #! Setting the doc string after "def f_with...()" does not
    # seem to work.  We define it explicitly:
    f_with_affine_output.__doc__ = """\
Version of %s(...) that returns an affine approximation
(AffineScalarFunc object), if its result depends on variables
(Variable objects).  Otherwise, returns a simple constant (when
applied to constant arguments).

Warning: arguments of the function that are not AffineScalarFunc
objects must not depend on uncertainties.Variable objects in any
way.  Otherwise, the dependence of the result in
uncertainties.Variable objects will be incorrect.

Original documentation:
%s""" % (f.__name__, f.__doc__)

    return f_with_affine_output

class AffineScalarFunc(object):
    """
    Affine functions that support basic mathematical operations (*,
    -,...).  Such functions can for instance be used for representing
    the local (linear) behavior of any function.

    This class can also be used to represent constants.

    The variables of affine scalar functions are Variable objects.

    AffineScalarFunc objects include facilities for calculating the
    'error' on the function, from the uncertainty in its variables.

    Main attributes (with examples):
    
    - nominal_value, std_dev(): value at the origin / nominal value,
      and standard deviation.

    - error_components(): affineScalarFunc_object.error_components()[x]
      is the error on affineScalarFunc_object due to Variable x.

    - derivatives: affineScalarFunc_object.derivatives[x] is the
      (value of the) derivative with respect to Variable x.  This
      attribute is a dictionary whose keys are the Variable objects on
      which the function depends.
      
      All the Variable objects on which the function depends are in
      'derivatives'.

    - position_in_sigmas(x): position of number x with respect to the
      nominal value, in units of the standard deviation.
    """

    #! The code could be modify in order to accomodate for non-float
    # nominal values.  This could for instance be done through
    # the operator module: instead of delegating operations to
    # float.__*__ operations, they could be delegated to
    # operator.__*__ functions (while taking care of properly handling
    # reverse operations: __radd__, etc.).

    def __init__(self, nominal_value, derivatives):
        """
        'nominal_value' is the value of the function at the origin.
        
        'derivatives' maps each Variable object on which the function
        being defined depends to the value of the derivative with
        respect to that variable.

        'nominal_value' must not depend in any way of the Variable
        objects in 'derivatives' (the value at the origin of the
        function being defined is a constant).

        Warning: the above constraint is not checked, and the user is
        responsible for complying with it.
        """

        # Defines the value at the origin:

        #! There is no coercion to a float, here, because
        # AffineScalarFunc objects are also used for representing
        # constants of any type (in which case derivatives is empty:
        # there are no variables):
        self._nominal_value = nominal_value
        self.derivatives = derivatives

    @property
    def nominal_value(self):
        return self._nominal_value
    
    ############################################################

        
    ### Operators: operators applied to AffineScalarFunc and/or
    ### float-like objects only are supported.  This is why methods
    ### from float are used for implementing these operators.

    # Operators with no reflection:

    ########################################
        
    # __nonzero__() is supposed to return a boolean value (it is used
    # by bool()).  It is for instance used for converting the result
    # of comparison operators to a boolean, in sorted().  If we want
    # to be able to sort AffineScalarFunc objects, __nonzero__ cannot
    # return a AffineScalarFunc object.  Since boolean results (such
    # as the result of bool()) don't have a very meaningful
    # uncertainty, this should not be a big deal:
    def __nonzero__(self):
        #! This might not be relevant for AffineScalarFunc objects
        # that contain values in a linear space which does not convert
        # the float 0 into the null vector (see the __eq__ function:
        # __nonzero__ works fine if subtracting the 0 float from a
        # vector of the linear space works as if 0 were the null
        # vector of that space):
        return self != 0.  # Uses the AffineScalarFunc.__ne__ function

    ########################################
    
    ## Logical operators: warning: the resulting value cannot always
    ## be differentiated.

    # The logical operations are not differentiable everywhere, but
    # almost...

    # (1) I can rely on the assumption that the user only has "small"
    # errors on variables, as this is used in the calculation of the
    # standard deviation (which performs linear approximations):

    # (2) However, this assumption is not relevant for some
    # operations, and does not have to hold, in some cases.  This
    # comes from the fact that logical operations (e.g. __eq__(x,y))
    # are not differentiable for many usual cases.  For instance, it
    # is desirable to have u+-v == u+-v, whatever the size of v.
    # Furthermore, u+-v != u+-v', if v != v', whather the size of v or
    # v'.

    # (3) The result of logical operators does not have to be a
    # function with derivatives, as these derivatives are either 0 or
    # don't exist (i.e., the user should probably not rely on
    # derivatives for his code).
    
    def __eq__(self, y):
        difference = self - y
        #! "== 0" is not used, because it is less general than
        # not(bool(..)).  This can be useful if
        # difference._nominal_value is not a float (which could happen
        # in some version of this module), but some element in a
        # linear space.
        return not(difference._nominal_value or difference.std_dev())
    
    def __ne__(self, y):
        return not(self == y)

    def __gt__(self, y):
        return self._nominal_value > _get_nominal_value(y)

    def __ge__(self, y):
        if self > y:
            return True
        else:
            return self == y

    def __lt__(self, y):
        # __lt__ is not the opposite of __ge__: 3+-0.1 is neither
        # larger nor smaller than 3:
        return self._nominal_value < _get_nominal_value(y)

    def __le__(self, y):
        if self < y:
            return True
        else:
            return self == y

    ########################################

    # Uncertainties handling:
    
    def error_components(self):
        """
        Individual components of the standard deviation of the affine
        function (in absolute value), returned as a dictionary with
        Variable objects as keys.

        This method assumes that the derivatives contained in the
        object take scalar values (and are not a tuple, like what
        math.frexp() returns, for instance).
        """
    
        # Caculation of the variance:
        error_components = {}
        for (variable, derivative) in self.derivatives.iteritems():            
            # Individual standard error due to variable:
            error_components[variable] = abs(derivative*variable._std_dev)

        return error_components

    def std_dev(self):
        """
        Standard deviation of the affine function.

        This method assumes that the function returns scalar results.

        This returned standard deviation depends on the current
        standard deviations [std_dev()] of the variables (Variable
        objects) involved.
        """
        #! It would be possible to not allow the user to update the
        #std dev of Variable objects, in which case AffineScalarFunc
        #objects could have a pre-calculated or, better, cached
        #std_dev value (in fact, many intermediate AffineScalarFunc do
        #not need to have their std_dev calculated: only the final
        #AffineScalarFunc returned to the user does).
        return sqrt(sum(
            delta**2 for delta in self.error_components().itervalues()))

    def _general_representation(self, to_string):
        """
        Uses the to_string() conversion function on both the nominal
        value and the standard deviation, and returns a string that
        describes them.

        to_string() is typically repr() or str().
        """

        (nominal_value, std_dev) = (self._nominal_value, self.std_dev())

        # String representation:

        # Not putting spaces around "+-" helps with arrays of
        # Number_with_uncert, as each value with an uncertainty is a
        # block of signs (otherwise, the standard deviation can be
        # mistaken for another element of the array).

        return ("%s+-%s" % (to_string(nominal_value), to_string(std_dev))
                if std_dev
                else to_string(nominal_value))

    def __repr__(self):
        return self._general_representation(repr)
                    
    def __str__(self):
        return self._general_representation(str)

    def position_in_sigmas(self, value):
        """
        Returns 'value' - nominal value, in units of the standard
        deviation.

        Raises a ValueError exception if the standard deviation is zero.
        """
        try:
            # The ._nominal_value is a float: there is no integer division,
            # here:
            return (value - self._nominal_value) / self.std_dev()
        except ZeroDivisionError:
            raise ValueError("The standard deviation is zero:"
                             " undefined result.")


def get_ops_with_reflection():

    """
    Returns operators with a reflection, along with their derivatives
    (for float operands).
    """
    
    # Operators with a reflection:

    # We do not include divmod().  This operator could be included, by
    # allowing its result (a tuple) to be differentiated, in
    # derivative_value().  However, a similar result can be achieved
    # by the user by calculating separately the division and the
    # result.

    # {operator(x, y): (derivative wrt x, derivative wrt y)}:

    # Note that unknown partical derivatives can be numerically
    # calculated by expressing them as something like
    # "partial_derivative(float.__...__, 1)(x, y)":
    derivatives_list = {
        'add': ("1.", "1."),
        # 'div' is the '/' operator when __future__.division is not in
        # effect.  Since '/' is applied to
        # AffineScalarFunc._nominal_value numbers, it is applied on
        # floats, and is therefore the "usual" mathematical division.
        'div': ("1/y", "-x/y**2"),
        'floordiv': ("0.", "0."),  # Non exact: there a discontinuities
        # The derivative wrt the 2nd arguments is something like (..., x//y),
        # but it is calculated numerically, for convenience:
        'mod': ("1.", "partial_derivative(float.__mod__, 1)(x, y)"),
        'mul': ("y", "x"),
        'pow': ("y*x**(y-1)", "math.log(x)*x**y"),
        'sub': ("1.", "-1."),
        'truediv': ("1/y", "-x/y**2")
        }

    # Conversion to Python functions:
    ops_with_reflection = {}
    for (op, derivatives) in derivatives_list.iteritems():
        ops_with_reflection[op] = [
            eval("lambda x, y: %s" % expr) for expr in derivatives ]

        ops_with_reflection["r"+op] = [
            eval("lambda y, x: %s" % expr) for expr in reversed(derivatives)]

    return ops_with_reflection

# Operators that have a reflexion, along with their derivatives:
_ops_with_reflection = get_ops_with_reflection()

# Some effectively modified operators (for test purposes):
_modified_operators = []

def add_operators_to_AffineScalarFunc():
    """
    Adds many operators (__add__, etc.) to the AffineScalarFunc class.
    """
    
    ########################################

    #! Derivatives are set to return floats.  For one thing,
    # uncertainties generally involve floats, as they are based on
    # small variations of the parameters.  It is also better to
    # protect the user from unexpected integer result that behave
    # badly with the division.

    ## Operators that return a numerical value:

    # Single-argument operators that should be adapted from floats to
    # AffineScalarFunc objects:
    simple_numerical_operators_derivatives = {
        'abs': lambda x: 1. if x>=0 else -1.,
        'neg': lambda x: -1.,
        'pos': lambda x: 1.,
        'trunc': lambda x: 0.
        }

    for (op, derivative) in \
          simple_numerical_operators_derivatives.iteritems():
        
        attribute_name = "__%s__" % op
        # float objects don't exactly have the same attributes between
        # different versions of Python (for instance, __trunc__ was
        # introduced with Python 2.6):
        if attribute_name in dir(float):
            setattr(AffineScalarFunc, attribute_name,
                    local_approx(getattr(float, attribute_name),
                                 [derivative]))
            _modified_operators.append(op)
            
    ########################################

    # Reversed versions (useful for float*AffineScalarFunc, for instance):
    for (op, derivatives) in _ops_with_reflection.iteritems():
        attribute_name = '__%s__' % op
        setattr(AffineScalarFunc, attribute_name,
                local_approx(getattr(float, attribute_name), derivatives))

    ########################################
    # Conversions to pure numbers are meaningless.  Note that the
    # behavior of float(1j) is similar.
    for coercion_type in ('complex', 'int', 'long', 'float'):
        def raise_error(self):
            raise TypeError("can't convert an affine function (%s)"
                            ' to %s; use x.nominal_value'
                            # In case AffineScalarFunc is sub-classed:
                            % (self.__class__, coercion_type))

        setattr(AffineScalarFunc, '__%s__' % coercion_type, raise_error)

add_operators_to_AffineScalarFunc()  # Actual addition of class attributes

# Test of correctness of the fixed (usually analytical) derivatives:
def test_fixed_derivatives_basic_funcs():
    """
    Pre-calculated derivatives for operations on AffineScalarFunc.
    """

    def check_op(op, num_args):
        """
        Makes sure that the derivatives for function '__op__' of class
        AffineScalarFunc, which takes num_args arguments, are correct.

        If num_args is None, a correct value is calculated.
        """

        op_string = "__%s__" % op
        # print "Checking %s..." % op_string
        func = getattr(AffineScalarFunc, op_string)
        numerical_derivatives = NumericalDerivatives(
            lambda *args: func(*args).nominal_value)
        _compare_derivatives(op, func, numerical_derivatives, num_args)

    # Operators that take 1 value:
    for op in _modified_operators:
        check_op(op, 1)

    # Operators that take 2 values:
    for op in _ops_with_reflection.keys():
        check_op(op, 2)


class Variable(AffineScalarFunc):    
    """
    Representation of a float-like scalar random variable, along with
    its uncertainty.
    """
    
    def __init__(self, value, std_dev = 0, tag = None):
        """
        The nominal value and the standard deviation of the variable
        are set.  These values must scalars.

        'tag' is a tag that the user can associate to the variable.  This
        is useful for tracing variables.

        The notion of nominal value is described in the main module
        documentation.        
        """

        # If the variable changes by dx, then the value of the affine
        # function that gives its value changes by 1*dx:

        assert isinstance(value, (int, float)), (
            "Variable objects can only have a float-like "
            " value.  Got type %s." % type(value))

        # Only float-like values are handled.  One reason is that the
        # division operator on integers would not produce a
        # differentiable functions: for instance, Variable(3, 0.1)/2
        # has a nominal value of 3/2 = 1, but a "shifted" value
        # of 3.1/2 = 1.55.
        value = float(value)

        super(Variable, self).__init__(value,
                                       # We avoid memory circles:
                                       weakref.WeakKeyDictionary({self: 1.})
                                       )

        # We force the error to be float-like.  Since it is considered
        # as a Gaussian standard deviation, it is semantically
        # positive (even though there would be no problem defining it
        # as a sigma, where sigma can be negative and still define a
        # Gaussian):

        assert std_dev >= 0, "the error must be a positive number"
        # Since AffineScalarFunc.std_dev is a property, we cannot do
        # "self.std_dev = ...":
        self._std_dev = std_dev
        
        self.tag = tag

    # Standard deviations can be modified (this is a feature).
    # AffineScalarFunc objects that depend on the Variable have their
    # std_dev() automatically modified (recalculated with the new
    # std_dev of their Variables):
    def set_std_dev(self, value):
        """
        Updates the standard deviation of the variable to a new value.
        """
        self._std_dev = value

    # The following method is overridden so that we can represent the tag:
    def _general_representation(self, to_string):
        """
        Uses the to_string() conversion function on both the nominal
        value and standard deviation and returns a string that
        describes the number.

        to_string() is typically repr() or str().
        """
        num_repr  = super(Variable, self)._general_representation(to_string)
        
        # Optional tag: only full representations (to_string == repr)
        # contain the tag, as the tag is required in order to recreate
        # the variable.  Outputing the tag for regular string ("print
        # x") would be too heavy and produce an unusual representation
        # of a number with uncertainty.
        return (num_repr if ((self.tag is None) or (to_string != repr))
                else "< %s = %s >" % (self.tag, num_repr))

###############################################################################

# Utilities for unit testing

def _numbers_close(x, y, tolerance = 1e-6):
    """
    Returns True if the numbers are close enough.

    The given tolerance is the relative difference allowed, or the absolute
    difference, if one of the numbers is 0.
    """

    # Instead of using a try and ZeroDivisionError, we do a test,
    # NaN could appear silently:

    if x != 0 and y != 0:
        return abs(1-y/x) < tolerance
    else:
        if x == 0:
            return abs(y) < tolerance
        else:
            return abs(x) < tolerance

class DerivativesDiffer(Exception):
    pass

def _compare_derivatives(name, func, numerical_derivatives,
                         num_args = None):
    """
    Checks the derivatives of a function 'func' (as returned by the
    local_approx() wrapper), by comparing them to the
    'numerical_derivatives' functions.

    Raises a DerivativesDiffer exception in case of problem.
    
    These functions all take the same number of arguments: num_args.
    If num_args is None, it is automatically obtained.

    Tests are done on random arguments.
    """

    # Detecting automatically the correct number of arguments is not
    # always easy (because not all values are allowed, etc.):

    num_args_table = {
        'atanh': 1,
        }
    if func.__name__ in num_args_table:
        num_args = num_args_table[func.__name__]
    else:

        # We determine the number of arguments for 'func':
        if num_args is None:

            # We get the number of arguments by trial and error:
            for num_args in range(10):
                try:
                    #! Giving integer arguments is good for preventing
                    # certain functions from failing even though num_args
                    # is their correct number of arguments
                    # (e.g. math.ldexp(x, i), where i must be an integer)
                    func(*(1,)*num_args)
                except TypeError:
                    pass  # Not enough arguments
                else:  # No error
                    break  # num_args is a good number of arguments for func
            else:
                raise Exception("Can't find a reasonable number of arguments"
                                " for function '%s'." % name)

    # We loop until we find reasonable function arguments:

    # Argument numbers that will have a random integer value:
    integer_arg_nums = set()
    while True:
        try:

            # We include negative numbers, for more thorough tests:
            args = [
                random.choice(range(-10, 10)) if arg_num in integer_arg_nums
                else Variable(random.random()*10-5, 0)
            for arg_num in range(num_args)]

            func_approx = func(*args)

            # Some functions are simple Python constants, after
            # wrapping in local_approx(): no test has to be performed:
            if isinstance(func_approx, AffineScalarFunc):

                # We compare all derivatives:
                for (arg_num, (arg, numerical_deriv)) in \
                      enumerate(zip(args, numerical_derivatives)):

                    # Some arguments might not be differentiable:
                    if isinstance(arg, int):
                        continue

                    fixed_deriv_value = func_approx.derivatives[arg]
                    num_deriv_value = numerical_deriv(*args)

                    if not _numbers_close(fixed_deriv_value,
                                          num_deriv_value, 1e-4):

                        # It is possible that the result is nan:
                        #! Python 2.6: this would be math.isnan(func_approx):
                        if func_approx == func_approx:
                            raise DerivativesDiffer(
                                "Derivative #%d of function '%s' may be wrong:"
                                " at args = %s, fixed val = %f,"
                                " while num. val = %f"
                                % (arg_num, name, args,
                                   fixed_deriv_value, num_deriv_value))

        except ValueError, err:  # Arguments out of range, or of wrong type
            # Factorial(real) lands here:
            if str(err).startswith('factorial'):
                integer_arg_nums = set([0])
            continue  # We try with different arguments
        # Some arguments might have to be integers, for instance:
        except TypeError:
            if len(integer_arg_nums) == num_args:
                raise Exception("Incorrect testing procedure: unable to "
                                "find correct argument values for %s."
                                % func.__name__)

            # Another argument might be forced to be an integer:
            integer_arg_nums.add(random.choice(range(num_args)))
        else:
            # We have found reasonable arguments, and the test passed:
            break



###############################################################################

# Utilities

def _get_nominal_value(n):
    """
    Returns the nominal value of n if it is a Number_with_uncert
    object, or simply the value of n, if n is not a
    Number_with_uncert.

    This utility function is useful for transforming a series of
    numbers, some of which might carry an uncertainty (i.e., be
    AffineScalarFunc objects).
    """

    return n.nominal_value if isinstance(n, AffineScalarFunc) else n

def covariance_matrix(expressions):
    """
    Returns a matrix that contains the covariances between the given
    AffineScalarFunc objects (iterable).  They must be ordered in some
    way (list, tuple,...), as the resulting matrix implicitly depends
    on their ordering.

    The covariances are floats (never int objects).
    """
    # See PSI.411.

    covariance_matrix = []
    for (i1, expr1) in enumerate(expressions):
        derivatives1 = expr1.derivatives  # Optimization
        vars1 = set(derivatives1)
        coefs_expr1 = []
        for (i2, expr2) in enumerate(expressions[:i1+1]):
            derivatives2 = expr2.derivatives  # Optimization
            coef = 0.
            for var in vars1.intersection(expr2.derivatives):
                # var is a variable common to both expressions:
                coef += (derivatives1[var]*derivatives2[var]*var._std_dev**2)
            coefs_expr1.append(coef)
        covariance_matrix.append(coefs_expr1)

    # We symmetrize the matrix:
    for (i, covariance_coefs) in enumerate(covariance_matrix):
        covariance_coefs.extend(covariance_matrix[j][i]
                                 for j in range(i+1, len(covariance_matrix)))

    return covariance_matrix

# Entering variables as a block of correlated values.  Only available
# if Numpy is installed.

#! It would be possible to dispense with Numpy, but a routine should be
# written for obtaining the eigenvectors of a symmetric matrix.  See
# for instance Numerical Recipes: (1) reduction to tri-diagonal
# [Givens or Householder]; (2) QR / QL decomposition.

try:
    from numpy import linalg
except ImportError:
    pass
else:

    def _repr_dot(coefs, tags):
        """
        Represents a 'linear combination' of the strings from 'tags'
        with the given values.

        Both iterables must be of the same length.
        """
        # Parenthesis are here for negative coefficients:
        return '+'.join("(%r*%s)" % (c, t) for (c, t) in zip(coefs, tags))
    
    def correlated_values(values, covariance_mat, tags = None):
        """
        Returns AffineScalarFunc objects that correctly reproduce the
        given covariance matrix, and have the given values as their
        nominal value.

        The list of values and the covariance matrix must have the
        same length, and the matrix must be a square (symmetric) one.

        The affine functions returned depend on newly created,
        independent variables (Variable objects).

        If 'tags' is not None, it must list the tag of each new
        independent variable.
        """

        # If no tags were given, we prepare tags for the newly created
        # variables:
        if tags is None:
            tags = (None,) * len(values)

        # The covariance matrix is diagonalized in order to define
        # the independent variables that model the given values:

        (variances, transform) = linalg.eigh(covariance_mat)

        # Numerical errors might make some variances negative: we set
        # them to zero:
        variances[variances < 0] = 0.
        
        # Creation of new, independent variables:

        # We use the fact that the eigenvectors in 'transform' are
        # special: 'transform' is unitary: its inverse is its transpose:

        variables = tuple(
            # The variables represent uncertainties only:
            Variable(0, sqrt(variance), tag)
            for (variance, tag) in zip(variances, tags))

        # Representation of the initial correlated values:
        values_funcs = tuple(
            AffineScalarFunc(value, dict(zip(variables, coords)))
            for (coords, value) in zip(transform, values))

        return values_funcs

    __all__.append('correlated_values')
    
###############################################################################

# Some functions from the math module cannot be simply adapted to work
# with AffineScalarFunc objects (either as their result or as their
# arguments):

# (1) Some functions return a result of a type whose value and
# variations (uncertainties) cannot be represented by AffineScalarFunc
# (e.g., math.frexp, which returns a tuple).  The exception raised
# when not wrapping them with local_approx() is more obvious than the
# one obtained when wrapping them (in fact, the wrapped functions
# attempts operations that are not supported, such as calculation a
# subtraction on a result of type tuple).

# (2) Some functions don't take scalar arguments (which can be varied
# during differentiation): math.fsum...  Such functions can either be:

# - wrapped in a special way in wrap_math_functions()

# - excluded from wrapping by adding their name to _no_wrapping

# - wrapped in a general way in wrap_math_functions(); in this case,
# the function does not have to be mentioned in any location in this
# code.  The function should function normally, except possibly when
# given AffineScalarFunc arguments.

_no_wrapping = ['frexp', 'modf']

_wrapped_math_funcs = []  # Effectively wrapped math functions

def wrap_math_functions():
    """
    Wraps functions from the math module.
    """

    # Special cases:

    if 'fsum' in dir(math):  # Introduced in Python 2.6

        # fsum takes a single argument, which cannot be differentiated.
        # However, each of the arguments inside this single list can
        # be a variable.  We handle this in a specific way:

        def copy_elements(element):
            """
            Returns an iterator that returns the given element
            indefinitely.
            """
            while True:
                yield element

        # The fsum function is flattened, in order to go through the
        # local_approx() wrapper:
        original_func = math.fsum  # "Copy": in order to avoid recursion
        
        flat_fsum = lambda *args: original_func(args)
        flat_fsum.__doc__ = original_func.__doc__
        flat_fsum.__name__ = original_func.__name__
        
        flat_fsum_local_approx = local_approx(flat_fsum,
                                              copy_elements(lambda *args: 1))
        
        math.fsum = lambda arg_list: flat_fsum_local_approx(*arg_list)
        math.fsum.__doc__ = flat_fsum_local_approx.__doc__
        
        _no_wrapping.append('fsum')  # Wrapping already done

    # Wrapping of functions not in _no_wrapping:

    # Fixed formulas for the derivatives of some functions from the math
    # module (some functions might not be present in all version of
    # Python).  Singular points are not taken into account.  The user
    # should never give "large" uncertainties: problems could only appear
    # if this assumption does not hold.

    # Functions not mentioned in _fixed_derivatives have their derivatives
    # calculated numerically.

    # Functions that have singularities (possibly at infinity) benefit
    # from analytical calculations (instead of the default numerical
    # calculation).  Even slowly varying functions (e.g., abs()) yield
    # more precise results when differentiated analytically, because of
    # the loss of precision in numerical calculations.

    _fixed_derivatives = {
        # In alphabetical order, here:
        'acos': [lambda x: -1/math.sqrt(1-x**2)],
        'acosh': [lambda x: 1/math.sqrt(x**2-1)],
        'asin': [lambda x: 1/math.sqrt(1-x**2)],
        'asinh': [lambda x: 1/math.sqrt(1+x**2)],
        'atan': [lambda x: 1/(1+x**2)],
        'atan2': [lambda y, x: x/(x**2+y**2),  # Correct for x == 0
                  lambda y, x: -y/(x**2+y**2)],  # Correct for x == 0
        'atanh': [lambda x: 1/(1-x**2)],
        'ceil': [lambda x: 0],
        'copysign': [lambda x, y: (1 if x >= 0 else -1) * math.copysign(1, y),
                     lambda x, y: 0],
        'cos': [lambda x: -math.sin(x)],
        'cosh': [math.sinh],
        'degrees': [lambda x: math.degrees(1)],
        'exp': [math.exp],
        'fabs': [lambda x: 1 if x >= 0 else -1],
        'floor': [lambda x: 0],
        'hypot': [lambda x, y: x/math.hypot(x, y),
                  lambda x, y: y/math.hypot(x, y)],
        'ldexp': [lambda x, y: 2**y,
                  # math.ldexp only accepts an integer as its second
                  # argument:
                  None],
        'log': [lambda x: 1/x],
        'log10': [lambda x: 1/x/math.log(10)],
        'log1p': [lambda x: 1/(1+x)],
        'pow': [lambda x, y: y*math.pow(x, y-1),
                lambda x, y: math.log(x) * math.pow(x, y)],
        'radians': [lambda x: math.radians(1)],
        'sin': [math.cos],
        'sinh': [math.cosh],
        'sqrt': [lambda x: 0.5/math.sqrt(x)],
        'tan': [lambda x: 1+math.tan(x)**2],
        'tanh': [lambda x: 1-math.tanh(x)**2]
        }

    
    for name in set(dir(math)).difference(_no_wrapping):
        obj = getattr(math, name)
        if isinstance(obj, BuiltinFunctionType):
            if name in _fixed_derivatives:
                derivatives = _fixed_derivatives[name]
            else:
                derivatives = None
            setattr(math, name, local_approx(obj, derivatives))
            _wrapped_math_funcs.append(name)
            
# We wrap the functions from the math module so that they keep track of
# uncertainties by returning a AffineScalarFunc object:
wrap_math_functions()

def test_fixed_derivatives_math_funcs():
    """
    Check of wrapped functions from the math module.
    """

    for name in _wrapped_math_funcs:
        # print "Checking %s..." % name
        func = getattr(math, name)
        numerical_derivatives = NumericalDerivatives(
            lambda *args: func(*args).nominal_value)            
        _compare_derivatives(name, func, numerical_derivatives)


###############################################################################
# Parsing of values with uncertainties:

POSITIVE_FLOAT_UNSIGNED = r'(\d+)(\.\d*)?'

# Regexp for a number with uncertainty (e.g., "-1.234(2)e-6"), where the
# uncertainty is optional (in which case the uncertainty is implicit):
NUMBER_WITH_UNCERT_RE_STR = '''
    ([+-])?  # Sign
    %s  # Main number
    (?:\(%s\))?  # Optional uncertainty
    ([eE][+-]?\d+)?  # Optional exponent
    ''' % (POSITIVE_FLOAT_UNSIGNED, POSITIVE_FLOAT_UNSIGNED)

NUMBER_WITH_UNCERT_RE = re.compile(
    "^%s$" % NUMBER_WITH_UNCERT_RE_STR, re.VERBOSE)

# The following function is not exposed because it can in effect be
# obtained by doing x = Number_with_uncert(representation) and
# x.nominal_value and x.std_dev():
def str_to_number_with_uncert(representation):
    """
    Given a string that represents a number with uncertainty, returns the
    central value and the uncertainty.

    When no error is given, an uncertainty of 1 on the last digit is implied.
    """

    match = NUMBER_WITH_UNCERT_RE.search(representation)

    if match:
        # The 'main' part is the central value, with 'int'eger part, and
        # 'dec'imal part.  The 'uncert'ainty is similarly broken into its
        # integer and decimal parts.
        (sign, main_int, main_dec, uncert_int, uncert_dec,
         exponent) = match.groups()
    else:
        raise Exception("Unparsable number representation: '%s'."
                        % representation)

    # The value of the number is its central value:
    value = float("%s%s%s%s" % (sign or '',
                                main_int,
                                main_dec or '.0',
                                exponent or ''))
    
    if uncert_int is None:
        # No uncertainty was found: an uncertainty of 1 on the last
        # digit is assumed:
        uncert_int = "1"

    # Do we have a fully explicit uncertainty?
    if uncert_dec is not None:
        uncert = float("%s%s" % (uncert_int, uncert_dec or '.0'))
    else:
        # uncert_int represents an uncertainty on the last digits:
        abs_value_string = "%s%s" % (main_int, main_dec) \
                           if main_dec \
                           else main_int
        # We replace the digits that are known by zeroes:
        fixed_value = abs_value_string[:-len(uncert_int)]
        fixed_value = re.sub(r'\d', '0', fixed_value)
        # The last digits of the uncertainty are known:
        uncert = float("%s%s" % (fixed_value, uncert_int))

    # We apply the exponent to the uncertainty as well:
    uncert *= float("1%s" % (exponent or ''))

    return (value, uncert)


class Number_with_uncert(Variable):
    """
    Random variable object, with added support for string
    representation of numbers with errors.

    Main attributes and methods:
    - nominal_value and std_dev(): nominal value, and standard deviation
    - set_std_dev(),
    - tag: variable name or tag,
    
    Inherited from the AffineScalarFunc class:
    - error_components()
    - derivatives
    - position_in_sigmas()

    The notion of nominal value is described in the main module
    documentation.
    """

    def __init__(self, representation, tag = None):
        """
        Converts the representation of a number into a number with
        uncertainty (a random variable, defined by a nominal value and
        a standard deviation).

        The representation can be a string.  In this case, it will be
        parsed by str_to_number_with_uncert(): '12.345(15)',...

        The representation can also be a (value, uncertainty) pair, or a
        simple value number (in which case a zero uncertainty is implied).

        'tag' is an optional string tag for the variable.  Variables
        don't have to have distinct tags.  Tags are useful for tracing
        what values (and errors) enter in a given result (through the
        error_components() method).

        Examples of valid representations:

            -1.23(3.4)
            -1.34(5)
            1(6)
            3(4.2)
            -9(2)
            1234567(1.2)
            12.345(15)
            -12.3456(78)e-6
            0.29
            31.
            -31.
            31
            -3.1e10
            169.0(7)
        """

        # We create the correct tuple of arguments 'init_args' for the
        # Variable initialization.

        if isinstance(representation, tuple):
            init_args = representation
        #! Different, in Python 3:
        elif isinstance(representation, (str, unicode)):
            init_args = str_to_number_with_uncert(representation)
        else:
            # Case of a single float, etc.:
            init_args = (representation,)

        #! The tag is forced to be a string, so that the user does not
        # create a Number_with_uncert(2.5, 0.5) in order to represent 2.5
        # +- 0.5.  Forcing 'tag' to be a string prevents errors from being
        # considered as tags, here:

        #! 'unicode' is removed in Python3:
        if tag is not None:
            assert ((type(tag) is str) or (type(tag) is unicode)), \
                   "The tag can only be a string."

        #! init_args must contain all arguments:
        super(Number_with_uncert, self).__init__(*init_args, **{'tag': tag})

        ####################

        #!! __str__ could also be modified to give a nice representation
        # of the number with error ("1.234(4)").

###############################################################################

try:
    import numpy
except ImportError:
    pass
else:

    _matrix_nominal_values = numpy.vectorize(_get_nominal_value)

    def derivative(n, var):
        """
        Returns the derivative of n along var, if n is an
        AffineScalarFunc instance, and if var is one of the variables
        on which it depends.  Otherwise, return 0.
        """
        if isinstance(n, AffineScalarFunc):
            try:
                return n.derivatives[var]
            except KeyError:
                return 0.
        else:
            return 0.

    # numpy.matrix.getI is OK too, but the rest of the code assumes
    # that numpy.matrix.I is a property object anyway.
    __original_matrix_inv = numpy.matrix.I.fget
    
    def _inv_matrix(m):
      """
      Inverts a numpy.matrix object, even if m contains
      uncertainties.AffineScalarFunc() objects.  This is a wrapper
      around the original numpy.matrix.I property.

      As of Numpy 1.3.0, the .I property does not work on matrices
      that contain AffineScalarFunc objects.
      """

      if m.dtype != 'object':
          # Numerical calculations can be done directly:
          return __original_matrix_inv(m)

      # The algorithm consists in numerically calculating the derivatives
      # of the Numpy matrix inverse function (which should be numerically
      # stable):

      # Variables on which the matrix depend are collected:
      variables = set()
      for element in m.flat:
          # floats, etc. might be present
          if isinstance(element, AffineScalarFunc):
              variables |= set(element.derivatives.iterkeys())

      # Inverse without uncertainties:
      m_nominal_value = _matrix_nominal_values(m)
      inv_nominal_value = __original_matrix_inv(m_nominal_value)

      # Calculation of the derivatives of each element with respect to
      # the variables:
      derivatives = numpy.vectorize(lambda _: {})(m)
      for var in variables:
          
          # The variable standard deviations are supposed to be "small":

          # The std dev might be 0:
          if var._std_dev:
              shift_var = var._std_dev/100.
          else:
              shift_var = 1e-5
          
          # Shift of all the elements of m when var changes by shift_var:
          shift_m = numpy.vectorize(lambda n: derivative(n, var))(m)*shift_var
          
          # Origin value of matrix m when var is shifted by shift_var:
          shifted_m_values = m_nominal_value + shift_m

          inv_shifted = __original_matrix_inv(shifted_m_values)

          numerical_deriv = ((inv_shifted - inv_nominal_value)
                             / shift_var)

          # Update of the list of variables and associated
          # derivatives, for each element:
          for (derivative_list, derivative_value) in zip(derivatives.flat,
                                                         numerical_deriv.flat):
              if derivative_value:
                  derivative_list[var] = derivative_value
              
      # Numbers with uncertainties are build from the result:      
      inverse = numpy.vectorize(AffineScalarFunc)(inv_nominal_value,
                                                  derivatives)

      return inverse

    # We redefine Numpy's matrix inverse:
    
    #! For Python >= 2.6: simpler way:
    #   numpy.matrix.I = numpy.matrix.I.getter(_inv_matrix)
    numpy.matrix.I = property(_inv_matrix, numpy.matrix.I.fget,
                              numpy.matrix.I.fdel, numpy.matrix.I.__doc__)
    
###############################################################################

# Additional, more complex checks, for use with the nose unit testing
# framework.

def test_int_div():
    "Integer division"
    # We perform all operations on floats, because derivatives can
    # otherwise be meaningless:
    x = Number_with_uncert((3.9, 2))//2
    assert x.nominal_value == 1.
    # All errors are supposed to be small, so the Number_with_uncert()
    # in x violates the assumption.  Therefore, the following is
    # correct:
    assert x.std_dev() == 0.0

def test_comparison_ops():
    "Comparison operators"

    from math import tan, sin, cos
    import random
    
    # Operations on quantities equivalent to Python numbers must still
    # be correct:
    a = Number_with_uncert((-3, 0))
    b = Number_with_uncert((10, 0))
    c = Number_with_uncert((10, 0))
    assert a < b
    assert a < 3
    assert 3 < b  # This is first given to int.__lt__()
    assert b == c

    x = Number_with_uncert((3, 0.1))
    
    # One constraint is that usual Python code for inequality testing
    # still work in a reasonable way (for instance, it is generally
    # desirable that functions defined by different formulas on
    # different intervals can still do "if 0 < x < 1:...".  This
    # supposes again that errors are "small" (as for the esimate of
    # the standard error).
    assert x > 1

    # The limit case is not obvious:
    assert not(x >= 3)
    assert not(x < 3)

    assert x == x
    # Comparaison between Number_with_uncert and AffineScalarFunc:
    assert x == x + 0
    # Comparaison between 2 _different_ AffineScalarFunc objects
    # representing the same value:
    assert x/2 == x/2
    # With uncorrelated result that have the same behavior (value and
    # standard error):
    assert 2*Number_with_uncert((1, 0.1)) != Number_with_uncert((2, 0.2))    
    # Comparaison between 2 _different_ Number_with_uncert objects
    # that are uncorrelated:
    assert x != Number_with_uncert((3, 0.1))
    
    assert x != Number_with_uncert((3, 0.2))

    # More complicated, and prone to numerical errors (but not much
    # more than floats):
    assert tan(x) == sin(x)/cos(x)

    
    ####################
    
    # Checks of the semantics of logical operations: they return True
    # iff they are always True when the parameters vary in an
    # infinitesimal interval inside sigma (sigma == 0 is a special
    # case):

    def test_all_comparison_ops(x, y):
        """
        Takes two Number_with_uncert objects.
        
        Fails if any comparison operation fails to follow the proper
        semantics: a comparison returns True iff the correspond float
        comparison results are True for all the float values taken by
        the variables (of x and y) when they vary in an infinitesimal
        neighborhood within their uncertainty.
        """

        def random_float(var):
            """
            Returns a random value for Variable var, in an
            infinitesimal interval withing its uncertainty.  The case
            of a zero uncertainty is special.
            """
            return ((random.random()-0.5) * min(var.std_dev(), 1e-5)
                    + var.nominal_value)

        # All operations are tested:
        for op in ("__%s__" % name
                   for name in('ne', 'eq', 'lt', 'le', 'gt', 'ge')):

            float_func = getattr(float, op)
            
            # Determination of the correct truth value of func(x, y):

            sampled_results = []
            
            # The "main" value is an important particular case, and
            # the starting value for the final result
            # (correct_result):

            sampled_results.append(float_func(x.nominal_value, y.nominal_value))

            for check_num in range(50):  # Many points checked
                sampled_results.append(float_func(random_float(x),
                                                  random_float(y)))

            min_result = min(sampled_results)
            max_result = max(sampled_results)

            if min_result == max_result:
                correct_result = min_result
            else:

                # Almost all results must be True, for the final value
                # to be True:
                num_min_result = sampled_results.count(min_result)

                # 1 exception is considered OK:
                correct_result = (num_min_result == 1)

            try:
                assert correct_result == getattr(x, op)(y)
            except AssertionError:
                print "Sampling results:", sampled_results
                raise Exception("Semantic value of %s %s (%s) %s not"
                                " correctly reproduced."
                                % (x, op, y, correct_result))
                

    # With different numbers:
    test_all_comparison_ops(Number_with_uncert((3, 0.1)),
                            Number_with_uncert((-2, 0.1)))
    test_all_comparison_ops(Number_with_uncert((0, 0)),  # Special number
                            Number_with_uncert((1, 1)))
    test_all_comparison_ops(Number_with_uncert((0, 0)),  # Special number
                            Number_with_uncert((0, 0.1)))
    # With identical numbers:
    test_all_comparison_ops(Number_with_uncert((0, 0)),
                            Number_with_uncert((0, 0)))
    test_all_comparison_ops(Number_with_uncert((1, 1)),
                            Number_with_uncert((1, 1)))


def test_logic():
    "Boolean logic: __nonzero__, bool."

    x = Number_with_uncert((3, 0))
    y = Number_with_uncert((0, 0))
    z = Number_with_uncert((0, 0.1))
    t = Number_with_uncert((-1, 2))

    assert bool(x) == True
    assert bool(y) == False
    assert bool(z) == True
    assert bool(t) == True  # Only infinitseimal neighborhood are used

        
    
def test_basic_access_to_data():
    "Access to data from Number_with_uncert and AffineScalarFunc objects."

    x = Number_with_uncert((3.14, 0.01), "x var")
    assert x.tag == "x var"
    assert x.nominal_value == 3.14
    assert x.std_dev() == 0.01

    # Case of AffineScalarFunc objects:
    y = x + 0
    assert type(y) == AffineScalarFunc
    assert y.nominal_value == 3.14
    assert y.std_dev() == 0.01

    # Details on the sources of error:
    a = Number_with_uncert((-1, 0.001))
    y = 2*x + 3*x + 2 + a
    error_sources = y.error_components()
    assert len(error_sources) == 2  # 'a' and 'x'
    assert error_sources[x] == 0.05
    assert error_sources[a] == 0.001

    # Derivative values should be available:
    assert y.derivatives[x] == 5

    # Modification of the standard deviation of variables:
    x.set_std_dev(1)
    assert y.error_components()[x] == 5  # New error contribution!

    # Calculation of deviations in units of the standard deviations:
    assert 10/x.std_dev() == x.position_in_sigmas(10 + x.nominal_value)

    # "In units of the standard deviation" is not always meaningfull:
    x.set_std_dev(0)
    try:
        x.position_in_sigmas(1)
    except ValueError:
        pass  # Normal behavior
    else:
        raise

def test_numerical_example():
    "Specific numerical examples"

    x = Number_with_uncert((3.14, 0.01))
    result = math.sin(x)
    # In order to prevent big errors such as a wrong, constant value
    # for all analytical and numerical derivatives, which would make
    # test_fixed_derivatives_math_funcs() succeed despite incorrect
    # calculations:
    assert ("%.6f +- %.6f" % (result.nominal_value, result.std_dev())
            == "0.001593 +- 0.010000")

    # Regular calculations should still work:
    assert("%.11f" % math.sin(3) == "0.14112000806")

    
def test_math_module():
    "Operations with the math module"

    import math
    
    x = Number_with_uncert((-1.5, 0.1))
    
    # The exponent must not be differentiated, when calculating the
    # following (the partial derivative with respect to the exponent
    # is not defined):
    assert (x**2).nominal_value == 2.25

    # factorial must not be "damaged" by this module; in particular,
    # as of Python 2.6, it does not accept non integral values, and
    # must therefore not be differentiated:
    try:
        assert math.factorial(4) == 24  # Only for Python >= 2.6
    except AttributeError:
        pass

    # Regular operations are chosen to be unchanged:
    assert isinstance(math.sin(3), float)

    # Some math functions have a result that cannot be represented by
    # AffineScalarFunc objects.

    # math.frexp does not return a scalar, and therefore cannot be
    # represented by an AffineScalarFunc object.

    # math.fsum does not take scalar arguments.

    for func_name in _no_wrapping:
        try:
            print getattr(math, func_name)(Number_with_uncert((3.1, 0.1)))
        except TypeError, err:
            # For frexp, modf:
            if str(err).startswith("can't convert an affine function"):
                pass
            elif str(err).startswith("fsum() argument after *"):
                pass
            else:
                raise

    # Boolean functions:
    try:
        assert not math.isinf(x)  # Only for Python >= 2.6
    except AttributeError:
        pass
    
    # Comparison, possibly between an AffineScalarFunc object and a
    # boolean, which makes things more difficult for this code:
    try:
        assert math.isinf(x) == False  # Only for Python >= 2.6
    except AttributeError:
        pass
    
def test_correlations():
    "Correlations between variables"

    a = Number_with_uncert(1)
    x = Number_with_uncert((4, 0.1))
    y = x*2 + a
    # Correlations cancel "naive" additions of uncertainties:
    assert y.std_dev() != 0
    normally_zero = y - (x*2 + 1)
    assert normally_zero.nominal_value == 0
    assert normally_zero.std_dev() == 0

def test_str_input():

    "Input of numbers with uncertainty as a string"

    # String representation, and numerical values:
    tests = {
        "-1.23(3.4)": (-1.23, 3.4),  # (Central value, error)
        "-1.34(5)": (-1.34, 0.05),
        "1(6)": (1, 6),
        "3(4.2)": (3, 4.2),
        "-9(2)": (-9, 2),
        "1234567(1.2)": (1234567, 1.2),
        "12.345(15)": (12.345, 0.015),
        "-12.3456(78)e-6": (-12.3456e-6, 0.0078e-6),
        "0.29": (0.29, 0.01),
        "31.": (31, 1),
        "-31.": (-31, 1),
        "31": (31, 1),
        "-3.1e10": (-3.1e10, 0.1e10),
        "169.0(7)": (169, 0.7)
        }
          
    for (representation, values) in tests.iteritems():
        
        num = Number_with_uncert(representation)

        assert _numbers_close(num.nominal_value, values[0])
        assert _numbers_close(num.std_dev(), values[1])

def test_numpy():
    
    """
    Interaction with Numpy, including matrix inversion and
    correlated_values()--which depends on Numpy.
    """

    try:
        import numpy
    except ImportError:
        return

    arr = numpy.array(range(3))
    num = Number_with_uncert((3.14, 0.01))

    # Numpy arrays can be multiplied by Number_with_uncert objects,
    # whatever the order of the operands:
    prod1 = arr*num
    prod2 = num*arr
    # Additional check:
    assert (prod1 == prod2).all()

    # Operations with arrays work (they are first handled by Numpy,
    # then by this module):
    prod1*prod2
    assert not (prod1-prod2).any()  # All elements must be 0

    # Comparisons work too:

    # Usual behavior:
    assert len(arr[arr > 1.5]) == 1
    # Comparisons with Number_with_uncert objects:
    assert len(arr[arr > Number_with_uncert((1.5, 0.1))]) == 1

    assert len(prod1[prod1 < prod1*prod2]) == 2

    # The following can be calculated (special Numpy abs() function):
    numpy.abs(arr + Number_with_uncert((-1, 0.1)))

    # The following does not completely work, because Numpy does not
    # implement numpy.exp on an array of general objects, apparently:
    assert numpy.exp(arr).all()  # All elements > 0
    # Equivalent with an array of AffineScalarFunc objects:
    try:
        numpy.exp(arr + Number_with_uncert((0, 0)))
    except AttributeError:
        pass  #! This is usual (but could be avoided)
    else:
        raise Exception("numpy.exp unexpectedly worked")

    ########################################
    # Matrix inversion:

    # Matrix with a mix of Number_with_uncert objects and regular
    # Python numbers:

    m = numpy.mat([[ Number_with_uncert((10, 1)), -3.1],
                   [0, Number_with_uncert(3)]])
    m_nominal_values = _matrix_nominal_values(m)

    # "Regular" inverse matrix, when uncertainties are not taken
    # into account:
    m_no_uncert_inv = m_nominal_values.I

    assert type(m[0, 0]) == Number_with_uncert
    # m_no_uncert_inv is a matrix of floats, with no uncertainties:
    assert isinstance(m_no_uncert_inv[0, 0], float)

    # Inverse with uncertainties:
    m_inv_uncert = m.I  # AffineScalarFunc elements
    assert type(m_inv_uncert[0, 0]) == AffineScalarFunc

    # Checks of the numerical values: the diagonal elements of the
    # inverse should be the inverses of the diagonal elements of
    # m (because we started with a triangular matrix):

    assert _numbers_close(1/m_nominal_values[0, 0],
                          m_inv_uncert[0, 0].nominal_value), "Wrong value"
    assert _numbers_close(1/m_nominal_values[1, 1],
                          m_inv_uncert[1, 1].nominal_value)


    # Checks of the covariances between elements:
    x = Number_with_uncert((10, 1))
    m = numpy.mat([[x, x],
                   [0, 3+2*x]])

    m_inverse = m.I


    # Check of the properties of the inverse:
    m_double_inverse = m_inverse.I
    # The initial matrix should be recovered, including its
    # derivatives, which define covariances:
    assert _numbers_close(m_double_inverse[0, 0].nominal_value,
                          m[0, 0].nominal_value)
    assert _numbers_close(m_double_inverse[0, 0].std_dev(),
                          m[0, 0].std_dev())


    def _derivatives_close(x, y):
        """
        Returns True iff the AffineScalarFunc objects x and y have
        derivatives that are close to each other (they must depend
        on the same variables).
        """

        # x and y must depend on the same variables:
        if len(set(x.derivatives)\
               .symmetric_difference(y.derivatives)):
            return False  # Not the same variables

        return all( _numbers_close(x.derivatives[var],
                                   y.derivatives[var])
                    for var in x.derivatives)


    # The double inverse should be exactly the initial function:
    def _matrices_almost_equal(m1, m2):
        """
        Returns True iff m1 and m2 are almost equal, where elements
        can be either floats or AffineScalarFunc objects.
        """

        for (elmt1, elmt2) in zip(m1.flat, m2.flat):

            # For a simpler comparison, both elements are
            # converted to AffineScalarFunc objects:
            elmt1 = to_affine_scalar(elmt1)
            elmt2 = to_affine_scalar(elmt2)

            if not _numbers_close(elmt1.nominal_value,
                                  elmt2.nominal_value, 1e-4):
                return False

            if not _numbers_close(elmt1.std_dev(), elmt2.std_dev(), 1e-4):
                return False
        return True

    assert _matrices_almost_equal(m_double_inverse, m)

    # Partial test:
    assert _derivatives_close(m_double_inverse[0, 0], m[0, 0])
    assert _derivatives_close(m_double_inverse[1, 1], m[1, 1])

    ####################

    # Tests of covariances during the inversion:

    # There are correlations if both the next two derivatives are
    # not zero:
    assert m_inverse[0, 0].derivatives[x]
    assert m_inverse[0, 1].derivatives[x]

    # Correlations between m and m_inverse should create a perfect
    # inversion:
    assert _matrices_almost_equal(m * m_inverse,  numpy.eye(m.shape[0]))

    ########################################

    # Covariances between output and input variables:

    x = Number_with_uncert((1, 0.1))
    y = -2*x+10
    z = -3*x
    covs = covariance_matrix([x, y, z])
    # Diagonal elements are simple:
    assert _numbers_close(covs[0][0], 0.01)
    assert _numbers_close(covs[1][1], 0.04)
    assert _numbers_close(covs[2][2], 0.09)
    # Non-diagonal elements:
    assert _numbers_close(covs[0][1], -0.02)

    # "Inversion" of the covariance matrix: creation of new
    # variables:
    (x_new, y_new, z_new) = correlated_values(
        [x.nominal_value, y.nominal_value, z.nominal_value],
        covs,
        tags = ['x', 'y', 'z'])

    # Even the uncertainties should be correctly reconstructed:
    assert _matrices_almost_equal(numpy.array((x, y, z)),
                                  numpy.array((x_new, y_new, z_new)))

    # ... and the covariances too:
    assert _matrices_almost_equal(
        numpy.array(covs),
        numpy.array(covariance_matrix([x_new, y_new, z_new])))

    assert _matrices_almost_equal(
        numpy.array([y_new]), numpy.array([-2*x_new+10]))

    ####################

    # ... as well as functional relations:

    u = Number_with_uncert((1, 0.05))
    v = Number_with_uncert((10,  0.1))
    sum_value = u+v

    # Covariance matrices:
    cov_matrix = covariance_matrix([u, v, u+v])

    # Correlated variables can be constructed from a covariance matrix, if
    # Numpy is available:
    (u2, v2, sum2) = correlated_values(
        [x.nominal_value for x in [u, v, sum_value]],
        cov_matrix)
    assert _matrices_almost_equal(numpy.array([0]),
                                  numpy.array([sum2-u2-v2]))
    
def test_no_coercion():
    """
    Coercion of Number_with_uncert to simple floats: impossible.
    """

    x = Number_with_uncert((4, 1))
    try:
        print float(x)
    except TypeError:
        pass
    else:
        raise Exception("Conversion to float() should fail.")
