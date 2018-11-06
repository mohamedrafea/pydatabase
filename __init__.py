from pydatabase.dimension.datetimeutil import DateTimeUtil
from pydatabase.dimension.time import Time
from pydatabase.dimension.month import Month
def testTimeDiff():
    print(DateTimeUtil.calcDiffInMinutes('2017-06-29 16:01:00','2017-06-29 16:00:00'))

def testMonthDiff():
    m1 = Month.createMonthFromYearAndMonth(2018,11)
    m2 = Month.createMonthFromYearAndMonth(2016, 9)
    print(m1.monthDiff(m2))
    print(m2.monthDiff(m1))
#testTimeDiff()
testMonthDiff()