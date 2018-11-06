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
        
    def copy(self,orig):
        for k in sorted(orig.__dict__.keys()):
            if k[0] != '_':
                self.__dict__[k] = orig.__dict__[k]
