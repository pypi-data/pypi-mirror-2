#Copyright 2010 Erik Tollerud
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


"""
This module contains tools and utilities for computing ephemerides of solar
system objects, as well as proper motion calculations for extrasolar objects.

.. warning::
    This module is currently being re-worked and has incomplete/possibly 
    incorrect functionality

.. seealso::
        
    `Pyephem <http://rhodesmill.org/pyephem/>`_
        A Pythonic implementation of the 
        `xephem <http://www.clearskyinstitute.com/xephem/>`_ ephemerides 
        algorithms. 
        
    `Meeus, Jean H. "Astronomical Algorithms" ISBN 0943396352 <http://www.willbell.com/MATH/mc1.htm>`_ 
        An authoritative reference on coordinates, ephemerides, and related
        transforms in astronomy.
        
    `JPL Solar System Dynamics Group <http://ssd.jpl.nasa.gov/>`_
        The standard source for solar system dynamics and ephemerides.  Source 
        of DE200 and DE405 solar system models, and HORIZON ephemerides service.

.. todo:: Tutorials

Classes and Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. inheritance-diagram:: astropysics.coords.ephems
   :parts: 1
   
Module API
^^^^^^^^^^

"""

#TODO: JPL Ephemeris and default ephemeris setting functions

#useful references:
#*http://www.astro.rug.nl/software/kapteyn/index.html
#*"Astronomical Algorithms" by Jean Meeus 
#*"The IAU Resolutions on Astronomical Reference Systems,Time Scales, and Earth 
#  Rotation Models": http://aa.usno.navy.mil/publications/docs/Circular_179.pdf
from __future__ import division,with_statement

from ..constants import pi
from ..utils import DataObjectRegistry
import numpy as np

from .coordsys import EquatorialCoordinatesEquinox as EquatorialCoordinates

_twopi = 2*pi

try:
    #requires Python 2.6
    from abc import ABCMeta
    from abc import abstractmethod
    from abc import abstractproperty
    from collections import Sequence,MutableSequence
except ImportError: #support for earlier versions
    abstractmethod = lambda x:x
    abstractproperty = property
    ABCMeta = type
    class MutableSequence(object):
        __slots__=('__weakref__',) #support for weakrefs as necessary
    class Sequence(object):
        __slots__=('__weakref__',) #support for weakrefs as necessary
        
        
#<----------Lunisolar/SS fundamental arguments for coords via SOFA------------->
#TODO: eventually replace with objects that return the proper thing?

_mean_anomaly_of_moon_poly = np.poly1d([-0.00024470,
                                        0.051635,
                                        31.8792,
                                        1717915923.2178,
                                        485868.249036])
def _mean_anomaly_of_moon(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean anomaly of the moon  in radians
    """
    from ..constants import asecperrad
    return np.fmod(_mean_anomaly_of_moon_poly(T)/asecperrad,_twopi)

_mean_anomaly_of_sun_poly = np.poly1d([-0.00001149,
                                       0.000136,
                                       -0.5532,
                                       129596581.0481,
                                       1287104.793048])
def _mean_anomaly_of_sun(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean anomaly of the sun  in radians
    """
    from ..constants import asecperrad
    return np.fmod(_mean_anomaly_of_sun_poly(T)/asecperrad,_twopi)
   
_mean_long_of_moon_minus_ascnode_poly = np.poly1d([0.00000417,
                                              -0.001037,
                                              -12.7512,
                                              1739527262.8478,
                                              335779.526232])
def _mean_long_of_moon_minus_ascnode(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean logitude of the Moon minus the ascending node in radians
    
    """
    from ..constants import asecperrad
    return np.fmod(_mean_long_of_moon_minus_ascnode_poly(T)/asecperrad,_twopi)

_mean_elongation_of_moon_from_sun_poly = np.poly1d([-0.00003169,
                                                    0.006593,
                                                    -6.3706,
                                                    1602961601.2090,
                                                    1072260.703692])
def _mean_elongation_of_moon_from_sun(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean elongation of the Moon from the Sun in radians
    """
    from ..constants import asecperrad
    return np.fmod(_mean_elongation_of_moon_from_sun_poly(T)/asecperrad,_twopi)

_mean_long_ascnode_moon_poly = np.poly1d([-0.00005939,
                                          0.007702,
                                          7.4722,
                                          -6962890.5431,
                                          450160.398036])
def _mean_long_asc_node_moon(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean longitude of the Moon's ascending node in radians 
    """
    from ..constants import asecperrad
    return np.fmod(_mean_long_ascnode_moon_poly(T)/asecperrad,_twopi)
   
def _long_venus(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean longitude of Venus in radians
    """
    return np.fmod(3.176146697 + 1021.3285546211*T,_twopi)
   
def _long_earth(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: Mean longitude of Earth in radians
    """
    return np.fmod(1.753470314 + 628.3075849991*T,_twopi)

def _long_prec(T):
    """
    From SOFA (2010) - IERS 2003 conventions
    
    :param T: Julian centuries from 2000.0 in TDB (~TT for this function)
    :type T: float or array-like
    
    :returns: General accumulated precession in longitude in radians
    """
    return (0.024381750 + 0.00000538691*T)*T

class EphemerisAccuracyWarning(Warning):
    """
    Class for warnings due to Ephemeris accuracy issues
    """
    
class EphemerisObject(object):
    """
    An object that can be used to generate positions on the sky for a given 
    date and time as dictated by the :attr:`jd` attribute.
    
    :meth:`equatorialCoordinates` must be overridden.
    """
    
    __metaclass__ = ABCMeta
    
    name = '' #put here so it ends up in autogenerated documentation
    
    def __init__(self,name,jd0=None,validjdrange=None):
        self.name = name
        self.jd0 = EphemerisObject.jd2000 if jd0 is None else jd0
        self._jd = self._jd0
        self.validjdrange = validjdrange
    
    def _getJd0(self):
        return self._jd0
    def _setJd0(self,val):
        from operator import isSequenceType
        from ..obstools import calendar_to_jd
        from datetime import datetime
        
        if hasattr(val,'year') or isSequenceType(val):
            self._jd0 = calendar_to_jd(val)
        else:
            self._jd0 = val
    jd0 = property(_getJd0,_setJd0,doc="""
    The Epoch for this object - when :attr:`jd` equals this value, :attr:`d` is
    0. Can be set as a decimal number, :class:`datetime.datetime` object, or a
    gregorian date tuple.
    """)
    
    
    def _getJd(self):
        return self._jd
    def _setJd(self,val):
        from operator import isSequenceType
        from ..obstools import calendar_to_jd
        from datetime import datetime
        
        if val == 'now':
            jd =  calendar_to_jd(datetime.utcnow(),tz=None)
        elif hasattr(val,'year') or isSequenceType(val):
            jd = calendar_to_jd(val)
        else:
            jd = val
        if self._validrange is not None:
            from warnings import warn
            if jd < self._validrange[0]:
                warn('JD {0} is below the valid range for this EphemerisObject'.format(jd),EphemerisAccuracyWarning)
            elif jd > self._validrange[1]:
                warn('JD {0} is above the valid range for this EphemerisObject'.format(jd),EphemerisAccuracyWarning)
        self._jd = jd
        
    jd = property(_getJd,_setJd,doc="""
    Julian Date at which to calculate the orbital elements. Can be set either as
    a scalar JD, 'now', :class:`datetime.datetime` object or a compatible tuple.
    """)
    
    def _getD(self):
        return self._jd - self._jd0
    def _setD(self,val):
        self._jd = val + self._jd0
    d = property(_getD,_setD,doc='the julian date offset by the epoch')
    
    def _getValidjdrange(self):
        if self._validrange is None:
            return (None,None)
        else:
            return self._validrange
    def _setValidjdrange(self,val):
        if val is None:
            self._validrange = None
        else:
            v1,v2 = val
            if v1 is None and v2 is None:
                self._validrange = None
            else:
                from operator import isSequenceType
                from ..obstools import calendar_to_jd
                from datetime import datetime
                
                vs = []
                for v in (v1,v2):
                    if v is None:
                        vs.append(None)
                    elif v == 'now':
                        vs.append(calendar_to_jd(datetime.utcnow(),tz=None))
                    elif hasattr(val,'year') or isSequenceType(val):
                        vs.append(calendar_to_jd(val))
                    else:
                        vs.append(val)
                self._validrange = tuple(vs)
    validjdrange = property(_getValidjdrange,_setValidjdrange,doc="""
    The range of jds over which these Ephemerides are valid. Should be a 2-tuple
    set as the :attr:`jd` attribute indicating (minjd,maxjd). Either can be None
    to indicate no bound.  If set to None, the result will be (None,None)
    """)
    
    @abstractmethod    
    def equatorialCoordinates(self):
        """
        Returns the equatorial coordinates of this object at the current
        date/time as a :class:`EquatorialCoordinates` object.
        
        Must be overridden in subclasses.
        """
        raise NotImplementedError
    
    def radecs(self,ds,usejd=False):
        """
        Generates an array of RAs and Decs for a set of input julian dates. `ds`
        must be a sequence of objects that can be set to `d` or `jd`.
        
        If `usejd` is True, the inputs are interpreted as Julian Dates without
        the epoch offset. Otherwise, they are interpreted as offsets from `jd0`.
        
        Returns a 2xN array with the first column RA and the second Dec in
        degrees.
        """
        
        oldjd = self._jd
        try:
            ra = []
            dec = []
            for d in ds:
                if usejd:
                    self.jd = d
                else:
                    self.d = d
                    
                eqpos = self.equatorialCoordinates()
                ra.append(eqpos.ra.d)
                dec.append(eqpos.dec.d)
                
            return np.array((ra,dec))
        finally:
            self._jd = oldjd
            
class SolarSystemObject(EphemerisObject):
    """
    A :class:`EphemerisObject` that can be interpreted as an object in the Solar
    System.  
    
    :meth:`cartesianCoordinates` must be overridden in subclasses.
    """
    
    def _obliquity(self,jd):
        """
        obliquity of the Earth/angle of the ecliptic in degrees
        
        the input `jd` is the actual Julian Day, *not* the offset `d` used for
        the orbital elements
        """
        #TODO: eventually pull this from Ecliptic coordinate transform
        return 23.4393 - 3.563E-7 * (jd - KeplerianOrbit.jd2000)
    
    @abstractmethod
    def cartesianCoordinates(self,geocentric=False):
        """
        Returns the ecliptic rectangular coordinates of this object
        at the current date/time as an (x,y,z) tuple (in AU).
        
        If `geocentric` is True, return geocentric coordinates.  Otherwise, 
        heliocentric.
        """
        raise NotImplementedError
    
    def equatorialCoordinates(self):
        """
        Returns the equatorial coordinates of this object at the current
        date/time as a :class:`EquatorialCoordinates` object for the epoch at which
        they are derived.
        """
        from math import radians,degrees,cos,sin,atan2,sqrt
        from ..obstools import jd_to_epoch
        
        
        if hasattr(self,'_eqcache') and self._eqcache[0] == self._jd:
            return EquatorialCoordinates(*self._eqcache[1:],**dict(epoch=jd_to_epoch(self._jd)))
        
        jd = self.jd
        
        eclr = radians(self._obliquity(jd))
        
        #heliocentric coordinates
        xh,yh,zh = self.cartesianCoordinates()
        
        #get Earth position - from the Sun ephemeris
        xs,ys,zs = _earth_coords(jd)
        
        #switch to geocentric coordinates
        xg = xh - xs
        yg = yh - ys
        zg = zh - zs
        
        #finally correct for obliquity to get equatorial coordinates
        cecl = cos(eclr)
        secl = sin(eclr)
        x = xg
        y = cecl*yg - secl*zg
        z = secl*yg + cecl*zg
        
        ra = degrees(atan2(y,x))
        dec = degrees(atan2(z,sqrt(x*x+y*y)))
        
        #cache for faster retrieval if JD is not changed
        self._eqcache = (self._jd,ra,dec)
        return EquatorialCoordinates(ra,dec,epoch=jd_to_epoch(self._jd))
    
    def phase(self,perc=False):
        """
        Compute the phase of this object - 0 is "new", 1 is "full".
        
        if `perc` is True, returns percent illumination.
        """
        from math import sqrt
        
        xh,yh,zh = self.cartesianCoordinates()
        
        xs,ys,zs = _earth_coords(jd)
        
        xg = xh - xs
        yg = yh - ys
        zg = zh - zs
        
        r = sqrt(xh*xh+yh*yh+zh*zh)
        R = sqrt(xg*xg+yg*yg+zg*zg)
        s = sqrt(xs*xs+ys*ys+zs*zs)
        
        phase = (1+(r*r + R*R - s*s)/(2*r*R))/2
        
        if perc:
            return 100*phase
        else:
            return phase
    
class KeplerianOrbit(SolarSystemObject):
    """
    An object with orbital elements (probably a solar system body) that can be
    used to construct ephemerides.
    
    The orbital elements are accessible as properties, computed for a Julian
    Date given by the :attr:`jd` attribute. They can also be set to a function
    of the form `element(d)`, where `d` is the offset from `jd0`. Alternatively,
    subclasses may directly override the orbital elements with their own custom
    properties that should return orbital elements at time `d`. The primary
    orbital elements are:
    
    * :attr:`e`
        ellipticity 
    * :attr:`a`
        semimajor axis (AU)
    * :attr:`i` 
        is the orbital inclination (degrees)
    * :attr:`N` 
        is the longitude of the ascending node (degrees)
    * :attr:`w` 
        is the argument of the perihelion (degrees)
    * :attr:`M`
        is the mean anamoly (degrees)
    
    Note that the default algorithms used here (based on heavily modified
    versions of `these methods <http://stjarnhimlen.se/comp/ppcomp.html>`_) are
    only accurate to ~ 1 arcmin within a millenium or so of J2000, but are
    computationally quite fast and simple.
    """
    jd2000 = 2451545.0
    
    def __init__(self,name,e,a,i,N,w,M,jd0=None,jdnow=None):
        """
        Generates an object with orbital elements given a generator 
        
        Arguments for these orbital elements can be either fixed values or
        functions of the form f(jd-jd0) that return the orbital element as a
        function of Julian Day from the epoch
        
        `name` is a string describing the object `jd0` is the epoch for these
        orbital elements (e.g. where their input functions are 0). To use raw
        JD, set this to 0. If None, it defaults to J2000
        
        `jdnow` can be used to set the initial JD.  If None, it will be the same
        as `jd0`
        """
        if jd0 is None:
            jd0 = EphemerisObject.jd2000 - 0.5
        EphemerisObject.__init__(self,name,jd0)
        
        self.e = e
        self.a = a
        self.i = i
        self.N = N
        self.w = w
        self.M = M
        self.name = name
        
        self.jd0 = jd0
        self._jd = jd0
        if jdnow is None:
            self._jd = jd0
        else:
            self.jd = jdnow
        
    
    #primary orbital elements
    def _getE(self):
        return self._e(self.d)
    def _setE(self,val):
        if callable(val):
            self._e = val
        else:
            self._e = lambda d:val
    e = property(_getE,_setE,doc='orbital eccentricity')
    
    def _getA(self):
        return self._a(self.d)
    def _setA(self,val):
        if callable(val):
            self._a = val
        else:
            self._a = lambda d:val
    a = property(_getA,_setA,doc='semi-major axis (au)')
    
    def _getI(self):
        return self._i(self.d)
    def _setI(self,val):
        if callable(val):
            self._i = val
        else:
            self._i = lambda d:val
    i = property(_getI,_setI,doc='inclination (degrees)')
    
    def _getN(self):
        return self._N(self.d)
    def _setN(self,val):
        if callable(val):
            self._N = val
        else:
            self._N = lambda d:val
    N = property(_getN,_setN,doc='Longitude of the ascending node (degrees)')
    
    def _getW(self):
        return self._w(self.d)
    def _setW(self,val):
        if callable(val):
            self._w = val
        else:
            self._w = lambda d:val
    w = property(_getW,_setW,doc='Argument of the perihelion (degrees)')
    
    def _getM0(self):
        return self._M0(self.d)
    def _setM0(self,val):
        if callable(val):
            self._M0 = val
        else:
            self._e = lambda d:val
    M0 = property(_getM0,_setM0,doc='Mean anamoly (degrees)')
    
    #secondary/read-only orbital elements
    
    @property
    def lw(self):
        """
        longitude of the perihelion (degrees): :math:`N + w`
        """
        return self.N + self.w
    
    @property
    def L(self):
        """
        mean longitude: (degrees):math:`M + lw`
        """
        return self.M + self.N + self.w
    
    @property
    def dperi(self):
        """
        distance at perihelion (AU): :math:`a(1-e)`
        """
        return self.a*(1 - self.e)
    
    @property
    def dapo(self):
        """
        distance at apohelion (AU): :math:`a(1+e)`
        """
        return self.a*(1 + self.e)
    
    @property
    def P(self):
        """
        orbital period (years): :math:`a^{3/2}`
        """
        return self.a**1.5
    
    @property
    def T(self):
        """
        time of perihelion (in *offset* JD i.e. `d`)
        """
        return - self.M/(self.P*360.0)
    
    @property
    def Eapprox(self):
        """
        *approximate* Eccentric anamoly - faster than proper numerical solution
        of the E-M relation, but lower precision
        """
        from math import radians,sin,cos,degrees
        Mr = radians(self.M)
        e = self.e
        return degrees(Mr + e*sin(Mr)*(1.0 + e*cos(Mr)))
            
    @property
    def vapprox(self):
        """
        *approximate* Eccentric anamoly - faster than proper numerical solution
        of the E-M relation, but lower precision
        """
        from math import radians,sin,cos,atan2,sqrt,degrees
        
        Mr = radians(self.M)
        e = self.e
        
        E = Mr + e*sin(Mr)*(1.0 + e*cos(Mr))
        xv = cos(E) - e
        yv = sqrt(1.0 - e*e) * sin(E)
        
        return degrees(atan2(yv,xv))
    
    def cartesianCoordinates(self,geocentric=False):
        """
        Returns the heliocentric ecliptic rectangular coordinates of this object
        at the current date/time as an (x,y,z) tuple (in AU)
        """
        from math import radians,degrees,cos,sin,atan2,sqrt
        
        #now get the necessary elements
        Mr = radians(self.M)
        wr = radians(self.w)
        ir = radians(self.i)
        Nr = radians(self.N)
        e = self.e
        a = self.a
        
        #compute coordinates
        #approximate eccentric anamoly
        E = Mr + e*sin(Mr)*(1.0 + e*cos(Mr))
        
        xv = a*(cos(E) - e)
        yv = a*(sqrt(1.0 - e*e) * sin(E))
        
        v = atan2(yv,xv)
        r = sqrt(xv*xv + yv*yv)
        
        sN = sin(Nr)
        cN = cos(Nr)
        si = sin(ir)
        ci = cos(ir)
        svw = sin(v + wr)
        cvw = cos(v + wr)
        
        #convert to heliocentric ecliptic coords
        xh = r*(cN*cvw - sN*svw*ci)
        yh = r*(sN*cvw + cN*svw*ci)
        zh = r*(svw*si)
        
        if geocentric:
            xg,yg,zg = _earth_coords(self._jd)
            return xh+xg,yh+yg,zh+zg
        else:
            return xh,yh,zh
    
    
class Sun(KeplerianOrbit):
    """
    This class represents the Sun's ephemeris.  Properly this is actually the 
    Earth's ephemeris, but it's still the way to get the on-sky location of the 
    sun
    """
    
    _validrange = (2415021.0,2488070.0)
    
    def __init__(self,jdordate=None):    
        """
        Initialize the object and optionally set the initial date with the 
        `jdordate` argument (by default this is J2000)
        """
        EphemerisObject.__init__(self,name='Sol',jd0=KeplerianOrbit.jd2000-0.5)
            
        if jdordate is None:
            self.jd = self.jd0 
        else:
            self.jd = jdordate
    
    @property
    def e(self):
        return 0.016709 - 1.151E-9 * self.d
    
    @property
    def a(self):
        return 1
    
    @property
    def i(self):
        return 0
    
    @property
    def N(self):
        return 0
    
    @property
    def w(self):
        return 282.9404 + 4.70935E-5 * self.d
    
    @property
    def M(self):
        return 356.0470 + 0.9856002585 * self.d
    
    def cartesianCoordinates(self,geocentric=False):
        """
        Returns the ecliptic coordinates of the Sun at the date/time given by
        :attr:`jd` as an (x,y,z) tuple (in AU) .
        """
        if geocentric:
            from ..obstools import jd_to_epoch
            from math import radians,cos,sin,atan2,sqrt
            
            #now get the necessary elements
            Mr = radians(self.M)
            wr = radians(self.w)
            e = self.e
            
            #compute coordinates
            #approximate eccentric anamoly
            E = Mr + e*sin(Mr)*(1.0 + e*cos(Mr))
            
            xv = cos(E) - e
            yv = sqrt(1.0 - e*e) * sin(E)
            
            v = atan2(yv,xv)
            r = sqrt(xv*xv + yv*yv)
            
            lsun = v + wr
            xs = r*cos(lsun)
            ys = r*sin(lsun)
            
            return xs,ys,0
        else:
            return 0,0,0
    
    def equatorialCoordinates(self):
        """
        Returns the equatorial coordinates of the Sun at the current date/time
        as a :class:`EquatorialCoordinates` object for the epoch at which they are
        derived.
        """
        from math import radians,degrees,cos,sin,atan2,sqrt
        from ..obstools import jd_to_epoch
        
        if hasattr(self,'_eqcache') and self._eqcache[0] == self._jd:
            return EquatorialCoordinates(*self._eqcache[1:],**dict(epoch=jd_to_epoch(self._jd)))
        
        xs,ys,zs = self.cartesianCoordinates(True) #geocentric location
        
        eclr = radians(self._obliquity(self.jd))
        
        x = xs
        y = ys*cos(eclr)  
        z = ys*sin(eclr)
        
        ra = degrees(atan2(y,x))
        dec = degrees(atan2(z,sqrt(x*x+y*y)))
        
        #cache for faster retrieval if JD is not changed
        self._eqcache = (self._jd,ra,dec)
        return EquatorialCoordinates(ra,dec,epoch=jd_to_epoch(self._jd))
    
    

class Moon(KeplerianOrbit):
    """
    Orbital Elements for Earth's Moon
    """
    
    _validrange = (2415021.0,2488070.0)
    
    def __init__(self,jd=None):    
        """
        Initialize the object and optionally set the initial Julian Date (by
        default this is J2000)
        """    
        EphemerisObject.__init__(self,name='Luna',jd0=KeplerianOrbit.jd2000-0.5)
        
        if jd is None:
            self.jd = self.jd0 
        else:
            self.jd = jd
        
    @property
    def e(self):
        return 0.054900
    
    @property
    def a(self):
        return 0.00256955
    
    @property
    def i(self):
        return 5.1454
    
    @property
    def N(self):
        return 125.1228 - 0.0529538083 * self.d
    
    @property
    def w(self):
        return 318.0634 + 0.1643573223 * self.d
    
    @property
    def M(self):
        return 115.3654 + 13.0649929509 * self.d
    
    
    
    def cartesianCoordinates(self,geocentric=False):
        """
        Returns the ecliptic coordinates of the Moon at the date/time given by
        :attr:`jd` as an (x,y,z) tuple (in AU) .
        """
        
        
        xg,yg,zg = KeplerianOrbit.cartesianCoordinates(self) #the orbital elements are for geocentric coordinates
        if geocentric:
            return xg,yg,zg
        else:
            xs,ys,zs = _sun_coords(jd)
            return xg-xs,yg-ys,zg-zs
    
    
    def phase(self,perc=False):
        """
        Compute the phase of the moon - 0 is "new", 1 is "full".
        
        if `perc` is True, returns percent illumination.
        """
        from math import sqrt,atan2,cos
        
        xg,yg,zg = self.cartesianCoordinates(True)
        sun = solsysobj['sun']
        oldsunjd = sun.jd
        sun.jd = self.jd
        xs,ys,zs = sun.cartesianCoordinates()
        sun.jd = oldsunjd
        
        longsun = atan2(ys,xs)
        longmoon = atan2(yg,xg)
        latmoon = atan2(zs,sqrt(xg*xg + yg*yg))
        
        phase = (1 + cos(longsun - longmoon)*cos(latmoon))/2
        
        if perc:
            return 100*phase
        else:
            return phase
        
#now generate the registry of solar system objects
solsysobjs = DataObjectRegistry('object',KeplerianOrbit)
solsysobjs['sun'] = Sun()
solsysobjs['moon'] = Moon()

#all of these from http://stjarnhimlen.se/comp/ppcomp.html#4
solsysobjs['mercury'] = KeplerianOrbit('Mercury',
                        e=lambda d: 0.205635 + 5.59E-10 * d,
                        a=0.387098,
                        i=lambda d: 7.0047 + 5.00E-8 * d,
                        N=lambda d: 48.3313 + 3.24587E-5 * d,
                        w=lambda d: 29.1241 + 1.01444E-5 * d,
                        M=lambda d: 168.6562 + 4.0923344368 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['mercury']._validrange = solsysobjs['sun']._validrange

solsysobjs['venus'] = KeplerianOrbit('Venus',
                        e=lambda d: 0.006773 - 1.302E-9 * d,
                        a=0.723330,
                        i=lambda d: 3.3946 + 2.75E-8 * d,
                        N=lambda d: 76.6799 + 2.46590E-5 * d,
                        w=lambda d: 54.8910 + 1.38374E-5 * d,
                        M=lambda d: 48.0052 + 1.6021302244 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['venus']._validrange = solsysobjs['sun']._validrange    

solsysobjs['mars'] = KeplerianOrbit('Mars',
                        e=lambda d: 0.093405 + 2.516E-9 * d,
                        a=1.523688,
                        i=lambda d: 1.8497 - 1.78E-8 * d,
                        N=lambda d: 49.5574 + 2.11081E-5 * d,
                        w=lambda d: 286.5016 + 2.92961E-5 * d,
                        M=lambda d: 18.6021 + 0.5240207766 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['mars']._validrange = solsysobjs['sun']._validrange

solsysobjs['jupiter'] = KeplerianOrbit('Jupiter',
                        e=lambda d: 0.048498 + 4.469E-9 * d,
                        a=5.20256,
                        i=lambda d: 1.3030 - 1.557E-7 * d,
                        N=lambda d: 100.4542 + 2.76854E-5 * d,
                        w=lambda d: 273.8777 + 1.64505E-5 * d,
                        M=lambda d: 19.8950 + 0.0830853001 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['jupiter']._validrange = solsysobjs['sun']._validrange

solsysobjs['saturn'] = KeplerianOrbit('Saturn',
                        e=lambda d: 0.055546 - 9.499E-9 * d,
                        a=9.55475,
                        i=lambda d: 2.4886 - 1.081E-7 * d,
                        N=lambda d: 113.6634 + 2.38980E-5 * d,
                        w=lambda d: 339.3939 + 2.97661E-5 * d,
                        M=lambda d:  316.9670 + 0.0334442282 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['saturn']._validrange = solsysobjs['sun']._validrange

solsysobjs['uranus'] = KeplerianOrbit('Uranus',
                        e=lambda d: 0.047318 + 7.45E-9 * d,
                        a=lambda d: 19.18171 - 1.55E-8 * d,
                        i=lambda d: 0.7733 + 1.9E-8 * d,
                        N=lambda d: 74.0005 + 1.3978E-5 * d,
                        w=lambda d: 96.6612 + 3.0565E-5 * d,
                        M=lambda d: 142.5905 + 0.011725806 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['uranus']._validrange = solsysobjs['sun']._validrange

solsysobjs['neptune'] = KeplerianOrbit('Neptune',
                        e=lambda d: 0.008606 + 2.15E-9 * d,
                        a=lambda d: 30.05826 + 3.313E-8 * d,
                        i=lambda d: 1.7700 - 2.55E-7 * d,
                        N=lambda d: 131.7806 + 3.0173E-5 * d,
                        w=lambda d: 272.8461 - 6.027E-6 * d,
                        M=lambda d: 260.2471 + 0.005995147 * d,
                        jd0=KeplerianOrbit.jd2000 - 0.5)
solsysobjs['neptune']._validrange = solsysobjs['sun']._validrange

def _earth_coords(jd):
    """
    Coordinates of the earth in heliocentric cartesian coordinates.  Can also
    be thought of as the negative of the sun coordinates in geocentric.
    """
    try:
        sun = solsysobjs['sun']
        oldsunjd = sun.jd
        sun.jd = self.jd
        xs,ys,zs = sun.cartesianCoordinates(True)
        return -xs,-ys,-zs
    finally:
        sun.jd = oldsunjd
    
