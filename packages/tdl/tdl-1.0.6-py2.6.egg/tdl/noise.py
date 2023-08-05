#!/usr/bin/env python
"""
    This module provides access to noise generaters that can be used for world
    generation or special effects.

    Normally it is used like this:
    n = Perlin(3) # up to 4D (except Wavelet witch only goes up to 3D)
    print n[.1, .1, .1]
    print n[.2, .2, .2]
    print n[.2, .2]

    some of the generators allow you to set the hurst, lacunarity, and octaves.

"""
import ctypes

from tcod import _lib

class Perlin(object):
    __slots__ = ('_cfloats', '_noisegen', 'dimensions', 'octaves',
                 'hurst', 'lacunarity')
    MAXDIMENSIONS = 4
    MAXOCTAVES = 128
    CFLOATS = tuple((ctypes.c_float * d for d in xrange(1, MAXDIMENSIONS + 1)))
    GENERATOR = _lib.TCOD_noise_perlin

    def __del__(self):
        try:
            _lib.TCOD_noise_delete(self._noisegen)
        except StandardError:
            pass

    def __init__(self, dimensions=2):
        assert 0 < dimensions <= self.MAXDIMENSIONS
        self.dimensions = dimensions
        self._cfloats = self.CFLOATS[dimensions - 1]
        self._noisegen = _lib.TCOD_noise_new(dimensions, 0.5, 2.0, None)

    def __getitem__(self, key):
        if isinstance(key, (int, float)):
            key = key,
        else:
            assert 0 < len(key) <= self.dimensions
        return (self.GENERATOR(self._noisegen, self._cfloats(*key)))

class FBM(Perlin):
    __slots__ = ()
    GENERATOR = _lib.TCOD_noise_fbm_perlin

    def __init__(self, dimensions=2, hurst=0.5, lacunarity=2.0, octaves=4):
        assert 0 < dimensions <= self.MAXDIMENSIONS
        assert octaves < self.MAXOCTAVES
        self.dimensions = dimensions
        self.hurst = hurst
        self.lacunarity = lacunarity
        self._cfloats = self.CFLOATS[dimensions - 1]
        self._noisegen = _lib.TCOD_noise_new(dimensions, hurst, lacunarity, None)
        self.octaves = octaves

    def __getitem__(self, key):
        if isinstance(key, (int, float)):
            key = key,
        else:
            assert 0 < len(key) <= self.dimensions
        return self.GENERATOR(self._noisegen,  self._cfloats(*key), self.octaves)

class Turbulence(FBM):
    __slots__ = ()
    GENERATOR = _lib.TCOD_noise_turbulence_perlin

    def __getitem__(self, key):
        if isinstance(key, (int, float)):
            key = key,
        else:
            assert 0 < len(key) <= self.dimensions
        return self.GENERATOR(self._noisegens, self._cfloats(*key), self.octaves)

class Simplex(Perlin):
    __slots__ = ()
    GENERATOR = _lib.TCOD_noise_simplex

class SimplexFBM(FBM):
    __slots__ = ()
    GENERATOR = _lib.TCOD_noise_fbm_simplex

class SimplexTurbulence(Turbulence):
    __slots__ = ()
    GENERATOR = _lib.TCOD_noise_turbulence_simplex

class Wavelet(Perlin):
    __slots__ = ()
    MAXDIMENSIONS = 3
    GENERATOR = _lib.TCOD_noise_wavelet

class WaveletFBM(FBM):
    __slots__ = ()
    MAXDIMENSIONS = 3
    GENERATOR = _lib.TCOD_noise_fbm_wavelet

class WaveletTurbulence(Turbulence):
    __slots__ = ()
    MAXDIMENSIONS = 3
    GENERATOR = _lib.TCOD_noise_turbulence_wavelet

__all__ = [var for var in locals().keys() if not '_' in var[0]]

if __name__ == '__main__': # preform benchmarks
    import random
    import timeit
    r = lambda:random.uniform(-10, 1000)
    ranges = [[r() for i in xrange(10)],
              [(r(), r()) for i in xrange(10)],
              [(r(), r(), r()) for i in xrange(10)],
              [(r(), r(), r(), r()) for i in xrange(10)]]
    timer = timeit.Timer(stmt="""[ngen[p] for p in plist]""",
       setup="""import __main__;ngen = __main__.ngen; plist = __main__.plist""")

    for g in [Perlin, Simplex, Wavelet]:
        for d in xrange(4 if g is 'Wavelet' not in g.__name__ else 3):
            ngen = g(d+1)
            plist = ranges[d]
            print '%s %iD: %f' % (g.__name__, d+1, min(timer.repeat(3, 5000)))
