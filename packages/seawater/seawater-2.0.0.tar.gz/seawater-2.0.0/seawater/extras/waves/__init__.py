# -*- coding: utf-8 -*-

import numpy as np
import seawater.csiro as sw

class Waves():
    """
    Solves the wave dispersion relationship.

    .. math::
        \Omega = ...

    Parameters
    ----------
    h : array_like, str
        Water depth [m] or 'deep', 'shallow' as keywords
    T : array_like
        Wave period [s]
    L : array_like
        Wave length [m]
    thetao : array_like
        TODO
    Ho : array_like
        TODO

    Returns
    -------
    omega : array_like
            Wave frequency
    TODO: hoLo, hoL, Lo, L, k, T, Co, C, Cg, G, Ks, Kr, theta, H

    Notes
    -----
    Compare values with:
    http://www.coastal.udel.edu/faculty/rad/wavetheory.html

    Examples
    --------
    >>> from seawater.extras.waves import Waves
    >>> Waves(h=10, T=5, L=None)

    References
    ----------
    TODO

    Modifications: Filipe Fernandes, 2010
                10-01-26. Filipe Fernandes, first version.
    """

    def __init__(self, h, T=None, L=None, thetao=None, Ho=None, lat=None):
        self.T = np.asarray( T, dtype=np.float32 )
        self.L = np.asarray( L, dtype=np.float32 )
        self.Ho = np.asarray( Ho, dtype=np.float32 )
        self.lat = np.asarray( lat, dtype=np.float32 )
        self.thetao = np.asarray( thetao, dtype=np.float32 )

        if isinstance(h, str):
            if L is not None:
                if h == 'deep':
                    self.h = self.L/2.
                elif h == 'shallow':
                    self.h = self.L * 0.05
        else:
            self.h = np.asarray( h, dtype=np.float32 )

        if lat is None:
            g = 9.81 # default gravity
        else:
            g = sw.grav(lat) #FIXME

        if L is None:
            self.omega = 2 * np.pi / self.T
            self.Lo    = (g * self.T**2) / 2 / np.pi
            # returns wavenumber of the gravity wave dispersion relation using newtons method
            self.k = self.omega / np.sqrt(g) # the initial guess will be the shallow water wavenumber
            # TODO: May change to : self.k = self.w**2 / ( g * np.sqrt(
            # self.w**2 * self.h / g ) )
            f = g * self.k * np.tanh( self.k * self.h ) - self.omega**2

            while np.abs(f.max()) > 1e-10:
                dfdk = g * self.k * self.h * ( 1 / ( np.cosh( self.k * self.h ) ) )**2 + g * np.tanh( self.k * self.h )
                self.k    = self.k - f / dfdk
                f    = g * self.k * np.tanh( self.k * self.h ) - self.omega**2 #FIXME

            self.L = 2 * np.pi / self.k
            if isinstance(h, str):
                if h == 'deep':
                    self.h = self.L/2.
                elif h == 'shallow':
                    self.h = self.L * 0.05
        else:
            self.Lo    = self.L / np.tanh( 2 * np.pi * self.h / self.L )
            self.k     = 2 * np.pi / self.L
            self.T     = np.sqrt( 2 * np.pi * self.Lo / g )
            self.omega = 2 * np.pi / self.T

        self.hoL   = self.h / self.L
        self.hoLo  = self.h / self.Lo
        self.C     = self.omega / self.k # or L / T
        self.Co    = self.Lo / self.T
        self.G     = 2 * self.k * self.h / np.sinh( 2 * self.k * self.h )
        self.n     = ( 1 + self.G ) / 2
        self.Cg    = self.n * self.C
        self.Ks    = np.sqrt( 1 / ( 1 + self.G ) / np.tanh( self.k * self.h ) )

        if thetao is None:
            self.theta = np.NaN
            self.Kr    = np.NaN
        if thetao is not None:
            self.theta = np.rad2deg( np.asin( self.C / self.Co * np.sin( np.deg2rad( self.thetao ) ) ) )
            self.Kr    = np.sqrt( np.cos( np.deg2rad( self.thetao ) ) / np.cos( np.deg2rad( self.theta ) ) )

        if Ho is None:
            self.H = np.NaN
        if Ho is not None:
            self.H = self.Ho * self.Ks * self.Kr

if __name__=='__main__':
    wav = Waves(h=10, T=5, L=None)
    print "ho/Lo = %s " % wav.hoLo
    print "ho/L  = %s " % wav.hoL
    print "Lo    = %s " % wav.Lo
    print "L     = %s " % wav.L
    print "k     = %s " % wav.k
    print "omega = %s " % wav.omega
    print "T     = %s " % wav.T
    print "C     = %s " % wav.C
    print "Cg    = %s " % wav.Cg
    print "G     = %s " % wav.G
    #print "  = %s " % wav.G
    #print "  = %s " % wav.Ks
    #print "  = %s " % wav.Kr
    #print "  = %s " % wav.theta
    #print "  = %s " % wav.H
    print
    print
    wav = Waves(h=10, T=None, L=100)
    print "ho/Lo = %s " % wav.hoLo
    print "ho/L  = %s " % wav.hoL
    print "Lo    = %s " % wav.Lo
    print "L     = %s " % wav.L
    print "k     = %s " % wav.k
    print "omega = %s " % wav.omega
    print "T     = %s " % wav.T
    print "C     = %s " % wav.C
    print "Cg    = %s " % wav.Cg
    print "G     = %s " % wav.G
    #print "  = %s " % wav.G
    #print "  = %s " % wav.Ks
    #print "  = %s " % wav.Kr
    #print "  = %s " % wav.theta
    #print "  = %s " % wav.H