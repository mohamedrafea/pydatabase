import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean

from pydatabase.dimension.month import Month
from pydatabase.table.tableobjectnoid import TableObjectNoID
from datetime import datetime
from datetime import timedelta

class Date(TableObjectNoID, TableObjectNoID.Base):
    id = Column(Integer,primary_key=True)
    dateString = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    day_name = Column(String)
    week = Column(Integer)
    month_name = Column(String)
    quarter = Column(Integer)
    year_half = Column(Integer)
    isHoliday = Column(Boolean,default=False)
    holidayName = Column(String)

    @classmethod
    def convertIdToDateString(cls,id):
        s = str(id)
        year = int(s[0:4])
        month = int(s[4:6])
        day = int(s[6:8])
        return cls.toDateString(year,month,day)
    def calcId(self):
        s = str(self.year) + str(self.month).zfill(2) + str(self.day).zfill(2)
        return int(s)
    @classmethod
    def convertIdToMonthId(cls,id):
        mid = str(id)[0:6]
        return int(mid)

    @classmethod
    def createDateFromId(cls,id):
        d = Date()
        d.id = id
        s = str(id)
        d.year = int(s[0:4])
        d.month = int(s[4:6])
        d.day = int(s[6:8])
        d.updateDateString()
        return d

    #return negative in case of a later date
    def calcDiffInDays(self,aDate):
        yearDiff = self.year - aDate.year
        monthDiff = self.month - aDate.month
        daysDiff = self.day - aDate.day
        diff = yearDiff*365
        if yearDiff>0 and monthDiff<0:
            diff -= 365
            monthDiff += 12
        if yearDiff<0 and monthDiff>0:
            diff += 365
            monthDiff -= 12
        diff += monthDiff * 30
        if monthDiff>0 and daysDiff<0:
            diff -= 30
            daysDiff += 30
        if monthDiff<0 and daysDiff>0:
            diff += 30
            daysDiff -= 30
        diff += daysDiff
        return diff


    @classmethod
    def createDateFromMonthAndDay(cls,month,day):
        d = Date()
        d.year = month.year
        d.month = month.month_number
        d.day = day
        d.id = d.calcId()
        d.updateDateString()
        return d
    @classmethod
    def createFirstAndLastMonthDates(cls,month):
        first = cls.createDateFromMonthAndDay(month,1)
        last = cls.createDateFromMonthAndDay(month,month.getNumberOfDays())
        return first,last

    def updateDateString(self):
        self.dateString = self.toDateString(self.year,self.month,self.day)
    @classmethod
    def toDateString(cls,year,month,day):
        s = str(year)+"-"
        if month<10:
            s = s + '0'+str(month)
        else:
            s = s + str(month)
        s = s + '-'
        if day<10:
            s = s + '0'+str(day)
        else:
            s = s + str(day)
        return s
    @classmethod
    def convertDatetimeToId(cls,timestamp):
        d = Date()
        d.year = timestamp.year
        d.month = timestamp.month
        d.day = timestamp.day
        return d.calcId()

    @classmethod
    def createDateFromDateTime(cls, timestamp):
        id = cls.convertTimestampToId(timestamp)
        return cls.createDateFromId(id)
    @classmethod
    def createDateFromDateString(cls,timestamp):
        return cls.createDateFromId(cls.convertTimestampToId(timestamp))
    @classmethod
    def convertTimestampToId(cls,timestamp):
        s = timestamp[0:10]
        s2 = s.replace('-','')
        return int(s2)
    @classmethod
    def createDateFromSeconds(cls,sec):
        dt = datetime(1970, 1, 1) + timedelta(seconds=sec)
        d = Date()
        d.year = dt.year
        d.month = dt.month
        d.day = dt.day
        d.id = d.calcId()
        d.updateDateString()
        return d

    @classmethod
    def populateDimension(cls):
        start = '2010-01-01'
        end = '2030-12-31'
        df = pd.DataFrame({"Date": pd.date_range(start, end)})
        df["day"] = df.Date.dt.day
        df["day_name"] = df.Date.dt.weekday_name
        #week starts Sunday
        df['week'] = df.Date.dt.strftime('%U')
        df["month"] = df.Date.dt.month
        df["month_name"] = df['month'].apply(Month.getMonthName)
        df["quarter"] = df.Date.dt.quarter
        df["year"] = df.Date.dt.year
        df["year_half"] = (df.quarter + 1) // 2
        df.insert(0, 'id', (df.year.astype(str) + df.month.astype(str).str.zfill(2) + df.day.astype(str).str.zfill(2)).astype(int))
        df.rename(columns={'Date': 'dateString'}, inplace=True)
        print(df.head())
        print(df.tail())
        cls.savePandasDataframe(df)
