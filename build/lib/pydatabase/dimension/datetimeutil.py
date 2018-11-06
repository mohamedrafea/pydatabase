from pydatabase.common import Common
import datetime
from pydatabase.dimension.date import Date
from pydatabase.dimension.time import Time
class DateTimeUtil(Common):

    def __init__(self,dateId,timeId):
        self.dateId = dateId
        self.timeId = timeId

    #>0 in case later than
    #<0 in case less than
    #0 in case equal
    def compare(self,dateId,timeId):
        if self.dateId>dateId:
            return 1
        if self.dateId<dateId:
            return -1
        #both dates are equal
        if self.timeId>timeId:
            return 1
        if self.timeId < timeId:
            return -1
        return 0

    @classmethod
    def convertUnixTimestampToDateTime(cls,timestamp):
        return datetime.datetime.fromtimestamp(timestamp)

    @classmethod
    #if dateTime1 is later than dateTime2, return positive number
    def calcDiffInMinutes(cls,dateTime1,dateTime2):
        d1 = Date.createDateFromDateString(dateTime1[0:10])
        t1 = Time.createTimeFromTimeString(dateTime1[11:16])
        d2 = Date.createDateFromDateString(dateTime2[0:10])
        t2 = Time.createTimeFromTimeString(dateTime2[11:16])
        daysDiff = d1.calcDiffInDays(d2)
        minutesDiff = t1.calcDiffInMinutes(t2)
        return minutesDiff + (daysDiff*24*60)
