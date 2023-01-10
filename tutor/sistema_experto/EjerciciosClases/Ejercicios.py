# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 12:40:21 2014

@author: fernando
"""

# coding: utf8
from __future__ import division

#from tem_proc import *
from sympy import *
from random import *
from tutor.sistema_experto.LatexProc.Cadenas import *
import random
import string

def id_generator(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

#cualquier ejercicio debe tener:
# 1.- Una pregunta
# 2.- Respuesta 
# 3.- Un identificador (hash)
# 4.- Un título (para desplegar en la página web)
# 5.- Un nombre (con el que se identificará a los eleemntos web: botones, etc. )
class exercise(object):
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.hash = id_generator(30)
        self.title = ""
        self.info = {}
        
    def getQuestion(self):        
        return self.question
        
    def getAnswer(self):
        return self.answer
        
    def getId(self):
        return self.hash
        
class optionsExercise(exercise):
    def __init__(self, question, answer, resps, name):
        self.name = name        
        self.perm = [i for i in range(len(resps))]
        shuffle(self.perm)
        self.indx = self.perm.index(0)
        self.resps = []
        for i in self.perm:
            self.resps.append(resps[i])                        
        super(optionsExercise,self).__init__(question, answer)
        
    def tipo(self):
        return 'options'
    
    def getResps(self):
        return self.resps
    
    def getName(self):
        return self.name
        
    def getPerm(self):
        return self.perm
    
    def getSolIndx(self):
        return self.indx
        
    def getData(self):        
        d = {}
        d['question'] = self.getQuestion()
        d['options'] = self.getResps()
        d['answers'] = [self.getSolIndx()]
        d['procedure'] = []
        d['exType'] = 1
        d['dataToAssess'] = {}
        d['difficulty'] = 0
        d['points'] = 0
        #revisa que las respuestas sean diferentes
        s = set(d["options"])
        if len(s) < len(d["options"]):
        	d['not_solvd'] = True
        return d
        
#answer es un vector con valores booleanos indicando 
#los índices que debe marcar el usuario : [0,0,1,0,1]       
class selectsExercise(exercise):
    def __init__(self, question, answer, resps):
        self.perm = [i for i in range(len(resps))]
        shuffle(self.perm)
        #permuta las respuestas
        self.resps = []        
        tmp_answ = []
        for i in self.perm:
            self.resps.append(resps[i])
            tmp_answ.append(answer[i])
        super(selectsExercise,self).__init__(question, tmp_answ)
    
    def tipo(self):
        return 'selects'
    
    def getResps(self):
        return self.resps
    
    def getName(self):
        return self.name
        
    def getPerm(self):
        return self.perm    
    
    def getData(self):
        
        d = {}
        d['question'] = self.getQuestion()
        d['options'] = self.getResps()        
        d['answers'] = []
        resps = self.getAnswer()
        for i,r in enumerate(resps):
            if r:
                d['answers'].append(i)                
        d['procedure'] = []
        d['exType'] = 2
        d['dataToAssess'] = {}
        d['difficulty'] = 0
        d['points'] = 0
        return d
    
class contrastExercise(exercise):
    def __init__(self, question, answer, incorr, msg):
        if random.random()>0.5:
            self.indx = 0
            self.resps = [answer,incorr]
        else:
            self.indx = 1
            self.resps = [incorr,answer]
        
        self.msg = msg
            
        super(contrastExercise,self).__init__(question, answer)
        

    def tipo(self):
        return 'contrast'    
    
    def getResps(self):
        return self.resps
    
    def getSolIndx(self):
        return self.indx
        
    def getMsg(self):
        return self.msg
    
    def getData(self):
        d = {}
        d['question'] = self.getQuestion()
        d['options'] = self.getResps()
        d['answers'] = [self.getSolIndx()]
        d['procedure'] = []
        d['exType'] = 1
        d['dataToAssess'] = {}
        d['difficulty'] = 0
        d['points'] = 0
        
        return d

#Ejercicio de procedimiento (step by step)
##  1.- Deben contener una lista de variables y de funciones para poder limitar la entrada de cada paso 
##  2.- Deben validar las cadenas de latex que reciban
#   3.- Deben identificar si la cadena latex, después de ser validada, es equivalente a la solución
#   4.- La validación final debe ser muy rigurosa
##  5.- Deben contener una cadena temporal que separe el problema matemático de la pregunta; por ejemplo "Resuelve 3x+2=0", hayq que separar la ecuación de la pregunta para colocarla en el campo de texto y empezar a trabajar sobre ella
#   6.- Deben poder identificar cuando un paso es realmente diferente del anterior (se aplicó un proceso significativo? o se repite el paso anterior?)
class procedureExcercise(exercise):
    def __init__(self,symbs,funcs,preg,math_prob,answer,ltx_math_prob='',ltx_res=''):
        self.symbs = symbs
        self.funcs = funcs        
        #inicia el constructor
        self.math_prob = math_prob
        self.ltx_math_prob = ltx_math_prob
        super(procedureExcercise,self).__init__(preg,answer)                
        self.last_step = ltx_sympy2quill(self.ltx_math_prob)
        self.ltx_res = ltx_res
        
    def tipo(self):
        return 'steps'
        
    def getSymbols(self):
        return self.symbs
        
    def getMathProblem(self):
        return self.math_prob

    def getLtxMathProblem(self):
        return self.ltx_math_prob
        
    def getLtxAnswer(self):
        if self.ltx_res == '':
            return latex(self.answer)
        else:
            return self.ltx_res
    
    #recibe una cadena de código látex e indica si es válida o no            
    #además convierte la cadena látex a una cadena 
    #que puede convertirse a una expresión sympy
    def validaLtx(self,ltx):
        return valida_ltx(ltx,self.symbs,self.funcs) #ambia la cadena latex
        
    #recibe una cadena de latex (debe ser previamente validada) 
    #y regresa una expresión de sympy
    def cad2exp(self,cad):
        e = str2expr(cad,self.symbs)
        return e
        
    def pasoCorrecto(self,ltx):
        pass
    
    def esSolucion(self,ltx):
        pass
    
    def getData(self):
        pass
    
    
