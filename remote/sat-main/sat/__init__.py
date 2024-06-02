import argparse
from sgp4.api import Satrec
from sgp4.api import jday
import astropy.time
from astropy.time import Time
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
from astropy import units as u

from time import sleep



def main():
    parser = argparse.ArgumentParser(
        prog=__name__,
        description="What the program does",
        epilog="Text at the bottom of help",
    )

    args = parser.parse_args()
    
    while True:

        # FUNCUBE-1 (AO-73) update 2024-06-01
        s = '1 39444U 13066AE  24153.45272835  .00005531  00000+0  54051-3 0  9992'
        t = '2 39444  97.7185 112.8624 0047787 190.8992 169.1196 14.91906997567767'

        nt = Time.now() # XXX timezone?

        satellite = Satrec.twoline2rv(s, t)
        error_code, teme_p, teme_v = satellite.sgp4(nt.jd1, nt.jd2)

        teme_p = astropy.coordinates.CartesianRepresentation(teme_p*u.km)
        teme_v = astropy.coordinates.CartesianDifferential(teme_v*u.km/u.s)
        teme = TEME(teme_p.with_differentials(teme_v), obstime=nt)

        # EMF Camp 2024 EHLAB ground station
        location = astropy.coordinates.EarthLocation(lat=51.3833 * u.deg, lon=-2.7167 * u.deg, height=174 * u.m)
        itrs_geo = teme.transform_to(astropy.coordinates.ITRS(obstime=nt))
        topo_itrs_repr = itrs_geo.cartesian.without_differentials() - location.get_itrs(nt).cartesian
        itrs_topo = astropy.coordinates.ITRS(topo_itrs_repr, obstime = nt, location=location)
        altaz = itrs_topo.transform_to(astropy.coordinates.AltAz(obstime=nt, location=location))

        print(round(altaz.az.deg,3), round(altaz.alt.deg,3), flush=True) #azimuth, elevation
        sleep(5)

