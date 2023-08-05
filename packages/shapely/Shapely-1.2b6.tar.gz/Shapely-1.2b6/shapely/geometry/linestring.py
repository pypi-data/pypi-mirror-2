"""Line strings and related utilities
"""

from ctypes import c_double, cast, POINTER
from ctypes import ArgumentError

from shapely.geos import lgeos
from shapely.geometry.base import BaseGeometry
from shapely.geometry.proxy import CachingGeometryProxy

__all__ = ['LineString', 'asLineString']


class LineString(BaseGeometry):
    """
    A one-dimensional figure comprising one or more line segments
    
    A LineString has non-zero length and zero area. It may approximate a curve
    and need not be straight. Unlike a LinearRing, a LineString is not closed.
    """

    def __init__(self, coordinates=None):
        """
        Parameters
        ----------
        coordinates : sequence
            A sequence of (x, y [,z]) numeric coordinate pairs or triples or
            an object that provides the numpy array interface, including another
            instance of LineString.

        Example
        -------
        Create a line with two segments

          >>> a = LineString([[0, 0], [1, 0], [1, 1]])
          >>> a.length
          2.0
        """
        BaseGeometry.__init__(self)
        self._init_geom(coordinates)

    def _init_geom(self, coordinates):
        if coordinates is None:
            # allow creation of null lines, to support unpickling
            pass
        else:
            self._geom, self._ndim = geos_linestring_from_py(coordinates)

    @property
    def __geo_interface__(self):
        return {
            'type': 'LineString',
            'coordinates': tuple(self.coords)
            }

    @property
    def ctypes(self):
        if not self._ctypes_data:
            self._ctypes_data = self.coords.ctypes
        return self._ctypes_data

    def array_interface(self):
        """Provide the Numpy array protocol."""
        return self.coords.array_interface()
    
    __array_interface__ = property(array_interface)

    # Coordinate access

    def _set_coords(self, coordinates):
        if self.is_empty:
            lgeos.GEOSGeom_destroy(self.__geom__)
            self.__geom__ = None
        if self._geom is None:
            self._init_geom(coordinates)
        update_linestring_from_py(self, coordinates)

    coords = property(BaseGeometry._get_coords, _set_coords)

    @property
    def xy(self):
        """Separate arrays of X and Y coordinate values
        
        Example:
        
          >>> x, y = LineString(((0, 0), (1, 1))).xy
          >>> list(x)
          [0.0, 1.0]
          >>> list(y)
          [0.0, 1.0]
        """
        return self.coords.xy
        

class LineStringAdapter(CachingGeometryProxy, LineString):

    context = None
    _owned = False

    def __init__(self, context):
        self.context = context
        self.factory = geos_linestring_from_py

    @property
    def _ndim(self):
        try:
            # From array protocol
            array = self.context.__array_interface__
            n = array['shape'][1]
            assert n == 2 or n == 3
            return n
        except AttributeError:
            # Fall back on list
            return len(self.context[0])

    @property
    def __array_interface__(self):
        """Provide the Numpy array protocol."""
        try:
            return self.context.__array_interface__
        except AttributeError:
            return self.array_interface()

    _get_coords = BaseGeometry._get_coords

    def _set_coords(self, ob):
        raise NotImplementedError(
            "Adapters can not modify their coordinate sources")

    coords = property(_get_coords)


def asLineString(context):
    """Adapt an object the LineString interface"""
    return LineStringAdapter(context)


def geos_linestring_from_py(ob, update_geom=None, update_ndim=0):
    try:
        # From array protocol
        array = ob.__array_interface__
        assert len(array['shape']) == 2
        m = array['shape'][0]
        if m < 2:
            raise ValueError(
                "LineStrings must have at least 2 coordinate tuples")
        try:
            n = array['shape'][1]
        except IndexError:
            raise ValueError(
                "Input %s is the wrong shape for a LineString" % str(ob))
        assert n == 2 or n == 3

        # Make pointer to the coordinate array
        try:
            cp = cast(array['data'][0], POINTER(c_double))
        except ArgumentError:
            cp = array['data']

        # Create a coordinate sequence
        if update_geom is not None:
            cs = lgeos.GEOSGeom_getCoordSeq(update_geom)
            if n != update_ndim:
                raise ValueError(
                "Wrong coordinate dimensions; this geometry has dimensions: %d" \
                % update_ndim)
        else:
            cs = lgeos.GEOSCoordSeq_create(m, n)

        # add to coordinate sequence
        for i in xrange(m):
            dx = c_double(cp[n*i])
            dy = c_double(cp[n*i+1])
            dz = None
            if n == 3:
                try:
                    dz = c_double(cp[n*i+2])
                except IndexError:
                    raise ValueError("Inconsistent coordinate dimensionality")

            # Because of a bug in the GEOS C API, 
            # always set X before Y
            lgeos.GEOSCoordSeq_setX(cs, i, dx)
            lgeos.GEOSCoordSeq_setY(cs, i, dy)
            if n == 3:
                lgeos.GEOSCoordSeq_setZ(cs, i, dz)

    except AttributeError:
        # Fall back on list
        m = len(ob)
        if m < 2:
            raise ValueError(
                "LineStrings must have at least 2 coordinate tuples")
        try:
            n = len(ob[0])
        except TypeError:
            raise ValueError(
                "Input %s is the wrong shape for a LineString" % str(ob))
        assert n == 2 or n == 3

        # Create a coordinate sequence
        if update_geom is not None:
            cs = lgeos.GEOSGeom_getCoordSeq(update_geom)
            if n != update_ndim:
                raise ValueError(
                "Wrong coordinate dimensions; this geometry has dimensions: %d" \
                % update_ndim)
        else:
            cs = lgeos.GEOSCoordSeq_create(m, n)
        
        # add to coordinate sequence
        for i in xrange(m):
            coords = ob[i]
            dx = c_double(coords[0])
            dy = c_double(coords[1])
            dz = None
            if n == 3:
                try:
                    dz = c_double(coords[2])
                except IndexError:
                    raise ValueError("Inconsistent coordinate dimensionality")
        
            # Because of a bug in the GEOS C API, 
            # always set X before Y
            lgeos.GEOSCoordSeq_setX(cs, i, dx)
            lgeos.GEOSCoordSeq_setY(cs, i, dy)
            if n == 3:
                lgeos.GEOSCoordSeq_setZ(cs, i, dz)
    
    if update_geom is not None:
        return None
    else:
        return lgeos.GEOSGeom_createLineString(cs), n

def update_linestring_from_py(geom, ob):
    geos_linestring_from_py(ob, geom._geom, geom._ndim)

# Test runner
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
