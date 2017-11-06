# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime
import re, os


month_dict = {u"Ocak" : 1,
u"Şubat" : 2,u"Mart" : 3,u"Nisan" : 4,
u"Mayıs" : 5,u"Haziran" : 6,u"Temmuz" : 7,u"Ağustos" : 8,
u"Eylül" : 9,u"Ekim" : 10, u"Kasım" : 11,u"Aralık" : 12}


class DBWriter:
    regex_list = []
    def convert_dates(self,dttm):
        # inputs:: dttm: dataframe of datetime
        # output:: dataframe of processed datetime
        year,month,day,time = (re.findall(reg,dttm,flags=re.U) for reg in self.regex_list)
        print dttm
        if dttm:
            if re.search("[^\W0-9]+",month[0],flags=re.U):
                month = [str(month_dict[month[0]])]
            if not time:
                time = ['00:00']
            date_time = "-".join(year + month + day) + "T" + time[0]
            if not day:
                day = [dttm[:2].strip()]
            print day
        else: date_time = dttm

        return date_time

    def clean_raw_data(self,datapath):
        # inputs:: datapath: path of the json file of crawl outputs
        # output:: rawdata of crawl outputs
        rawdata = pd.read_json(datapath)
        rawdata = rawdata[rawdata["content"]!=""]
        rawdata["date_time"] = pd.to_datetime([self.convert_dates(d) for d in rawdata["date_time"]])
        # rawdata["date_time"] = pd.to_datetime(self.convert_dates(rawdata["date_time"]))
        return rawdata

    def convert_to_relationaldb(self,rawdata):
        # inputs:: dataframe of crawl outputs
        source  = rawdata["source"].tolist()[0]
        lang    = rawdata["lang"].tolist()[0]
        engine  = create_engine('sqlite:///hurriyet.db')
        sources = pd.read_sql("SELECT * FROM Source",engine)
        langs   = pd.read_sql("SELECT * FROM Lang",engine)
        src_ind = sources[sources["source"]==source]["index"].tolist()
        lng_ind = langs[langs["lang"]==lang]["index"].tolist()
        # lng_ind = sources[langs.ix[:,1]==lang][0].tolist()
        print src_ind, lng_ind
        if src_ind:
            rawdata["source"] = src_ind[0]
        else:
            nline = pd.DataFrame([sources.tail(1)["index"].tolist()[0] + 1, source]).transpose()
            nline.columns = ["index","source"]
            sources = pd.concat([sources,nline],axis=0)
            sources.to_sql("Source",engine,if_exists="replace",index=False)

        if lng_ind:
            rawdata["lang"] = lng_ind[0]
        else:
            nline = pd.DataFrame([langs.tail(1)["index"].tolist()[0] + 1, lang]).transpose()
            nline.columns = ["index","lang"]
            langs = pd.concat([langs,nline],axis=0)
            langs.to_sql("Lang",engine,if_exists="replace",index=False)

        return rawdata


    def writer(self,cleandata):
        # inputs:: cleaned dataframe of news
        engine = create_engine('sqlite:///hurriyet.db')
        cleandata.to_sql("News",engine,if_exists="append")

    def movedir(self,dataname):
        if not os.path.isdir("dataout/finished"): os.mkdir("dataout/finished")
        #
        os.rename("dataout/" + dataname , "dataout/finished/" + dataname)

    def execute(self,datapath):
        datname = datapath.split("/")[-1]
        rawdat = self.clean_raw_data(datapath)
        cleandat = self.convert_to_relationaldb(rawdat)
        self.writer(cleandat)
        self.movedir(datname)


class HurriyetColumnCleaner(DBWriter):
    regex_list = ["[0-9]{4}","\s([^\W0-9]+)","^([0-9]+)","[0-9]+:[0-9]{2}"]


class YenisafakCleaner(DBWriter):
    regex_list = ["[0-9]{4}$","\s([^\W0-9]+)","\s([0-9]{2}),","[0-9]+:[0-9]{2}"]

class WiredCleaner(DBWriter):
    regex_list = [""]
    def clean_raw_data(self,datapath):
        # inputs:: datapath: path of the json file of crawl outputs
        # output:: rawdata of crawl outputs
        rawdata = pd.read_json(datapath)
        rawdata = rawdata[(rawdata["content"]!="") & (rawdata["title"]!="")]
        return rawdata

class MirrorCleaner(DBWriter):
    regex_list = [""]
    def clean_raw_data(self,datapath):
        # inputs:: datapath: path of the json file of crawl outputs
        # output:: rawdata of crawl outputs
        rawdata = pd.read_json(datapath)
        rawdata = rawdata[(rawdata["content"]!="") & (rawdata["title"]!="")]
        return rawdata

class IndependentCleaner(DBWriter):
    regex_list = ["[0-9]{4}$","\s([0-9]+)","\s([0-9]{2}),","[0-9]+:[0-9]{2}"]

class OldCleaner(DBWriter):
    regex_list = [""]
    def clean_raw_data(self,datapath):
        # inputs:: datapath: path of the json file of crawl outputs
        # output:: rawdata of crawl outputs
        rawdata = pd.read_json(datapath)
        rawdata.columns = ['author','category','content','date_time','id','lang','slug','source','title','link']
        intros = pd.DataFrame(np.repeat("",rawdata.shape[0]))
        intros.columns = ["intro"]
        rawdata = pd.concat([rawdata,intros],axis=1)
        rawdata = rawdata[['author','category','content','date_time','intro','lang','link','source','title']]
        rawdata = rawdata[(rawdata["content"]!="") & (rawdata["title"]!="")]
        return rawdata


class HurriyetColumnCleaner(DBWriter):
    regex_list = ["[0-9]{4}$","\s([^\W0-9]+)","\s([0-9]{2}),","[0-9]+:[0-9]{2}"]

