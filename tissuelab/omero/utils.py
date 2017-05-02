# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

import functools
from openalea.image.gui.pixmap import to_pix

# def to_qimg(plane):
#     img = QtGui.QImage(plane.shape[0], plane.shape[1], QtGui.QImage.Format_Indexed8)
#     for i in range(256):
#         value = QtGui.qRgb(i, i, i);
#         img.setColor(i, value);
#
#     f = 255./plane.max()
#     for i in range(plane.shape[0]):
#         for j in range(plane.shape[1]):
#             color = 255-int(f*plane[i,j])
#             img.setPixel(i,j, color)
#     return img


def to_qimg(plane):
    return to_pix(plane)


def hash_simple_list(lst):
    return 0, str(list(lst))


def image_wrapper_to_ndarray(image):
    import numpy as np

    # Prepare plane list...
    sizeZ = image.getSizeZ()
    sizeC = image.getSizeC()
    sizeT = image.getSizeT()
    zctList = []

    for z in range(sizeZ):
        for c in range(sizeC):
            for t in range(sizeT):
                zctList.append((z, c, t))

    planes = image.getPrimaryPixels().getPlanes(zctList)

    img_matrix = np.transpose(list(planes),(2,1,0))
    
    if sizeC == 1:
        return img_matrix
    else:
        img_dict = {}
        for c, label in enumerate(image.getChannelLabels()):
            img_dict[label] = img_matrix[:,:,c::sizeC]
        return img_dict

def nd_array_to_image_generator(img):
    import numpy as np
    
    planes = [np.transpose(img[:,:,i_z]) for i_z in xrange(img.shape[2])]
    def plane_gen():
        for p in planes:
            yield p
    return plane_gen


class memoized(object):

    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, hash_func, nmax=100, cache_id=0):
        if not hash_func:
            self.hash_func = lambda *args: (0, args)
        else:
            self.hash_func = hash_func
        self.nmax = nmax
        self.cache_keys = {}
        self.cache_values = {}

    def __call__(self, cached_func):
        def wrapped_f(cls, *func_params):
            cache_id, hashed_args = self.hash_func(*func_params)

            # if cache doesn't exist, create it
            if cache_id not in self.cache_keys:
                self.cache_keys[cache_id] = []
                self.cache_values[cache_id] = []

            # if cache is full, remove first item
            if len(self.cache_keys[cache_id]) > self.nmax:
                print 'remove old', cache_id, repr(self.cache_keys[cache_id][0])
                self.cache_keys[cache_id].pop(0)
                self.cache_values[cache_id].pop(0)

            if hashed_args in self.cache_keys[cache_id]:
                return self.cache_values[cache_id][self.cache_keys[cache_id].index(hashed_args)]
            else:
                value = cached_func(cls, *func_params)
                self.cache_keys[cache_id].append(hashed_args)
                self.cache_values[cache_id].append(value)
                return value
        wrapped_f.clear_cache = self.clear_cache
        return wrapped_f

    def clear_cache(self, cache_id=None):
        if cache_id is None:
            print 'clear all caches'
            self.cache_keys = {}
            self.cache_values = {}
        elif cache_id in self.cache_keys:
            print 'clear cache', cache_id
            self.cache_keys[cache_id] = []
            self.cache_values[cache_id] = []
        else:
            print 'no cache %d to clean' % cache_id

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)

if __name__ == '__main__':

    class A(object):

        @memoized('', 5)
        def test(self, n1, n2, n3):
            return n1 + n2 + n3

        @memoized(hash_simple_list)
        def test2(self, args):
            return sum(args)

    a = A()
    assert a.test(1, 1, 1) == 3
    assert a.test(1, 2, 3) == 6
    assert a.test(1, 1, 1) == 3

    assert a.test2([1, 1, 1]) == 3
    assert a.test2([1, 2, 3, 4]) == 10
    assert a.test2([1, 1, 1]) == 3
    a.test2.clear_cache(0)

    for i in range(10):
        assert a.test(i, 1, 1) == i + 2
    a.test.clear_cache(0)
