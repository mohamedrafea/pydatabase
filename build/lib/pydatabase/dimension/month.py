# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 18:46:14 2017

@author: mohamed
"""

from sqlalchemy import Column, Integer, String

from pydatabase.table.tableobject import TableObject


class Month(TableObject,TableObject.Base):
	
	month_number = Column(Integer)
	year = Column(Integer)
	month_name = Column(String)
	month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
	month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

	@classmethod
	def createMonthFromYearAndMonth(cls,year,month_number):
		month = Month()
		month.year = year
		month.month_number = month_number
		month.month_name = cls.month_names[month_number]
		month.id = month.calcId()
		return month
	@classmethod
	def populateDimension(cls):
		startYear = 2010
		endYear = 2030
		for y in range(startYear,endYear+1):
			for m in range(1,13):
				month = cls.createMonthFromYearAndMonth(y,m)
				month.insert()
	def calcId(self):
		return int(str(self.year) + str(self.month_number).zfill(2))
	@classmethod
	def convertDatetimeToId(cls, timestamp):
		return cls.createFromDateTime(timestamp).id

	@classmethod
	def createFromId(cls, id):
		s = str(id)
		m = Month()
		m.id = id
		m.year = int(s[0:4])
		m.month_number = int(s[4:6])
		return m
	@classmethod
	def createFromDateTime(cls,timestamp):
		m = Month()
		m.year = timestamp.year
		m.month_number = timestamp.month
		m.id = m.calcId()
		return m

	def getNumberOfDays(self):
		if self.month_number==2 and (self.year % 4)==0:
			return 29
		return self.month_days[self.month_number]
	def getPreviousMonth(self):
		pm = Month()
		if self.month_number==1:
			pm.year = self.year-1
			pm.month_number = 12
		else:
			pm.year = self.year
			pm.month_number = self.month_number-1
		pm.id = pm.calcId()
		return pm

	@classmethod
	def fillDF(cls,df, fromMonth, toMonth, month_field, values):
		currentMonth = fromMonth
		while currentMonth.monthDiff(toMonth) <= 0:
			temp = df[df[month_field] == currentMonth.id]
			if temp.empty:
				valuesToInsert = [currentMonth.id]
				valuesToInsert.extend(values)
				df.loc[-1] = valuesToInsert
				df.index = df.index + 1
			currentMonth = currentMonth.getNextMonth()
		df.sort_values(month_field, inplace=True)
		return df

	def getNextMonth(self):
		return self.getFutureMonth(1)

	def getFutureMonth(self,increment):
		nm = Month()
		if self.month_number+increment > 12:
			nm.year = self.year + 1
			nm.month_number = self.month_number+increment-12
		else:
			nm.year = self.year
			nm.month_number = self.month_number + increment
		nm.id = nm.calcId()
		return nm
	#return +ve if month is earlier month
	def monthDiff(self,month):
		yearDiff = self.year - month.year
		d = yearDiff*12
		if self.month_number>=month.month_number:
			d += self.month_number - month.month_number
		else:
			d -= month.month_number - self.month_number
		return d