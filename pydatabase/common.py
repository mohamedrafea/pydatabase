# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 19:48:57 2017

@author: mohamed
"""

class Common(object):
    def __repr__(self):
        return "<{}({})>".format(
            self.__class__.__name__,
            ', '.join(
                ["{}={}".format(k, repr(self.__dict__[k]))
                    for k in sorted(self.__dict__.keys())
                    if k[0] != '_']
            )
        )
        
    def copy(self,orig,excludedFields={}):
        for k in sorted(orig.__dict__.keys()):
            if k[0] != '_' and k not in excludedFields:
                self.__dict__[k] = orig.__dict__[k]
    @classmethod
    def toCSV(self,objects,fileName):
        out = open(fileName, 'w')
        out.write(objects[0].rowHeader())
        for o in objects:
            out.write(o.rowValues())
        out.close()
    def rowHeader(self):
        h = ''
        for k in sorted(self.__dict__.keys()):
            if k[0] != '_':
                if len(h)==0:
                    h = k
                else:
                    h = h + ','+k
        return h+'\n'

    def rowValues(self):
        r = ''
        for k in sorted(self.__dict__.keys()):
            v = str(self.__dict__[k])
            if k[0] != '_':
                if len(r)==0:
                    r = v
                else:
                    r = r + ','+v
        return r+'\n'


