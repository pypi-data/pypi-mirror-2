# -*- coding: utf-8 -*-
# Copyright (C) 2008-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from __future__ import division
import numpy as np
from numpy import linalg

from . import _kmeans
from ..utils import get_pyrandom
from .normalise import zscore

__all__ = [
        'kmeans',
        'repeated_kmeans',
        ]


try:
    # This tests for the presence of 3-argument np.dot
    # with the 3rd argument being the output argument
    _x = np.array([1])
    _y = np.array([1])
    _r = np.array([0])
    np.dot(_x,_y,_r)
    if _r[0] != 1:
        raise NotImplementedError
    _dot3 = np.dot
except:
    def _dot3(x, y, _):
        return np.dot(x,y)
finally:
    del _x
    del _y
    del _r

def _mahalanobis2(fmatrix, x, icov):
    diff = fmatrix-x
    # The expression below seems to be faster than looping over the elements and summing
    return np.dot(diff, np.dot(icov, diff.T)).diagonal()

def centroid_errors(fmatrix, assignments, centroids):
    '''
    errors = centroid_errors(fmatrix, assignments, centroids)

    Computes the following::

        for all i, j:
            ci = assignments[i]
            errors[i,j] = fmatrix[ci, j] - centroids[ci, j]

    Parameters
    ----------
    fmatrix : 2D ndarray
        feature matrix
    assignments : 1D ndarray
        Assignments array
    centroids : 2D ndarray
        centroids

    Returns
    -------
    errors : float
        Difference between fmatrix and corresponding centroid
    '''
    errors = []
    for k,c in enumerate(centroids):
        errors.append(fmatrix[assignments == k] - c)
    return np.concatenate(errors)

def residual_sum_squares(fmatrix,assignments,centroids,distance='euclidean',**kwargs):
    '''
    rss = residual_sum_squares(fmatrix, assignments, centroids, distance='euclidean', **kwargs)

    Computes residual sum squares

    Parameters
    ----------
    fmatrix : 2D ndarray
        feature matrix
    assignments : 1D ndarray
        Assignments array
    centroids : 2D ndarray
        centroids

    Returns
    -------
    rss : float
        residual sum squares
    '''
    if distance != 'euclidean':
        raise NotImplemented, "residual_sum_squares only implemented for 'euclidean' distance"
    rss = 0.0
    for k, c in enumerate(centroids):
        diff = fmatrix[assignments == k] - c
        diff = diff.ravel()
        rss += np.dot(diff, diff)
    return rss

def assign_centroids(fmatrix, centroids):
    '''
    cids = assign_centroids(fmatrix, centroids)

    Assigns a centroid to each element of fmatrix

    Parameters
    ----------
    fmatrix : 2D ndarray
        feature matrix
    centroids : 2D ndarray
        centroids matrix

    Returns
    -------
    cids : sequence
        ``cids[i]`` is the index of the centroid closes to ``fmatrix[i]``
    '''
    dists = np.dot(fmatrix, (-2)*centroids.T)
    dists += np.array([np.dot(c,c) for c in centroids])
    return dists.argmin(1)

def _pycomputecentroids(fmatrix, centroids, assignments, counts):
    k, Nf = centroids.shape
    bins = np.arange(k+1)
    ncounts,_ = np.histogram(assignments, bins)
    counts[:] = ncounts
    any_empty = False
    mean = None
    for ci,count in enumerate(counts):
        if count:
            where = (assignments.T == ci)
            mean = _dot3(where, fmatrix, mean) # mean = dot(fmatrix.T, where.T), but it is better to not cause copies
            mean /= count
            centroids[ci] = mean
        else:
            any_empty = True
    return any_empty

def kmeans(fmatrix, k, distance='euclidean', max_iter=1000, R=None, **kwargs):
    '''
    assignments, centroids = kmean(fmatrix, k, distance='euclidean', max_iter=1000, R=None, icov=None, covmat=None)

    k-Means Clustering

    Parameters
    ----------
    fmatrix : ndarray
        2-ndarray (Nelements x Nfeatures)
    distance: string, optional
        one of:
        - 'euclidean'   : euclidean distance (default)
        - 'seuclidean'  : standartised euclidean distance. This is equivalent to first normalising the features.
        - 'mahalanobis' : mahalanobis distance.
            This can make use of the following keyword arguments:
                + 'icov' (the inverse of the covariance matrix),
                + 'covmat' (the covariance matrix)
            If neither is passed, then the function computes the covariance from the feature matrix
    max_iter : integer, optional
        Maximum number of iteration (default: 1000)
    R : source of randomness, optional

    Returns
    -------
    assignments : ndarray
        An 1-D array of size `len(fmatrix)`
    centroids : ndarray
        An array of `k'` centroids
    '''
    fmatrix = np.asanyarray(fmatrix)
    if distance == 'seuclidean':
        fmatrix = zscore(fmatrix)
        distance = 'euclidean'
    if distance == 'euclidean':
        def distfunction(fmatrix, cs, dists):
            dists = _dot3(fmatrix, (-2)*cs.T, dists)
            dists += np.array([np.dot(c,c) for c in cs])
            # For a distance, we'd need to add the fmatrix**2 components, but
            # it doesn't matter because we are going to perform an argmin() on
            # the result.
            return dists
    elif distance == 'mahalanobis':
        icov = kwargs.get('icov', None)
        if icov is None:
            covmat = kwargs.get('covmat', None)
            if covmat is None:
                covmat = np.cov(fmatrix.T)
            icov = linalg.inv(covmat)
        def distfunction(fmatrix, cs, _):
            return np.array([_mahalanobis2(fmatrix, c, icov) for c in cs]).T
    else:
        raise ValueError('milk.unsupervised.kmeans: `distance` argument unknown (%s)' % distance)
    if k < 2:
        raise ValueError('milk.unsupervised.kmeans `k` should be >= 2.')
    if fmatrix.dtype in (np.float32, np.float64) and fmatrix.flags['C_CONTIGUOUS']:
        computecentroids = _kmeans.computecentroids
    else:
        computecentroids = _pycomputecentroids
    R = get_pyrandom(R)

    centroids = np.array(R.sample(fmatrix,k), fmatrix.dtype)
    prev = np.zeros(len(fmatrix), np.int32)
    counts = np.empty(k, np.int32)
    dists = None
    for i in xrange(max_iter):
        dists = distfunction(fmatrix, centroids, dists)
        assignments = dists.argmin(1)
        if np.all(assignments == prev):
            break
        if computecentroids(fmatrix, centroids, assignments.astype(np.int32), counts):
            (empty,) = np.where(counts == 0)
            centroids = np.delete(centroids, empty, axis=0)
            k = len(centroids)
            counts = np.empty(k, np.int32)
            # This will cause new matrices to be allocated in the next iteration
            dists = None
        prev[:] = assignments
    return assignments, centroids

def repeated_kmeans(fmatrix,k,iterations,distance='euclidean',max_iter=1000,R=None,**kwargs):
    '''
    assignments,centroids = repeated_kmeans(fmatrix, k, repeats, distance='euclidean',max_iter=1000,**kwargs)

    Runs kmeans repeats times and returns the best result as evaluated
    according to distance

    See Also
    --------
    kmeans : runs kmeans once

    Parameters
    ----------
    fmatrix : feature matrix
    k : nr of centroids
    iterations : Nr of repetitions
    distance : 'euclidean' (default) or 'seuclidean'
    max_iter : Max nr of iterations per kmeans run
    R : random source

    Returns
    -------
    assignments : 1-D array of assignments
    centroids : centroids

    These are the same returns as the kmeans function
    '''
    if distance == 'seuclidean':
        fmatrix = zscore(fmatrix)
        distance = 'euclidean'
    if distance != 'euclidean':
        raise NotImplementedError, "repeated_kmeans is only implemented for 'euclidean' or 'seuclidean' distance"
    best = np.inf
    R = get_pyrandom(R)
    for i in xrange(iterations):
        A,C = kmeans(fmatrix, k, distance, max_iter=max_iter, R=R,**kwargs)
        rss = residual_sum_squares(fmatrix,A,C,distance,**kwargs)
        if rss < best:
            Ab,Cb = A,C
            best = rss
    return Ab,Cb

