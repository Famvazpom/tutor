# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 16:57:43 2017

@author: fernando
"""

from tutor.sistema_experto.EjerciciosClases.Ejercicios import procedureExcercise

class procedurePolinomio(procedureExcercise):    
    def __init__(self,preg,pol_ltx,symbs, ltx_math_prob="", math_prob=None):                    
        super(procedurePolinomio,self).__init__(symbs,[],preg,math_prob,pol_ltx,ltx_math_prob,pol_ltx)
        self.ltx = pol_ltx
        self.symbs = symbs
        
    def getData(self):        
        d = {}
        d['question'] = self.getQuestion()        
        d['answers'] = []
        d['procedure'] = []
        d['options'] = [""]
        d['exType'] = 3
        d['dataToAssess'] = {"clase":"polynom", "ltx":self.ltx, "symbs":self.symbs}
        
        return d
    
