# -*- coding: utf-8 -*-
'''
 * 各地图API坐标系统比较与转换;
 * WGS84坐标系：即地球坐标系，国际上通用的坐标系。设备一般包含GPS芯片或者北斗芯片获取的经纬度为WGS84地理坐标系,
 * 谷歌地图采用的是WGS84地理坐标系（中国范围除外）;
 * GCJ02坐标系：即火星坐标系，是由中国国家测绘局制订的地理信息系统的坐标系统。由WGS84坐标系经加密后的坐标系。
 * 谷歌中国地图和搜搜中国地图采用的是GCJ02地理坐标系; BD09坐标系：即百度坐标系，GCJ02坐标系经加密后的坐标系;
 * 搜狗坐标系、图吧坐标系等，估计也是在GCJ02基础上加密而成的。
'''
import math

PI=3.14159265358979324
RADII=6378245.0
EE=0.00669342162296594323
X_PI= PI * 3000.0 / 180.0

    
class GPSUtil(object):
    
    '''
    wgs84 to 百度坐标系
    
    @param lat
    @param lon
    @return
    '''
    def wgs2bd(self,lat,lon):
        gcj=self.wgs2gcj(lat, lon)
        if(gcj is None):
            return None
        bd=self.gcj2bd(gcj['lat'], gcj['lon'])
        return bd
    '''
    wgs84 to 火星坐标系 (GCJ-02) World Geodetic System ==> Mars Geodetic System
    
    @param lat
    @param lon
    @return
    '''
    
    def wgs2gcj(self,lat,lon):
        if(self.outOfChina(lat, lon)):
            return None
        dLat = self.transformLat(lon-105.0, lat-35.0)
        dLon = self.transformLon(lon-105.0, lat-35.0)
        radLat = lat / 180.0 * PI
        magic = math.sin(radLat)
        magic = 1 - EE * magic * magic;
        sqrtMagic = math.sqrt(magic);
        dLat = (dLat * 180.0) / ((RADII * (1 - EE)) / (magic * sqrtMagic) * PI)
        dLon = (dLon * 180.0) / (RADII / sqrtMagic * math.cos(radLat) * PI)
        mgLat = lat + dLat
        mgLon = lon + dLon
        return {'lat':mgLat, 'lon':mgLon}
    
    '''
    火星坐标系 (GCJ-02) to wgs84 
    @param lon 
    @param lat  
    @return
    '''
    def gcj2wgs(self,lat,lon):
        gps=self.transform(lat, lon)
        lontitude=lon*2-gps['lon']
        latitude=lat*2-gps['lat']
        return {'lat':latitude,'lon':lontitude}
    
    '''
    * 火星坐标系 (GCJ-02) 与百度坐标系 (BD-09) 的转换算法 将 GCJ-02 坐标转换成 BD-09 坐标
    *
     @param gg_lat
     @param gg_lon
    '''
    def gcj2bd(self,gg_lat,gg_lon):
        x=gg_lon
        y=gg_lat
        z=math.sqrt(x*x+y*y)+ 0.00002 * math.sin(y * X_PI)
        theta=math.atan2(y, x)+0.000003 *math.cos(x*X_PI)
        bd_lon=z*math.cos(theta)+0.0065
        bd_lat=z*math.sin(theta)+0.006
        return {'lat':bd_lat,'lon':bd_lon}
        
    '''
    火星坐标系 (GCJ-02) 与百度坐标系 (BD-09) 的转换算法 
    将 BD-09 坐标转换成GCJ-02 坐标 
     @param bd_lat 
     @param bd_lon 
    @return
    '''   
    def bd2gcj(self,bd_lat,bd_lon):
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PI)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * PI)
        gg_lon = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return {'lat':gg_lat,'lon': gg_lon}
    
    '''
    BD-09——>wgs84
    @param bd_lat
    @param bd_lon
    @return:  
    '''
    def bd2wgs(self,bd_lat,bd_lon):
        gcj=self.bd2gcj(bd_lat, bd_lon)
        map84=self.gcj2wgs(gcj['lat'], gcj['lon'])
        return map84
    
    '''
    判断是否国内坐标
    @param lat
    @param lon
    @return: True or False 
    '''
    def outOfChina(self,lat, lon):
        if (lon < 72.004 or lon > 137.8347):  
            return True
        if (lat < 0.8293 or lat > 55.8271):  
            return True 
        return False
    '''
    坐标转换
    @param lat
    @param lon
    @return:  
    '''
    def transform(self,lat,lon):
        if (self.outOfChina(lat, lon)):
            return None
        dLat = self.transformLat(lon - 105.0, lat - 35.0);
        dLon = self.transformLon(lon - 105.0, lat - 35.0);
        radLat = lat / 180.0 * PI;
        magic = math.sin(radLat);
        magic = 1 - EE * magic * magic;
        sqrtMagic = math.sqrt(magic);
        dLat = (dLat * 180.0) / ((RADII * (1 - EE)) / (magic * sqrtMagic) * PI);
        dLon = (dLon * 180.0) / (RADII / sqrtMagic * math.cos(radLat) * PI);
        mgLat = lat + dLat;
        mgLon = lon + dLon;
        return {'lat':mgLat, 'lon':mgLon}
    
    
    '''
    纬度坐标转换
    @param x
    @param y
    @return:  
    '''    
    
    def transformLat(self,x,y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y+ 0.2 * math.sqrt(math.fabs(x))
        ret+= (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
        return ret
    
        '''
    经度坐标转换
    @param x
    @param y
    @return:  
    ''' 
    def transformLon(self,x,y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1* math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0* PI)) * 2.0 / 3.0
        return ret