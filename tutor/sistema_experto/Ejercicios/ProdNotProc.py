# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:41:39 2015

@author: fernando
"""
from tutor.sistema_experto.LatexProc.Cadenas import factores3, ltx_terminos2
from sympy import expand
from tutor.sistema_experto.EjerciciosClases.Ejercicios import *

class procedureProdNot(procedureExcercise):
    def __init__(self, d):
        self.proc = None if not 'proc' in d.keys() else d['proc']
        super(procedureProdNot,self).__init__(d['symbs'],[],d['preg'],d['e'],d['ef'],d['ltx_math_prob'])
        
    #indica si la cadena guarda un resultado que es equivalente
    #al problema original
    # la función regresa:
    #  -1 Si la cadena no es válida (error de sintaxis)
    #  -2 Si no se presenta un cambio con respecto al paso anterior
    #   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
    #   1 Si el paso es correcto
    
    def getData(self):
        d = {}
        d['question'] = self.getQuestion()        
        d['answers'] = []
        d['procedure'] = []
        d['ltxMathProb'] = self.getLtxMathProblem()
        d['exType'] = 4 #step-by step
        d['dataToAssess'] = {"clase":"ProdNot",'ans':latex(self.getAnswer()),'symbs':self.getSymbols()}
        d['procedure'] = self.proc
        
        return d
    
    
    def pasoCorrecto(self,ltx):

        d = super(procedureProdNot,self).validaLtx(ltx)

        #la cadena no es válida (error de sintaxis)
        if not d['valida']:
            return -1
        
        #el paso es diferente al anterior
        if self.last_step == ltx:
            return -2
        
        #utilizar la función de la clase
        cad = d['cad']
        e = super(procedureProdNot,self).cad2exp(cad)

        if e == False:
            return 0
        else:
            #extiende la cadena  la compara con el resultado
            ext_e = expand(e)
            if ext_e == self.math_prob:
                self.last_step = ltx
                return 1
            else:
                return 0
        
    def esSolucion(self,ltx):
        sol_ot = self.answer.as_ordered_terms()
        #extrae los términos de la cadena látex
        trms = ltx_terminos2(ltx,self.symbs)
        #recupera los factores de cada término y los compara con la solución
        
        for t in trms:
            f = False
            for tt in sol_ot:
                tt_of = tt.as_ordered_factors()
                if self.factores_iguales(t,tt_of) == 1:
                    sol_ot.remove(tt)
                    f = True
                    break
            if not f:
                return 0
        if len(sol_ot) == 0:
            return 1
        else:
            return 0                
                    
            
    def factores_iguales(self,cad,sol_of):
        ltx_ajst = ajusta_cad_latex(cad,self.symbs)
        resp_of = []
        facts = factores3(ltx_ajst,True)
        
        #extrae los fcatores del término
        for f in facts:
            fe = super(procedureProdNot,self).cad2exp(f['c'])
            #if fe != 1:
            if not f['in_num']:
                if type(fe) == type(1):
                    resp_of.append(Rational(1,fe))
                else:
                    resp_of.append(fe**(-1))
            else:
                resp_of.append(super(procedureProdNot,self).cad2exp(f['c']))
        
        #detecta si algún factor es una constante
        #y si sol_of y res_of tienen diferente tamaño
        digs = ['0','1','2','3','4','5','6','7','8','9']    
        dif = 1
        for f in resp_of:
            if f in sol_of:
                sol_of.remove(f)
            elif -f in sol_of:
                sol_of.remove(-f)
                dif = -dif
            #busca dividir el factor entre otro
            else:
                found = False
                if type(f) != type(1):
                    f_ot = f.as_ordered_terms()                    
                else:
                    f_ot = [f]
                for ff in sol_of:
                    if type(ff) != type(1):
                        ff_ot = ff.as_ordered_terms()
                    else:
                        ff_ot = [ff]
                    if len(f_ot) == len(ff_ot):                                                
                        d = factor(f)/factor(ff)
                        ad = abs(d)
                        is_num = True
                        st_d = str(ad)                          
                        for s in st_d:
                            if not s in digs:
                                is_num = False
                                break
                        if is_num:
                            sol_of.remove(ff)
                            dif = dif*d
                            found = True
                            break                            
                if not found:
                    dif = dif*f
            
        pr = 1
        for f in sol_of:
            pr = pr*f
         
        if (dif == 1 or dif == -1) and dif == pr:
            return 1
        else:
            return 0
        
            

