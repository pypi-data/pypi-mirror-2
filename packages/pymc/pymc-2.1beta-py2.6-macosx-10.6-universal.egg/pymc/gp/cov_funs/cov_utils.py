# Copyright (c) Anand Patil, 2007

import numpy as np
import wrapped_distances
import inspect
import imp
import pickle
from isotropic_cov_funs import symmetrize, imul
from copy import copy
import sys,os
from pymc import get_threadpool_size, map_noreturn
import pymc
mod_search_path = [pymc.__path__[0]+'/gp/cov_funs', os.getcwd()] + sys.path


__all__ = ['covariance_wrapper', 'covariance_function_bundle']


def regularize_array(A):
    """
    Takes an np.ndarray as an input.


    - If the array is one-dimensional, it's assumed to be an array of input values.

    - If the array is more than one-dimensional, its last index is assumed to curse
      over spatial dimension.


    Either way, the return value is at least two dimensional. A.shape[-1] gives the
    number of spatial dimensions.
    """
    if not isinstance(A,np.ndarray):
        A = np.array(A, dtype=float)
    else:
        A = np.asarray(A, dtype=float)

    if len(A.shape) <= 1:
        return A.reshape(-1,1)

    elif A.shape[-1]>1:
        return A.reshape(-1, A.shape[-1])

    else:
        return A

def import_nested_module(name):
    """
    Useful for importing nested modules such as pymc.gp.cov_funs.isotropic_cov_funs.
    """
    tree = name.split('.')
    root = tree[0]
    submods = tree[1:]
    mod = imp.load_module(root, *imp.find_module(root, mod_search_path))

    for name in submods:
        mod = getattr(mod,name)

    return mod


class covariance_wrapper(object):
    """
    A wrapper for the Fortran covariance functions that
    removes the need for worrying about the common arguments
    amp and scale, and that separates the distance-finding
    from the covariance-evaluating for less code duplication
    and easier nonstationary generalizations.

    Parallelizes calls of sufficient size.
    """

    # pickle support
    def __getstate__(self):
        return (self.cov_fun_name, self.cov_fun_module.__name__, self.extra_cov_params,
                self.distance_fun_name, self.distance_fun_module.__name__)

    def __setstate__(self, state):
        self.__init__(*state)

    def __init__(self, cov_fun_name, cov_fun_module, extra_cov_params, distance_fun_name, distance_fun_module):

        self.cov_fun_name = cov_fun_name
        self.distance_fun_name = distance_fun_name

        cov_fun_module = import_nested_module(cov_fun_module)
        cov_fun = getattr(cov_fun_module, cov_fun_name)

        distance_fun_module = import_nested_module(distance_fun_module)
        distance_fun = getattr(distance_fun_module, distance_fun_name)

        self.cov_fun_module = cov_fun_module
        self.cov_fun = cov_fun
        self.distance_fun_module = distance_fun_module
        self.distance_fun = distance_fun
        self.extra_cov_params = extra_cov_params
        self.__doc__ = cov_fun_name + '.' + distance_fun.__name__+ covariance_wrapperdoc[0]

        # Add covariance parameters to function signature
        for parameter in extra_cov_params.iterkeys():
            self.__doc__ += ', ' + parameter
        # Add distance parameters to function signature
        if hasattr(distance_fun,'extra_parameters'):
            self.extra_distance_params = distance_fun.extra_parameters
            for parameter in self.extra_distance_params.iterkeys():
                self.__doc__ += ', ' + parameter
        # Document covariance parameters
        self.__doc__ += covariance_wrapperdoc[1]
        if hasattr(cov_fun, 'extra_parameters'):
            for parameter in extra_cov_params.iterkeys():
                self.__doc__ += "\n\n    - " + parameter + ": " + extra_cov_params[parameter]
        # Document distance parameters.
        if hasattr(distance_fun,'extra_parameters'):
            for parameter in self.extra_distance_params.iterkeys():
                self.__doc__ += "\n\n    - " + parameter + ": " + self.extra_distance_params[parameter]

        self.__doc__ += "\n\nDistances are computed using "+distance_fun.__name__+":\n\n"+distance_fun.__doc__

    def __call__(self,x,y,amp=1.,scale=1.,symm=None,*args,**kwargs):

        if amp<0. or scale<0.:
            raise ValueError, 'The amp and scale parameters must be positive.'

        if symm is None:
            symm = (x is y)

        # Figure out how to divide job up between threads.
        nx = x.shape[0]
        ny = y.shape[0]
        n_threads = min(get_threadpool_size(), nx*ny / 10000)

        if n_threads > 1:
            if not symm:
                bounds = np.linspace(0,ny,n_threads+1)
            else:
                bounds = np.array(np.sqrt(np.linspace(0,ny*ny,n_threads+1)),dtype=int)

        # Split off the distance arguments
        distance_arg_dict = {}
        if hasattr(self.distance_fun, 'extra_parameters'):
            for key in self.extra_distance_params.iterkeys():
                if key in kwargs.keys():
                    distance_arg_dict[key] = kwargs.pop(key)

        # Allocate the matrix
        C = np.asmatrix(np.empty((nx,ny),dtype=float,order='F'))

        def targ(C,x,y, cmin, cmax,symm, d_kwargs=distance_arg_dict, c_args=args, c_kwargs=kwargs):
            # Compute distance for this bit
            self.distance_fun(C, x, y, cmin=cmin, cmax=cmax, symm=symm, **d_kwargs)
            imul(C, 1./scale, cmin=cmin, cmax=cmax, symm=symm)
            # Compute covariance for this bit
            self.cov_fun(C, cmin=cmin, cmax=cmax,symm=symm, *c_args, **c_kwargs)
            imul(C, amp*amp, cmin=cmin, cmax=cmax, symm=symm)

        if n_threads <= 1:
            targ(C,x,y,0,-1,symm)
        else:
            thread_args = [(C,x,y,bounds[i],bounds[i+1],symm) for i in xrange(n_threads)]
            map_noreturn(targ, thread_args)

        if symm:
            symmetrize(C)


        return C

class covariance_wrapper_with_diag(covariance_wrapper):
    def diag_call(self, x, amp=1., scale=1., *args, **kwds):
        return amp**2*np.ones(x.shape[0])

# Common verbiage in the covariance functions' docstrings
covariance_wrapperdoc = ["(x,y",""", amp=1., scale=1.)

A covariance function. Remember, broadcasting for covariance functions works
differently than for numpy universal functions. C(x,y) returns a matrix, and
C(x) returns a vector.


:Arguments:

    - `x, y`: arrays on which to evaluate the covariance function.

    - `amp`: The pointwise standard deviation of f.

    - `scale`: The factor by which to scale the distance between points.
             Large value implies long-range correlation."""]


class covariance_function_bundle(object):
    """
    B = covariance_function_bundle(cov_fun)

    A bundle of related covariance functions that use the stationary,
    isotropic covariance function cov_fun.

    Attributes:

        - `raw`: The raw covariance function, which overwrites a
          distance matrix with a covariance matrix.

        - `euclidean`: The covariance function wrapped to use
          Euclidean coordinates in R^n, with amp and scale arguments.

        - `geo_rad`: The covariance function wrapped to use
          geographic coordinates (latitude and longitude) on the
          surface of the sphere, with amp and scale arguments.

          Angles are assumed to be in radians. Radius of sphere is
          assumed to be 1, but you can effectively change the radius
          using the 'scale' argument.

        - `geo_deg`: Like geo_rad, but angles are in degrees.

        - `aniso_geo_rad`: Like geo_rad, but the distance function takes extra
          parameters controlling the eccentricity and angle of inclination of
          the elliptical level sets of distance.

        - `aniso_geo_deg`: Like aniso_geo_rad, but angles are in degrees.

        - `nonstationary`: Not implemented yet.

    Method:

        - `add_distance_metric(distance_fun)`: Takes a function that computes a
          distance matrix for points in some coordinate system and returns
          the covariance function wrapped to use that coordinate system.

    :Parameters:

        - `cov_fun` should overwrite distance matrices with covariance
          matrices in-place. In addition to the distance matrix, it should
          take an optional argument called 'symm' which indicates whether
          the output matrix will be symmetric.
    """

    def __init__(self, cov_fun_name, cov_fun_module, extra_cov_params, ampsq_is_diag=False):

        self.cov_fun_name = cov_fun_name
        self.cov_fun_module = cov_fun_module
        self.extra_cov_params = extra_cov_params
        self.ampsq_is_diag = ampsq_is_diag

        self.add_distance_metric('euclidean','wrapped_distances')
        self.add_distance_metric('geo_rad','wrapped_distances')
        self.add_distance_metric('geo_deg','wrapped_distances')
        self.add_distance_metric('aniso_geo_rad','wrapped_distances')
        self.add_distance_metric('aniso_geo_deg','wrapped_distances')
        self.add_distance_metric('partition_aniso_geo_deg','wrapped_distances')
        self.add_distance_metric('partition_aniso_geo_rad','wrapped_distances')

        self.raw = self.euclidean.cov_fun

    def add_distance_metric(self, distance_fun_name, distance_fun_module):
        """
        Takes a function that computes a distance matrix for
        points in some coordinate system and returns self's
        covariance function wrapped to use that distance function.


        Uses function apply_distance, which was used to produce
        self.euclidean and self.geographic and their docstrings.


        :Parameters:

            - `distance_fun`: Creates a distance matrix from two
              np.arrays of points, where the first index iterates
              over separate points and the second over coordinates.

              In addition to the arrays x and y, distance_fun should
              take an argument called symm which indicates whether
              x and y are the same array.


        :SeeAlso:
            - `apply_distance()`
        """

        if self.ampsq_is_diag:
            kls = covariance_wrapper_with_diag
        else:
            kls = covariance_wrapper
        new_fun = kls(self.cov_fun_name, self.cov_fun_module, self.extra_cov_params, distance_fun_name, distance_fun_module)
        # try:
        setattr(self, distance_fun_name, new_fun)
        # except:
        #     pass
        return new_fun


# def nonstationary(cov_fun):
#     """
#     A decorator for an isotropic covariance function. Takes one
#     additional argument, kernel, which takes a value for input
#     argument x and returns a kernel matrix Sigma(x), which is square,
#     positive definite and  of the same rank as the dimension of x, as
#     in theorem 1 of the reference below.
#
#
#     Christopher J. Paciorek,
#     "Nonstationary Gaussian processes for regression and spatial modeling",
#     PhD. Thesis, Carnegie Mellon University Department of Statistics,
#     May 2003.
#
#
#     TODO: Figure out what to do about the quadratic forms in different
#     coordinate systems.
#
#
#     Note: No scale parameter is necessary, you can manipulate the kernels
#     to get the same effect. The amp parameter is still necessary, though.
#
#     WARNING: Not implemented yet.
#     """
#     def covariance_wrapper(x,y,kernel,amp=1.,*args,**kwargs):
#         symm = (x is y)
#         kwargs['symm']=symm
#
#         x = regularize_array(x)
#         if symm:
#             y=x
#         else:
#             # if y_map is not None:
#             #     y = y_map(y)
#             y = regularize_array(y)
#
#         ndim = x.shape[1]
#
#         # Compute and store the kernels (note: you can do this in the loop with no loss
#         # if symm=False.)
#         kernels_x = np.zeros((len(x),ndim,ndim),dtype=float)
#         for i in range(len(x)):
#             kernels[i,:,:] = kernel(x[i,:])
#         if not symm:
#             kernels_y = np.zeros((len(y),ndim,ndim),dtype=float)
#             for i in range(len(y)):
#                 kernels[i,:,:] = kernel(y[i,:])
#
#         # Compute the distance matrix and the prefactors.
#         C = np.zeros((len(x),len(y)),dtype=flooat)
#         prefacs = np.ones(len(x), len(y), dtype=float) * 2. ** (ndim*.5) * amp
#
#         for i in range(len(x)):
#             kern_x = asmatrix(kernels_x[i,:,:])
#             for j in range(len(y)):
#                 if symm:
#                     kern_y = kern_x
#                 else:
#                     kern_y = asmatrix(kernels_y[j,:,:])
#                 sum_kern = .5 * (kern_x + kern_y)
#                 dev = (x[i,:]-y[j,:])
#                 # Eventually just make this a half-loop if symm=True, of course.
#                 C[i,j] = (dev.T * solve(sum_kern, dev))
#
#                 # Eventually, make the prefactor zero if one of the kernels is lower
#                 # rank than the other. Also make it work if the kernels are both
#                 # not full rank.
#                 prefacs[i,j] *= (det(kern_x) * det(kern_y))**(.25) / det(sum_kern)**.5
#
#         # Overwrite the distance matrix using a Fortran covariance function
#         cov_fun(C,*args,**kwargs)
#         C *= prefacs
#
#         return C
#
#     return covariance_wrapper
#
