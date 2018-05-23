# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.abspath(".."))
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic.settings")
application = get_wsgi_application()
reload(sys)
from bus.models import OldmanTabGps
from classes.GPSTransform import GPSUtil
sys.setdefaultencoding("utf-8")

def main():
    gpsls=OldmanTabGps.objects.filter(latitude__gt=0.0).filter(bdlat__isnull=True).values_list('latitude','longtitude').distinct()
    gtools=GPSUtil()
    cnt=0
    for gps in gpsls:
        tmplat=float(gps[0])
        tmplng=float(gps[1])
        bdgps=gtools.wgs2bd(tmplat,tmplng)
        print tmplat,tmplng,bdgps
        if(bdgps is not None):
            OldmanTabGps.objects.filter(latitude=gps[0]).filter(longtitude=gps[1]).update(bdlat=bdgps['lat'],bdlon=bdgps['lon'])

if __name__ == "__main__":
    main()
    print('Done!')