# -*- coding: utf-8 -*-
# Copyright (C) 2011, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the milk distribution

from __future__ import division
import numpy as np
from milk.unsupervised.kmeans import select_best_kmeans, assign_centroids
from milk import defaultlearner

class precluster_model(object):
    def __init__(self, centroids, base):
        self.centroids = centroids
        self.base = base

    def apply(self, features):
        histogram = assign_centroids(features, self.centroids, histogram=True, normalise=1)
        return self.base.apply(histogram)
        

class precluster_learner(object):
    '''
    This learns a classifier by clustering the input features
    '''
    def __init__(self, ks, base=None):
        if base is None:
            base = defaultlearner()
        self.ks = ks
        self.base = base

    def train(self, features, labels, **kwargs):
        allfeatures = np.concatenate(features)
        assignments, centroids = select_best_kmeans(allfeatures, self.ks, 1, "AIC")
        histograms = [assign_centroids(f, centroids, histogram=True, normalise=1) for f in features]
        base_model = self.base.train(histograms, labels, **kwargs)
        return precluster_model(centroids, base_model)
