LOAD DATA INFILE 'C:\Ato\PycharmProjects\demo\xiamen_university_track_1001.csv'
INTO TABLE ato.mobile_data  character set utf8
FIELDS TERMINATED BY '\t'
OPTIONALLY ENCLOSED BY '"'
lines terminated by '\r\n'
ignore 1 lines
(MBKID,MBKNO,FLAG,STARTTIME,STARTLNG,STARTLAT,ENDTIME,ENDLNG,ENDLAT,PATHSTR,COSTTIME);