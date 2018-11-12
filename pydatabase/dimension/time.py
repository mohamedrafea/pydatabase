from sqlalchemy import Column, Integer

from pydatabase.table.tableobject import TableObject


class Time(TableObject, TableObject.Base):
    hour = Column(Integer)
    minute = Column(Integer)

    @classmethod
    def createTimeFromId(cls,id):
        t = Time()
        t.id = id
        s = str(id)
        if id<=59:
            t.hour = 0
        else:
            t.hour = int(s[0:len(s)-2])
        t.minute = int(s[len(s)-2:len(s)])
        return t

    @classmethod
    def createTimeFromTimeString(cls,s):
        id = cls.convertTimeStringToId(s)
        return cls.createTimeFromId(id)

    @classmethod
    def populateDimension(cls):
        for h in range(0, 24):
            for m in range(1, 60):
                time = Time()
                time.hour = h
                time.minute = m
                time.id = int(str(h)+str(m).zfill(2))
                time.insert()

    @classmethod
    def convertIdToTimeString(cls,id):
        s = str(id)
        second = '00'
        hour = s[0:len(s)-2].zfill(2)
        minute = s[len(s)-2:len(s)].zfill(2)
        return hour+':'+minute+':'+second

    @classmethod
    def convertDatetimeToId(cls, timestamp):
        s = str(timestamp.hour) + str(timestamp.minute).zfill(2)
        return int(s)

    @classmethod
    def convertTimestampToId(cls,timestamp):
        s = timestamp[11:16]
        return cls.convertTimeStringToId(s)

    @classmethod
    def convertTimeStringToId(cls, s):
        s2 = s.replace(':', '')
        return int(s2)

    # can return negative values to indicate a later time
    def calcDiffInMinutes(self, aTime):
        hourDiff = self.hour - aTime.hour
        minuteDiff = self.minute - aTime.minute
        diff = hourDiff * 60
        if hourDiff > 0 and minuteDiff < 0:
            diff -= 60
            minuteDiff += 60
        if hourDiff < 0 and minuteDiff > 0:
            diff += 60
            minuteDiff -= 60
        diff += minuteDiff
        return diff