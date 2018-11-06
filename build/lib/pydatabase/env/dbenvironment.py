# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:24:22 2017

@author: mohamed
"""
from pydatabase.env.environment import Environment
class DBEnvironment(Environment):
    
    
	@classmethod
	def init(cls):
		cls.localEnv = DBEnvironment(Environment.ENV_LOCAL)
		cls.testingEnv = DBEnvironment(Environment.ENV_TESTING)
		cls.productionEnv = DBEnvironment(Environment.ENV_PRODUCTION)
		
	def __init__(self,env):
		Environment.__init__(self,env)
		self.user = self.getProperty('db:' + self.getName(), 'user')
		self.password = self.getProperty('db:' + self.getName(), 'password')
		self.db = self.getProperty('db:' + self.getName(), 'db')
		self.host = self.getProperty('db:' + self.getName(), 'host')
		self.port = self.getProperty('db:' + self.getName(), 'port')
		self.databaseType = self.getProperty('db:' + self.getName(), 'databaseType')
		print('env initialized:',self)
		"""
		if env==Environment.ENV_LOCAL:
			self.user=self.getProperty('db:'+self.getName(),)
			self.password='pocpass'
			self.db='racefoxstar'
			self.host='localhost'
			self.port=5432
			self.databaseType = 'postgres'
			
		elif env==Environment.ENV_TESTING:
			self.user='poc_role'
			self.password='pocpass'
			self.db='racefoxstar'
			self.host='localhost'
			self.port=5432
			self.databaseType = 'postgres'
		elif env==Environment.ENV_PRODUCTION:
			self.user='poc_role'
			self.password='pocpass'
			self.db='racefoxstar'
			self.host='localhost'
			self.port=5432
			self.databaseType = 'postgres'
		"""