# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:21:34 2017

@author: mohamed
"""
#from pydatabase.common import Common
from pycommonutil.common import Common
import configparser
class Environment(Common):
    ENV_LOCAL = 1
    ENV_TESTING = 2
    ENV_PRODUCTION = 3
    localEnv = None
    testingEnv = None
    productionEnv = None
    configParser = configparser.RawConfigParser()
    configFilePath = r'pydatabase.cfg'
    configParser.read(configFilePath)
    def __init__(self,env):
        self.env = env

    @classmethod
    def getProperty(cls,section,name):
        return cls.configParser.get(section,name)
    def getName(self):
        if self.env==self.ENV_LOCAL:
            return "local"
        elif self.env==self.ENV_TESTING:
            return "testing"
        elif self.env==self.ENV_PRODUCTION:
            return "production"

    @classmethod
    def getEnv(cls,env):
        #print("env=",env)
        if env==cls.ENV_LOCAL:
            return cls.localEnv
        elif env==cls.ENV_TESTING:
            return cls.testingEnv
        elif env==cls.ENV_PRODUCTION:
            return cls.productionEnv