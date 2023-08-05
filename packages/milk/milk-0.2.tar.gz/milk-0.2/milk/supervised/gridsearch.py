# -*- coding: utf-8 -*-
# Copyright (C) 2008-2010, Luis Pedro Coelho <lpc@cmu.edu>
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
from ..measures.nfoldcrossvalidation import nfoldcrossvalidation

def _allassignments(D):
    def allassignmentslist(L):
        if len(L) == 0:
            yield []
            return
        key0,vals0 = L[0]
        for v in vals0:
            for rest in allassignmentslist(L[1:]):
                yield [(key0,v)]+rest
    for A in allassignmentslist(list(D.items())):
        yield A

def _set_assignment(obj,assignments):
    for k,v in assignments:
        obj.set_option(k,v)

class gridsearch(object):
    '''
    G = gridsearch(base, measure=accuracy, param1=[...], param2=[...], ...)

    Perform a grid search for the best parameter values.


    When G.train() is called, then for each combination of p1 in param1, p2 in
    param2, ... it performs::

        base_classifier.param1 = p1
        base_classifier.param2 = p2
        ...
        value[p1, p2,...] = measure(crossvaliation(base_classifier)

    it then picks the highest set of parameters and re-learns a model on the
    whole data.


    Parameters
    -----------
      base_classifier : classifier to use
      measure : a function which takes a confusion matrix and outputs
                 how good the matrix is
    '''
    def __init__(self, base, measure=None, params={}):
        self.params = params
        self.base = base
        self.best = None
        if measure is None:
            measure = np.trace
        self.measure = measure

    def is_multi_class(self):
        return self.base.is_multi_class()

    def train(self,features,labels):
        best_val = -1
        for assignement in _allassignments(self.params):
            _set_assignment(self.base, assignement)
            #print 'gridsearch:', assignement
            S,_ = nfoldcrossvalidation(features, labels, classifier=self.base)
            cur = self.measure(S)
            if cur > best_val:
                self.best = assignement
                best_val = cur
        _set_assignment(self.base, self.best)
        return self.base.train(features, labels)


# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
